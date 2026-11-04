# MiniGit

Este projeto representa apenas o historico de um repositorio: commits, seus pais e referencias de branches.
Ele nao acessa arquivos e deixa visivel o custo de cada operacao pela propriedade `passos`.

## Medicao

| commits | passos do commitar | passos do log |
|---:|---:|---:|
| 10 | 2 | 10 |
| 100 | 2 | 100 |
| 1000 | 2 | 1000 |

## Observacoes

### 1. Escrita e leitura

O commit tem duas atualizacoes: guardar o novo registro e apontar a branch para ele, por isso o custo e fixo.
O log precisa visitar cada commit que consegue alcancar, entao um historico maior exige mais trabalho.

### 2. Consulta de mensagem e busca por texto

Com o identificador, o dicionario encontra a mensagem consultando uma chave diretamente, em um passo.
Para achar um trecho de texto e preciso comparar mensagens uma a uma, pois o texto procurado esta nos valores.

### 3. Merge e estrutura do historico

O merge registra como pais tanto o commit da branch atual quanto o da outra branch, preservando as duas origens.
Como um commit pode apontar para mais de um anterior, o historico forma ramificacoes e e um grafo, nao uma sequencia unica.

### 4. Pais imutaveis para quem consulta

Os pais ficam guardados em uma lista para que o historico possa ser percorrido.
O metodo devolve uma tupla, impedindo que quem consulta altere acidentalmente essa lista interna.
