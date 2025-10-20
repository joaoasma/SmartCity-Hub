#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <chrono>
#include <string>
#include <mutex>
#include <cstdlib>
#include <ctime>
#include <atomic>

using namespace std;

mutex mtx;

struct Semaforo {
    string direcao;
    int tempoInicial;
    atomic<int> carrosPassaram;

    // Construtor padrão
    Semaforo(string d = "", int t = 0)
        : direcao(d), tempoInicial(t), carrosPassaram(0) {}

    // Impede cópia, mas permite movimento
    Semaforo(const Semaforo&) = delete;
    Semaforo& operator=(const Semaforo&) = delete;
    Semaforo(Semaforo&& other) noexcept {
        direcao = move(other.direcao);
        tempoInicial = other.tempoInicial;
        carrosPassaram.store(other.carrosPassaram.load());
    }
    Semaforo& operator=(Semaforo&& other) noexcept {
        if (this != &other) {
            direcao = move(other.direcao);
            tempoInicial = other.tempoInicial;
            carrosPassaram.store(other.carrosPassaram.load());
        }
        return *this;
    }
};

// Limpa o terminal
void limpar() {
    system("clear");
}

void simularSemaforo(Semaforo &s) {
    const int verde = 25;
    const int amarelo = 5;
    const int vermelho = 30;
    const int ciclo = verde + amarelo + vermelho;

    this_thread::sleep_for(chrono::seconds(s.tempoInicial));
    int tempo = 0;

    while (true) {
        int fase = tempo % ciclo;
        string cor;

        if (fase < verde) cor = "VERDE";
        else if (fase < verde + amarelo) cor = "AMARELO";
        else cor = "VERMELHO";

        mtx.lock();
        limpar();
        cout << "=== Simulacao dos semaforos ===" << endl;
        cout << "[ " << s.direcao << " ] -> " << cor
             << " (" << fase << "s)" << endl;
        cout << "Carros que passaram nesta hora: " << s.carrosPassaram.load() << endl;
        mtx.unlock();

        if (cor == "VERDE") {
            int carros = rand() % 5;
            s.carrosPassaram += carros;
        }

        this_thread::sleep_for(chrono::seconds(1));
        tempo++;
    }
}

void monitorarCarros(vector<Semaforo> &semaforos) {
    while (true) {
        this_thread::sleep_for(chrono::hours(1));

        mtx.lock();
        cout << "\n===== RELATORIO DE FLUXO DE CARROS (última hora) =====\n";
        for (auto &s : semaforos) {
            cout << s.direcao << ": " << s.carrosPassaram.load() << " carros" << endl;
            s.carrosPassaram = 0;
        }
        cout << "=====================================================\n";
        mtx.unlock();
    }
}

int main() {
    srand(time(0));

    vector<Semaforo> semaforos;
    ifstream arquivo("semaforos.txt");

    if (!arquivo) {
        cerr << "Erro ao abrir semaforos.txt\n";
        return 1;
    }

    string direcao;
    while (getline(arquivo, direcao)) {
        if (direcao.empty()) continue;

        int tempoInicial = (direcao == "Leste" || direcao == "Oeste") ? 30 : 0;
        semaforos.emplace_back(direcao, tempoInicial);
    }

    cout << "Iniciando simulacao dos semaforos...\n";
    this_thread::sleep_for(chrono::seconds(2));

    vector<thread> threads;
    for (auto &s : semaforos)
        threads.emplace_back(simularSemaforo, ref(s));

    thread monitor(monitorarCarros, ref(semaforos));

    for (auto &t : threads)
        t.join();

    monitor.join();
    return 0;
}

