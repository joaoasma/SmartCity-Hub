#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <random>

using namespace std;

string tipo_reclamacao(int opcao){
    string tipos[]{
        "Sair", "Problema com o APP", "Monitoramento de Sensores", "Semaforos",
        "Iluminacao Publica", "Coleta de Lixo", "Transporte", "Seguranca",
        "Acidente", "Outro"
    };
    if(opcao < 0) opcao = 0;
    if(opcao > 9) opcao = 9;
    return tipos[opcao];
}

int main(int argc, char** argv){
    // N = número de eventos (padrão 50000). Pode passar como primeiro argumento.
    long N = 50000;
    if(argc > 1){
        try { N = stol(argv[1]); } catch(...) { /* mantém padrão */ }
    }

    const string arquivo = "reclamacoes_test.txt"; // arquivo de teste (não mexe no original)
    mt19937_64 rng((unsigned)chrono::high_resolution_clock::now().time_since_epoch().count());
    uniform_int_distribution<int> tipo(1,9); // usa 1..9 como no menu do seu programa

    auto t0 = chrono::high_resolution_clock::now();
    ofstream out(arquivo, ios::app);
    if(!out){
        cerr << "Erro ao abrir arquivo: " << arquivo << '\n';
        return 1;
    }

    for(long i = 0; i < N; ++i){
        int tp = tipo(rng);
        string comentario = "Evento_simulado_" + to_string(i);
        // grava no MESMO formato do seu programa: tipo_string \n comentario \n\n
        out << tipo_reclamacao(tp) << "\n" << comentario << "\n\n";
        // opcional: se quiser flush a cada X registros (descomente)
        // if(i % 10000 == 0) out.flush();
    }
    out.close();
    auto t1 = chrono::high_resolution_clock::now();
    double secs = chrono::duration<double>(t1 - t0).count();
    cout << "Gerados " << N << " eventos em " << secs << " s -> " << (N / secs) << " ev/s\n";
    cout << "Arquivo: " << arquivo << '\n';
    return 0;
}
