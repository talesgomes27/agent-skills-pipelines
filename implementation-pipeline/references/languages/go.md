# Go

Leia quando o componente da tarefa é escrito em Go.

## Descubra no projeto

- Versão e dependências: `go.mod` e `go.sum`. A linha `go` declara a versão mínima, e desde o Go 1.21 esse mínimo é obrigatório: toolchain mais antigo recusa o módulo. A linha `toolchain` sugere um toolchain específico.
- Comandos: `Makefile`, `magefile.go`, `.golangci.yml` e o workflow de CI.

Use os comandos do projeto e o toolchain que o `go.mod` pede. Diga no relatório a versão da linha `go` e a do toolchain local. Rode com `GOTOOLCHAIN=local`: sem isso, quando o `go.mod` pede um toolchain que não está na máquina, o próprio `go test` o baixa para o cache de módulos. Baixar toolchain é instalar ferramenta, um efeito do catálogo do contrato comum, e pede A2 com a versão, a origem e onde fica. Baixar os módulos com hash no `go.sum` já versionado e aceito equivale a instalar do lock aceito; acrescentar ou atualizar módulo, ou rodar `go install`, pede A2.

## Testes e checks

Exemplos a confirmar no projeto:

- `go test ./...`: roda também um subconjunto do `go vet` sobre o pacote e os testes.
- `go vet ./...` para todas as checagens do vet.
- `gofmt -l .` lista os arquivos fora do formato, sem reescrevê-los.
- `go test -race ./...` quando há concorrência. O detector só acha corridas nos caminhos que executam.

## Armadilhas

- Erro ignorado: `v, _ := f()` descarta o erro, e o código segue com valor zero ou `nil`. Trate todo erro retornado.
- Goroutine sem cancelamento: passe `context.Context` como primeiro parâmetro e chame o `cancel` de `WithCancel`, `WithTimeout` ou `WithDeadline`. Esquecer o `cancel` vaza o contexto até o pai ser cancelado ou o prazo vencer.
- Map nil: ler de um map nil funciona como map vazio, mas escrever causa panic. Crie com `make`.
- Variável de laço: a semântica de uma variável por iteração só vale em módulo com `go 1.22` ou mais no `go.mod`. Em módulo mais antigo, closures e goroutines dentro do laço compartilham a mesma variável.
- Corrida de dados: map ou variável usada por várias goroutines sem sincronização dá resultado errado sem erro de compilação. Rode os testes com `-race`.

## Fontes

Conferido em 08/11/2026:

- https://go.dev/ref/mod (diretivas `go` e `toolchain`)
- https://pkg.go.dev/cmd/go (`go test` e `go vet`)
- https://pkg.go.dev/cmd/gofmt
- https://go.dev/doc/articles/race_detector
- https://go.dev/doc/effective_go (erros e blank identifier)
- https://pkg.go.dev/context
- https://go.dev/blog/maps
- https://go.dev/blog/loopvar-preview
