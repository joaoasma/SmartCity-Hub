#include <iostream>
#include <cstring>
#include <fstream>
#include <string>
#include <limits>
using namespace std;

struct cadastro{

   string nome_completo;
   string cpf;
   string data_nascimento; 

   string email;
   string senha;
   string telefone;

   string cidade;
   string bairro;
   string cep;

   string empresa;
   string cargo;
   string email_inst;
   string cnpj;

};

bool checa_cpf(string cpf){     //avança pelo registro e confere se há algum cpf igual ao inserido

    ifstream arq("registro_usuarios.txt");
    string linha;

    // percorrendo o arquivo
    while(getline(arq,linha)){
        // buscando o cpf nas linhas
        if(linha.find(cpf) != string::npos){
            return false;
        }
    }
    return true;
}

void cadastro_usuario_cidadao(){ // marcado no registro como tipo C

    // abre o arquivo para escrever no fim
    ofstream arq("registro_usuarios.txt", ios::app);

    // coletando dados do usuário
    struct cadastro user;

    cout << "\033[36mPreencha as informacoes:\033[0m \n\n";
 
    cout << "Nome completo: ";
    getline(cin,user.nome_completo);

    cout << "CPF: ";
    getline(cin,user.cpf);

    // confere a exclusividade do cpf
    if(checa_cpf(user.cpf) == false){
        cout << "\nO cadastro nao foi realizado pois o CPF ja esta em uso";
        return;
    }

    cout << "Data de nascimento: ";
    getline(cin,user.data_nascimento);

    cout << "Email: ";
    getline(cin,user.email);

    cout << "Senha: ";
    getline(cin,user.senha);

    cout << "Telefone: ";
    getline(cin,user.telefone);

    cout << "Cidade: ";
    getline(cin,user.cidade);

    cout << "Bairro: ";
    getline(cin,user.bairro);

    cout << "CEP: ";
    getline(cin,user.cep);

    cout << "\nCadastro realizado com sucesso!";

    arq << "Nome completo: " << user.nome_completo <<
    "\nCPF: " << user.cpf <<
    "\nData de nascimento: " << user.data_nascimento <<
    "\nEmail: " << user.email <<
    "\nSenha: " << user.senha <<
    "\nTelefone: " << user.telefone <<
    "\nCidade: " << user.cidade <<
    "\nBairro: " << user.bairro <<
    "\nCEP: " << user.cep << 
    "\nTipo: C"<< "\n\n"; 

    arq.close();
}

void cadastro_gerente(){ // marcado no registro como tipo G

    // abre o arquivo para escrever no fim
    ofstream arq("registro_usuarios.txt", ios::app);

    // coletando dados do usuário
    struct cadastro user;

    cout << "\033[36mPreencha as informacoes:\033[0m \n\n";
 
    cout << "Nome completo: ";
    getline(cin,user.nome_completo);

    cout << "CPF: ";
    getline(cin,user.cpf);

    // confere a exclusividade do CPF
    if(checa_cpf(user.cpf) == false){
        cout << "\nO cadastro nao foi realizado pois o CPF ja esta em uso";
        return;
    }

    cout << "Data de nascimento: ";
    getline(cin,user.data_nascimento);

    cout << "Email: ";
    getline(cin,user.email);

    cout << "Senha: ";
    getline(cin,user.senha);

    cout << "Telefone: ";
    getline(cin,user.telefone);

    cout << "Cidade: ";
    getline(cin,user.cidade);

    cout << "Bairro: ";
    getline(cin,user.bairro);

    cout << "CEP: ";
    getline(cin,user.cep);

    // informações exclusivas para gerente 

    cout << "\nEmpresa vinculada: ";
    getline(cin,user.empresa);

    cout << "Cargo: ";
    getline(cin,user.cargo);

    cout << "Email institucional: ";
    getline(cin,user.email_inst);

    cout << "CNPJ: ";
    getline(cin,user.cnpj);

    cout << "\nCadastro realizado com sucesso!";
    
    arq << "Nome completo: " << user.nome_completo <<
    "\nCPF: " << user.cpf <<
    "\nData de nascimento: " << user.data_nascimento <<
    "\nEmail: " << user.email <<
    "\nSenha: " << user.senha <<
    "\nTelefone: " << user.telefone <<
    "\nCidade: " << user.cidade <<
    "\nBairro: " << user.bairro <<
    "\nCEP: " << user.cep << 
    "\nEmpresa vinculada: " << user.empresa << 
    "\nCargo: " << user.cargo << 
    "\nEmail institucional: " << user.email_inst << 
    "\nCNPJ: " << user.cnpj << 
    "\nTipo: G"<< "\n\n";

    arq.close();
}

int busca_cadastro(string cpf){

    ifstream arq("registro_usuarios.txt");
    string linha;
    
    int cont = 0;

    // percorre o arquivo
    while (getline(arq, linha)) {

        cont++;

        // se encontrou o cpf na linha retorna a posição - 1 (inicio do cadastro)
        // o comando find busca uma string na linha
        if (linha.find(cpf) != string::npos) { 
            return cont - 1;
        }
    }
    cout << "\nUsuario nao encontrado no sistema";
    return -1;

    arq.close();
}

bool checa_senha(string cpf, string senha){

    ifstream arq("registro_usuarios.txt");
    string linha;

    int cont = busca_cadastro(cpf);

    // desloca até a linha da senha do cadastro buscado
    for(int i = 0; i < cont + 4; i++){
        getline(arq,linha);
    }

    // checa a linha de senha e confere se a senha bate
    if(linha.find(senha) != string::npos)
        return true;
    else
        return false;

    arq.close();
}

bool checa_cadastro(string cpf, string senha, int tipo) {

    ifstream arq("registro_usuarios.txt");
    string linha;

    int cont = busca_cadastro(cpf);

    // se achar o registro
    if(cont != -1) {

        // checa a senha para cidadãos
        if((checa_senha(cpf, senha) == true) && tipo == 1) {

            for(int i = 0; i < cont + 9; i++) {
                getline(arq, linha);
            }

            //confere se o cadastro esta salvo como cidadadão
            if(linha.find("C") != string::npos) {
                return true;
            } else {
                cout << "\n\033[31mAcesso invalido!\033[0m";
                cout << "\nO usuario nao esta cadastrado como cidadao!";
                return false;
            }

        } else {

            // checa a senha para gerentes
            if((checa_senha(cpf, senha) == true) && tipo == 2) {

                for(int i = 0; i < cont + 13; i++) {
                    getline(arq, linha);
                }
            
                //confere se o cadastro esta salvo como gerente
                if(linha.find("G") != string::npos) {
                    return true;
                } else {
                    cout << "\n\033[31mAcesso invalido!\033[0m";
                    cout << "\nO usuario nao esta cadastrado como gestor!";
                    return false;
                }

            // se a senha esta errada
            } else {
                cout << "\n\033[31mSenha invalida!\033[0m";
                return false;
            }

        }

    // se não achar o registro
    } else {
        return false;
    }

    arq.close();
}

int main(){

    int opcao = -1, opc2;
    string cpf, senha;

    cout << "\n\t\t\033[36mSmartCity Hub\033[0m";
    cout << "\n\n\033[36mInicio\033[0m";
    cout << "\n\n\033[36m1 -\033[0m Entrar como usuario";
    cout << "\n\033[36m2 -\033[0m Entrar como gestor";
    cout << "\n\n\033[36m0 -\033[0m Sair\n\n";
    cin >> opcao;
    cout << "__________________________________________\n\n";

    
    while(opcao < 0 || opcao > 2){
        cout << "\033[31mOpcao errada!\033[0m Tente denovo: ";
        cin >> opcao;
    }

    switch(opcao){
        
    case 1:

        while(opcao != 0){

            cout << "\n\033[36m1.\033[0mInserir cadastro";
            cout << "\n\033[36m2.\033[0mCadastrar-se";

            cout << "\n\n\033[36m0.\033[0mSair\n\n";
            cin >> opcao;

            // comando que limpa o buffer de entrada do cin, removendo o '\n' que sobra, usado pra não atrapalhar o getline
            cin.ignore(numeric_limits<streamsize>::max(), '\n');

            cout << "__________________________________________\n\n";

            switch(opcao){
                case 1:

                    cout << "\nInsira seu cpf: ";
                    cin >> cpf;
                    cout << "\n\033[36m1.\033[0mInserir senha";
                    cout << "\n\033[36m2.\033[0mEsqueci minha senha\n\n";
                    cin >> opc2;

                    if(opc2 == 1){
                        cout << "\nSenha: ";
                        cin >> senha;
                    }
                    else{
                        cout << "\nEnviaremos um email para a alteracao de senha.";
                        break;
                    }

                    if(checa_cadastro(cpf,senha,1) == true){
                        cout << "__________________________________________\n";
                        cout << "\n\033[36mSeja bem vindo!\033[0m";
                        opcao = 0;
                    }
                    break;

                case 2:

                    cadastro_usuario_cidadao();
                    break;

                default:
                    if(opcao != 0)
                        cerr << "\033[31mComando errado\033[0m";
                    break;
                }

            if(opcao != 0)
                cout << "\n__________________________________________\n";                
        }

    case 2:

        while(opcao != 0){

            cout << "\n\033[36m1.\033[0mInserir cadastro";
            cout << "\n\033[36m2.\033[0mCadastrar-se";

            cout << "\n\n\033[36m0.\033[0mSair\n\n";
            cin >> opcao;
            cin.ignore(numeric_limits<streamsize>::max(), '\n');

            cout << "__________________________________________\n\n";

            switch(opcao){
                case 1:

                    cout << "\nInsira seu cpf: ";
                    cin >> cpf;
                    cout << "\n\033[36m1.\033[0mInserir senha";
                    cout << "\n\033[36m2.\033[0mEsqueci minha senha\n\n";
                    cin >> opc2;

                    if(opc2 == 1){
                        cout << "\nSenha: ";
                        cin >> senha;
                    }
                    else{
                        cout << "\nEnviaremos um email para a alteracao de senha.";
                        break;
                    }

                    if(checa_cadastro(cpf,senha,2) == true){
                        cout << "__________________________________________\n\n";
                        cout << "\033[36mSeja bem vindo!\033[0m";
                        opcao = 0;
                    }
                    break;

                case 2:

                    cadastro_gerente();
                    cout << "\nCadastro realizado com sucesso!";
                    break;

                default:
                    if(opcao != 0)
                        cerr << "\033[31mComando errado\033[0m";
                    break;
                }

                if(opcao != 0)
                    cout << "\n__________________________________________\n";                
    
                }
            }

    }

