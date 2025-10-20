🚦 README – Sistema de Semáforos Inteligentes

Descrição
Este projeto implementa um sistema de semáforos inteligentes em C++, com o objetivo de otimizar o fluxo de veículos em cruzamentos urbanos.
O sistema simula o funcionamento de semáforos sincronizados entre si (Norte-Sul e Leste-Oeste), controlando o tempo de cada ciclo de cor e armazenando informações de tráfego.
O programa lê os semáforos a partir de um arquivo semaforos.txt, que contém um número variável de semáforos para facilitar a modificação do ambiente de teste.

---

Funcionalidades

Ciclos de Operação
- Cada semáforo possui três estados:
  - Verde: 25 segundos
  - Amarelo: 5 segundos
  - Vermelho: 30 segundos

- Os semáforos Norte/Sul e Leste/Oeste são sincronizados:
  - Norte e Sul: iniciam juntos (0s).
  - Leste e Oeste: iniciam com atraso de 30s.

Monitoramento
- A cada atualização de tempo:
  - O terminal é limpo automaticamente para mostrar o estado atual (função limpar()).
  - O sistema mostra o estado e tempo restante de cada semáforo.
  - É registrada a quantidade de veículos que passam por cada semáforo a cada hora.

Registro de Dados
- As informações dos semáforos e do tráfego são armazenadas em um arquivo semaforos.txt, que pode ser usado como banco de dados simples.

---

Estrutura do Código

| Função | Descrição |
|--------|------------|
| limpar() | Limpa o terminal a cada atualização de ciclo |
| atualizarSemaforos() | Atualiza o estado (verde, amarelo, vermelho) de todos os semáforos conforme o tempo |
| contarCarros() | Simula a contagem de veículos que passam por cada semáforo |
| main() | Controla o loop principal e sincroniza os semáforos |

---

Compilação e Execução

g++ semaforos.cpp -o semaforos -pthread
./semaforos

Requisitos
- Compilador C++17 ou superior
- Sistema operacional Linux, Windows ou macOS
- Terminal compatível com comando clear

---

Tecnologias Utilizadas
- Linguagem: C++17
- Bibliotecas:
  - <iostream> – Entrada e saída de dados
  - <thread> – Controle de tempo e threads
  - <chrono> – Manipulação de intervalos de tempo
  - <fstream> – Leitura e gravação de arquivo
  - <cstdlib> – Comando system("clear")

---

Estrutura de Arquivos
├── semaforos.cpp          # Código principal do sistema
├── semaforos.txt          # Banco de dados dos semáforos
├── README_semaforos.txt   # Documentação do projeto
