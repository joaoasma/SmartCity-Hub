#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <chrono>
#include <string>
#include <cstdlib>
#include <ctime>

using namespace std;

struct Lixeira {
    string nome;
    bool coletada = false;
    bool sensorAtivado = false;
};

// Função para limpar a tela
void limpar() {
    system("clear");
}

// Função que simula o sensor da lixeira
void ativarSensor(Lixeira &lixeira) {
    lixeira.sensorAtivado = true;
    lixeira.coletada = true;
    cout << "[OK] " << lixeira.nome << " coletada com sucesso.\n";
}

// Função que simula a coleta sequencial
void simularColeta(vector<Lixeira> &lixeiras) {
    cout << "=== Simulacao de coleta de lixo inteligente ===\n";
    cout << "Horario de coleta: 6:00h às 6:30h\n\n";

    int tempoTotal = 30; // 30 minutos simulados
    int intervaloPorLixeira = tempoTotal / (int)lixeiras.size(); // minutos por lixeira

    srand(time(0));

    for (int minuto = 0; minuto <= tempoTotal; minuto++) {
        limpar();
        cout << "Hora simulada: 6:" << (minuto < 10 ? "0" : "") << minuto << "h\n\n";

        // Simula a coleta a cada intervalo
        if (minuto % intervaloPorLixeira == 0 && minuto != 0) {
            int indice = (minuto / intervaloPorLixeira) - 1;
            if (indice < (int)lixeiras.size()) {
                // 90% de chance de coletar
                if (rand() % 10 < 9)
                    ativarSensor(lixeiras[indice]);
                else
                    cout << "[ALERTA] " << lixeiras[indice].nome << " não foi coletada!\n";
            }
        }

        // Exibe status de todas as lixeiras
        cout << "\nStatus das lixeiras:\n";
        for (auto &l : lixeiras) {
            cout << "- " << l.nome
                 << " | Sensor: " << (l.sensorAtivado ? "Ativado" : "Desligado")
                 << " | Coleta: " << (l.coletada ? "Sim" : "Não") << "\n";
        }

        this_thread::sleep_for(chrono::milliseconds(800)); // acelera o tempo (0.8s = 1 min)
    }

    cout << "\n=== Fim da coleta ===\n\n";
    for (auto &l : lixeiras) {
        if (!l.coletada)
            cout << "[PROBLEMA] " << l.nome << " não foi coletada!\n";
    }
}

int main() {
    vector<Lixeira> lixeiras;
    ifstream arquivo("lixeiras.txt");

    if (!arquivo) {
        cerr << "Erro ao abrir arquivo lixeiras.txt\n";
        return 1;
    }

    string nome;
    while (getline(arquivo, nome)) {
        if (!nome.empty())
            lixeiras.push_back({nome});
    }

    if (lixeiras.empty()) {
        cerr << "Nenhuma lixeira encontrada no arquivo!\n";
        return 1;
    }

    simularColeta(lixeiras);
    return 0;
}

