# Sistema de Cadastro de Usuários

## Descrição
Este projeto implementa um sistema simples de cadastro de usuários em **C++**, que coleta informações pessoais e as armazena em um arquivo de texto.  
O objetivo é registrar dados básicos de identificação e contato de forma estruturada e acessível.

---

## Funcionalidades

### Login
- O sistema exige que o usuário insira seu **CPF** e sua **senha**.  
- Caso o usuário não lembre sua senha, há uma opção de recuperação.  
- O CPF deve ser escrito **com pontuação e traçado**.  
- O sistema realiza verificações de:
  - CPF existente  
  - Senha correta  
  - Tipo de usuário (Cidadão ou Gestor)  
  - Duplicação de CPF no momento do cadastro  

### Cadastro
Coleta os seguintes dados do usuário:

#### Cidadão (Tipo C)
- Nome completo  
- CPF  
- Data de nascimento  
- E-mail  
- Senha  
- Telefone  
- Cidade  
- CEP  

#### Gestor (Tipo G)
- Nome completo  
- CPF  
- Data de nascimento  
- E-mail  
- Senha  
- Telefone  
- Cidade  
- CEP  
- Empresa vinculada  
- Cargo  
- E-mail institucional  
- CNPJ  

Todas as informações são salvas no arquivo **`Registro_usuarios.txt`**.

---

## 🧩 Estrutura do Código

| Função | Descrição |
|--------|------------|
| `checa_cpf(string cpf)` | Verifica se um CPF já está cadastrado |
| `cadastro_usuario_cidadao()` | Cadastra um novo cidadão (Tipo C) |
| `cadastro_gerente()` | Cadastra um novo gestor (Tipo G) |
| `busca_cadastro(string cpf)` | Localiza a linha do CPF dentro do arquivo de registros |
| `checa_senha(string cpf, string senha)` | Confere se a senha digitada corresponde ao CPF informado |
| `checa_cadastro(string cpf, string senha, int tipo)` | Autentica o usuário de acordo com o tipo (Cidadão ou Gestor) |

---

## Como Executar

### Compilação
```bash
g++ cadastro_usuarios.cpp -o smartcity
```

### Execução
```bash
./smartcity
```

### Requisitos
- Compilador **C++17** ou superior  
- Sistema operacional **Windows**, **Linux** ou **macOS**

---

## Tecnologias Utilizadas
- **Linguagem:** C++17  
- **Bibliotecas:**
  - `<iostream>` – entrada e saída de dados  
  - `<fstream>` – manipulação de arquivos  
  - `<string>` – uso de strings  
  - `<limits>` – controle do buffer de entrada  

---

## Estrutura de Arquivos
```
├── cadastro_usuarios.cpp     # Código principal do sistema
├── Registro_usuarios.txt     # Arquivo de armazenamento dos cadastros
└── README_registros.md       # Documentação do projeto
```

