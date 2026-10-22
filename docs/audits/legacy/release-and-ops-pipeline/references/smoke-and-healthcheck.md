# Protocolo de Smoke Tests Pós-Deploy & Verificação de Entrega

Execute os testes correspondentes ao arquétipo do projeto no **Gate 5** da `release-and-ops-pipeline` antes de declarar o encerramento da entrega.

## 1. Arquétipo A — Relatório Quarto / GitHub Pages
1. **Verificação de Artefatos Estáticos Locais (`docs/` ou `_site/`):**
   - Confirme que `index.html` existe e não está vazio (`test -s docs/index.html`).
   - Confirme que `.nojekyll` existe quando servido via pasta `docs/`.
   - Verifique se todas as imagens `<img src="...">` relativas referenciadas no `index.html` existem fisicamente no diretório compilado *(nota: valida caminhos relativos locais; URLs externas `http(s)` e `data:` são ignoradas)*:
     ```bash
     python3 -c "
     import re, os, sys
     html_path = 'docs/index.html' if os.path.exists('docs/index.html') else '_site/index.html'
     base_dir = os.path.dirname(html_path)
     with open(html_path, errors='ignore') as f:
         imgs = re.findall(r'<img[^>]+src=[\"\\\']([^\"\\\']+)[\"\\\']', f.read())
     missing = [i for i in imgs if not i.startswith(('http', 'data:', '/')) and not os.path.exists(os.path.normpath(os.path.join(base_dir, i)))]
     print(f'Total imagens checadas: {len(imgs)} | Quebradas: {len(missing)}')
     if missing: print('Faltando:', missing); sys.exit(1)
     "
     ```
2. **Verificação Remota (URL do GitHub Pages):**
   - Teste o status HTTP 200 da URL publicada:
     ```bash
     curl -sL -o /dev/null -w "%{http_code}\n" "<URL_PUBLICADA>"
     ```

## 2. Arquétipo B — Software, Web, APIs & Containers
1. **Healthcheck de API / Backend:**
   - Verifique se o serviço responde `200 OK` na rota `/health` (ou `/docs` / `/openapi.json`) com tempo de resposta `< 2s`:
     ```bash
     curl -fsSL -w "\nHTTP: %{http_code} | Time: %{time_total}s\n" "<URL_API>/health"
     ```
2. **Smoke Test de UI (quando houver Frontend):**
   - Acione a skill `webapp-testing` (Playwright) para carregar a URL principal, verificar ausência de erros `console.error` / `pageerror` e confirmar renderização do elemento raiz.

## 3. Arquétipo C — CLI, Scripts & Pacotes Python
1. **Teste de Empacotamento e Execução Isolada:**
   - Valide que o pacote ou script roda fora do diretório de desenvolvimento e retorna código POSIX `0` para `--help` e `--version`:
     ```bash
     uv run <comando-cli> --help
     echo "Exit code: $?"
     ```

## 4. Procedimento de Contingência e Rollback
Se qualquer smoke test do Gate 5 falhar em produção:
1. **Não encerre o Gate 5.** Reporte imediatamente o log do erro ao usuário.
2. Em caso de regressão crítica em produção:
   - *GitHub Pages / Git:* Reverter o commit de publicação (`git revert HEAD`) ou restaurar a tag estável anterior (`git checkout <tag-anterior>`).
   - *Containers / Cloud:* Reapontar o serviço para a imagem/revisão anterior homologada.
