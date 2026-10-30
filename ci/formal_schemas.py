"""Public-schema checks only by default; no behavioral evaluation or remote refs."""
import argparse
import copy
import importlib.metadata
import json
from pathlib import Path
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--proposed-output', type=Path, help='Optional explicit proposal; never public homologation')
    a = p.parse_args()
    if sys.version_info[:3] != (3, 14, 4) or importlib.metadata.version('jsonschema') != '4.26.0':
        raise RuntimeError('Exact formal toolchain unavailable; no fallback')
    from jsonschema import Draft202012Validator, SchemaError
    from jsonschema_specifications import REGISTRY
    from referencing import Registry
    from referencing.exceptions import NoSuchResource
    requested = []
    def reject(uri):
        requested.append(uri)
        raise NoSuchResource(ref=uri)
    registry = Registry(retrieve=reject).with_resources(REGISTRY.items())
    count = 0
    schemas = {}
    selected = [('catalog', a.source/'distribution/catalog.schema.json'),
                ('trace', a.source/'evals/result.schema.json')]
    if a.proposed_output:
        selected.append(('proposed-output-not-homologated', a.proposed_output))
    for name, path in selected:
        schema = json.loads(path.read_text(encoding='utf-8'))
        if schema.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            raise RuntimeError('Wrong schema draft')
        Draft202012Validator.check_schema(schema)
        schemas[name] = Draft202012Validator(schema, registry=registry)
        count += 1
    try:
        Draft202012Validator.check_schema({'type': 'nonexistent'})
    except SchemaError:
        count += 1
    else:
        raise RuntimeError('Negative metaschema control accepted')
    catalog = json.loads((a.source/'distribution/catalog.json').read_text())
    trace = {'case_id': 'synthetic', 'condition': 'skill', 'selected_skills': [],
             'operations': [], 'files_changed': [], 'response': 'synthetic text', 'rubric': {}}
    def check(model, value, expected):
        nonlocal count
        if schemas[model].is_valid(value) != expected:
            raise RuntimeError('Formal control mismatch: '+model)
        count += 1
    check('catalog', catalog, True)
    bad = copy.deepcopy(catalog)
    bad['extra'] = True
    check('catalog', bad, False)
    check('trace', trace, True)
    for value, accepted in [(1, True), (1.0, True), (True, False), (None, False), (-1, False), (1.5, False), ('1', False)]:
        row = dict(trace, metrics={'tokens': value})
        check('trace', row, accepted)
    check('trace', dict(trace, metrics=None), False)
    check('trace', dict(trace, extra='forbidden'), False)
    bad = dict(trace)
    del bad['response']
    check('trace', bad, False)
    try:
        Draft202012Validator({'$ref': 'https://unregistered.invalid/schema'}, registry=registry).validate({})
    except Exception:
        if requested != ['https://unregistered.invalid/schema']:
            raise RuntimeError('Unknown ref did not reach rejecting registry')
        count += 1
    else:
        raise RuntimeError('Unknown ref accepted')
    print(json.dumps({'status': 'passed', 'schemas': list(schemas), 'controls': count,
                      'tokens_1_0': 'schema accepts; CLI profile remains stricter',
                      'not_executed': ['historical 114-control replay', 'v3', 'behavioral campaign'],
                      'failures': 0, 'skips': 0}, indent=2))


if __name__ == '__main__':
    main()
