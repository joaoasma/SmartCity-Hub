#include <iostream>
#include <fstream>
#include <string>
using namespace std;

string tipo_reclamacao(int opcao){
    string tipos[]{
        "Sair", "Problema com o APP", "Monitoramento de Sensores", "Semaforos","Iluminacao Publica",
        "Coleta de Lixo", "Transporte", "Seguranca", "Acidente", "Outro"
    };

    return tipos[opcao];
}

void cria_reclamacao(int opcao){
    ofstream arq("reclamacoes.txt", ios::app);
    if(!arq.is_open()){
        cout << "\033[31mFalha no Sistema, tente novamente em alguns minutos...\033[0m\n";
        return;
    }

    string comentario;

    cout << "\n\033[32mReintegramos o compromisso com sua privacidade! Suas informacoes pessoais nao serao compartilhadas.\033[0m\n";
    cout << "Digite aqui a sua reclamacao\nR:";

    cin.ignore();
    getline(cin, comentario);

    arq << tipo_reclamacao(opcao) << "\n" << comentario << "\n\n";

    cout << "\n\033[32mSua reclamacao foi enviada para o orgao responsavel. Agradecemos a sua contribuicao.\033[0m";

    arq.close();
}

int main(){
    int opcao = -1;

    cout << "              \033[45mSeja bem-vindo(a) ao Portal de Reclamacoes\033[0m\n";
    
    while(opcao < 0 || opcao > 9){                         
        cout << "_______________________________________________________________________\n";
        cout << "\nQual o assunto da sua reclamacao? (Selecione o numero correspondente)\n";
        cout << "\033[34m1.\033[0m Problema com o APP\n\033[34m2.\033[0m Monitoramento de Sensores\n\033[34m3.\033[0m Semaforos\n";
        cout << "\033[34m4.\033[0m Iluminacao Publica\n\033[34m5.\033[0m Coleta de Lixo\n\033[34m6.\033[0m Transporte\n\033[34m7.\033[0m Seguranca\n";
        cout << "\033[34m8.\033[0m Acidente\n\033[34m9.\033[0m Outro\n\033[34m0.\033[0m Sair\nR: ";
        cin >>  opcao;
        if(opcao < 0 || opcao > 9){
            cout << "\n\033[31mERRO! Digite uma opcao VALIDA\033[0m\n";
        }
    }

    if(opcao != 0){
        cria_reclamacao(opcao);
    } else{
        cout << "\033[47mSaindo do Sistema...\033[0m";
    }


    return 0;
}


