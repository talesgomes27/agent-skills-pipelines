"""Linux-only deterministic executor; no agent/runtime containment claim."""
import argparse
import ctypes
import ctypes.util
import errno
import json
import os
from pathlib import Path
import platform
import resource
import socket


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('command', nargs=argparse.REMAINDER)
    a = p.parse_args()
    argv = a.command[1:] if a.command[:1] == ['--'] else a.command
    if platform.system() != 'Linux' or platform.machine() != 'x86_64' or not argv:
        raise RuntimeError('Requires Linux x86_64 and an explicit trusted command; no fallback')
    work = a.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    library = ctypes.util.find_library('seccomp')
    if not library:
        raise RuntimeError('libseccomp unavailable; offline execution blocked')
    lib = ctypes.CDLL(library, use_errno=True)
    lib.seccomp_init.argtypes = [ctypes.c_uint32]
    lib.seccomp_init.restype = ctypes.c_void_p
    lib.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    lib.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    lib.seccomp_load.argtypes = [ctypes.c_void_p]
    lib.seccomp_release.argtypes = [ctypes.c_void_p]
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(38, 1, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), 'Cannot set no_new_privs')
    calls = ('socket socketpair connect bind listen accept accept4 sendto recvfrom '
             'sendmsg recvmsg sendmmsg recvmmsg shutdown getsockname getpeername '
             'setsockopt getsockopt io_uring_setup io_uring_enter io_uring_register').split()
    ctx = lib.seccomp_init(0x7fff0000)
    if not ctx:
        raise RuntimeError('Cannot create seccomp filter')
    try:
        for name in calls:
            number = lib.seccomp_syscall_resolve_name(name.encode())
            if number < 0 or lib.seccomp_rule_add(ctx, 0x00050000 | errno.EPERM, number, 0) != 0:
                raise RuntimeError('Cannot deny syscall: ' + name)
        # No inherited socket descriptors beyond stdio reach the filtered command.
        ceiling = resource.getrlimit(resource.RLIMIT_NOFILE)[0]
        os.closerange(3, 1048576 if ceiling == resource.RLIM_INFINITY else ceiling)
        if lib.seccomp_load(ctx) != 0:
            raise RuntimeError('Cannot load seccomp filter')
    finally:
        lib.seccomp_release(ctx)
    controls = {}
    for name, family in [('IPv4', socket.AF_INET), ('IPv6', socket.AF_INET6), ('Unix', socket.AF_UNIX)]:
        try:
            s = socket.socket(family, socket.SOCK_STREAM)
        except OSError as exc:
            if exc.errno != errno.EPERM:
                raise
            controls[name] = 'EPERM'
        else:
            s.close()
            raise RuntimeError('Network control failed: ' + name)
    marker = work/'local-io-control'
    marker.write_bytes(b'permitted local IO')
    if marker.read_bytes() != b'permitted local IO':
        raise RuntimeError('Positive IO control failed')
    status = Path('/proc/self/status').read_text()
    if 'NoNewPrivs:\t1' not in status or 'Seccomp:\t2' not in status:
        raise RuntimeError('Kernel confinement status missing')
    print(json.dumps({'offline_controls': controls, 'local_io': 'passed', 'denied_syscalls': calls,
                      'scope': 'deterministic child only; not G4'}), flush=True)
    env = {k:v for k,v in os.environ.items() if k in ('PATH', 'LANG', 'LD_LIBRARY_PATH')}
    env.update(HOME=str(work), TMPDIR=str(work), PYTHONDONTWRITEBYTECODE='1', PIP_CONFIG_FILE='/dev/null',
               PIP_DISABLE_PIP_VERSION_CHECK='1', PIP_NO_INDEX='1', PIP_NO_CACHE_DIR='1')
    os.execvpe(argv[0], argv, env)


if __name__ == '__main__':
    main()
