🗑️ README – Sistema de Coleta de Lixo Inteligente

Descrição
Este projeto simula um sistema de coleta de lixo inteligente em C++.
Cada lixeira possui um sensor que é acionado quando a coleta é feita. O sistema percorre as lixeiras em ordem sequencial, simulando a coleta diária entre 6:00 e 6:30.
O sistema registra e monitora o processo de coleta, identificando lixeiras não coletadas e reportando possíveis problemas operacionais.

---

Funcionalidades

Coleta Sequencial
- A coleta percorre todas as lixeiras listadas no arquivo lixeiras.txt.
- Cada lixeira tem um sensor booleano indicando se foi coletada.
- Caso uma lixeira não seja coletada dentro do horário, o sistema gera um alerta de falha.

Armazenamento de Dados
- As informações são lidas de um arquivo lixeiras.txt, contendo uma lista de lixeiras com status inicial.
- Após cada execução, o sistema grava o resultado (coletada / falha) no mesmo arquivo.

Simulação de Tempo
- A simulação de coleta dura 30 minutos (tempo acelerado).
- O sistema exibe no terminal o progresso em tempo real.

---

Estrutura do Código

| Função | Descrição |
|--------|------------|
| carregarLixeiras() | Lê o arquivo lixeiras.txt e carrega as lixeiras na memória |
| simularColeta() | Simula a coleta sequencial das lixeiras entre 6:00 e 6:30 |
| registrarFalha() | Marca e exibe lixeiras não coletadas |
| main() | Controla o fluxo principal do programa |

---

Compilação e Execução

g++ coleta_inteligente.cpp -o coleta
./coleta

Requisitos
- Compilador C++17 ou superior
- Sistema operacional Linux, Windows ou macOS
- Terminal compatível com comando clear

---

Tecnologias Utilizadas
- Linguagem: C++17
- Bibliotecas:
  - <iostream> – Entrada e saída de dados
  - <fstream> – Manipulação de arquivos
  - <string> – Manipulação de texto
  - <thread> e <chrono> – Simulação temporal
  - <cstdlib> – Comando system("clear")

---

Estrutura de Arquivos
├── coleta_inteligente.cpp  # Código principal do sistema
├── lixeiras.txt             # Banco de dados das lixeiras
├── README_coleta.txt        # Documentação do projeto
