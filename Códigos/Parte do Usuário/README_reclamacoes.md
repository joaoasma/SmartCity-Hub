# 🗳️ Portal de Reclamações

## Descrição
Este projeto implementa um **portal de reclamações** em **C++**, permitindo que cidadãos registrem problemas relacionados a serviços públicos e infraestrutura urbana.  
O programa apresenta um menu com diferentes categorias de reclamação, recebe o comentário do usuário e armazena as informações em um arquivo de texto.
O usuário poderá criar um comentário por execução, dificultando spam de comentários. Ao entrar no programa, o usuário será obrigado a escolher uma opção válida, de 0 à 9, com zero para sair (uma opção diferente dessas acarreta em um looping até a escolha for correta). 
O objetivo é fornecer um canal simples e rápido de comunicação entre o cidadão e os órgãos responsáveis.

---

## Funcionalidades

### Menu de Reclamações
- O sistema exibe uma lista de **10 opções** de assuntos para reclamação:
  1. Problema com o APP  
  2. Monitoramento de Sensores  
  3. Semáforos  
  4. Iluminação Pública  
  5. Coleta de Lixo  
  6. Transporte  
  7. Segurança  
  8. Acidente  
  9. Outro  
  0. Sair  

- O usuário escolhe o tipo de reclamação digitando o número correspondente.  
- Caso uma opção inválida seja informada, o sistema exibe uma **mensagem de erro** e solicita nova entrada.  

### Registro de Reclamação
- Após selecionar o tipo, o sistema solicita que o usuário **digite sua reclamação**.  
- O texto informado é salvo no arquivo **`reclamacoes.txt`**, junto com o tipo de problema escolhido.  
- O programa garante a **privacidade das informações pessoais**, pois não salva informações pessoais não comentadas, conforme mensagem exibida ao usuário.  
- Caso ocorra falha na abertura do arquivo, o sistema exibe uma mensagem de erro.  

---

## 🧩 Estrutura do Código

| Função                       |                                Descrição                                  |
|------------------------------|---------------------------------------------------------------------------|
| `tipo_reclamacao(int opcao)` |   Retorna o nome da categoria de reclamação conforme a opção escolhida    |
| `cria_reclamacao(int opcao)` | Solicita o comentário e grava as informações no arquivo `reclamacoes.txt` |
|          `main()`            |         Exibe o menu principal e gerencia o fluxo do programa             |

---

## Compilação e execução
```bash
g++ portal_reclamacoes.cpp -o reclamacoes
./reclamacoes
```
### Requisitos
- Compilador **C++17** ou superior  
- Sistema operacional **Windows**, **Linux** ou **macOS**

---

## Tecnologias Utilizadas
- **Linguagem:** C++17  
- **Bibliotecas:**
  - `<iostream>` – entrada e saída de dados  
  - `<fstream>` – gravação das reclamações no arquivo  
  - `<string>` – manipulação de textos e comentários  

## Load Generator

O arquivo **`load_generator.cpp`** é um gerador de eventos de teste para o portal de reclamações.  
Ele cria automaticamente um grande número de reclamações simuladas no mesmo formato do programa principal, permitindo **testes de performance e validação** sem alterar os dados reais.  
O número de eventos pode ser definido pelo usuário (padrão: 50.000), e os registros são salvos em **`reclamacoes_test.txt`**.

## Execução do Load Generator

### Compilação
```bash
g++ load_generator.cpp -o load_generator

./load_generator           # gera 50.000 eventos simulados (padrão)
./load_generator 100000    # gera 100.000 eventos simulados
```

---

## 🗂️ Estrutura de Arquivos
├── reclamacoes.cpp # Código principal do sistema
├── reclamacoes.txt # Arquivo onde as reclamações são salvas
└── README_reclamacoes.md # Documentação do projeto
└──load_generator.cpp
```