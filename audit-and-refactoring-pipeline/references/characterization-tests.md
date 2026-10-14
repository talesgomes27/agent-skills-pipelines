# Protocolo de Testes de Caracterização (Pinning Tests / Golden Master)

Este protocolo é obrigatório no **Gate 3** da `audit-and-refactoring-pipeline` antes de modificar qualquer módulo legado sem cobertura de testes confiável.

## 1. Regra de Ouro (Preservação Comportamental)
O teste de caracterização registra o comportamento **atual** do sistema em produção como uma rede de segurança (*Safety Net*).
- **Invariante:** Nenhum teste de caracterização pode falhar durante as refatorações estruturais do Gate 4, **exceto** quando a fatia atual estiver corrigindo intencionalmente um bug classificado como **Crítico (P0)** no `docs/audit-report.md`.

## 2. Implementação Prática por Arquétipo (`pytest`)

### 2.1 Arquétipo A (Pipelines de Dados e Modelos)
1. Fixe a semente global (`np.random.seed(42)`) e crie uma amostra reduzida determinística (20 a 100 linhas).
2. Grave em `tests/characterization/test_pinning_<modulo>.py` asserções que congelem:
   - Colunas de saída, ordem e `dtypes` exatos.
   - Dimensões (`shape`) pós-transformação e contagem de nulos.
   - Somas de verificação e estatísticas invariantes (`np.isclose(df['feature'].sum(), valor_registrado, rtol=1e-5)`).

### 2.2 Arquétipo B (APIs, Serviços e Repositórios)
1. Capture pares reais de `(payload_entrada, resposta_esperada)` nos endpoints ou serviços principais.
2. Congele o status HTTP, o schema JSON retornado e as transições de estado no banco de teste.

### 2.3 Arquétipo C (Scripts e Ferramentas CLI)
1. Invoque o comando via `subprocess.run([sys.executable, ...], capture_output=True, text=True)`.
2. Congele o código de saída POSIX (`returncode`), o `stdout` padrão e as mensagens de erro em `stderr`.

## 3. Protocolo *Verify-Revert-Stop* (Durante o Gate 4)
Ao final de cada fatia de refatoração no Gate 4:
1. Execute `pytest` completo (incluindo `tests/characterization/`).
2. Se houver quebra não intencional: **reverta imediatamente a fatia** (`git checkout -- <arquivos>`) e reavalie o acoplamento antes de tentar novamente.
