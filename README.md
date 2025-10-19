# 🏙️ SMARTHUB CITY - Plataforma de Cidade Inteligente

## 📋 Descrição do Projeto
O **SmartCity Hub** é uma plataforma integrada de monitoramento urbano desenvolvida na disciplina de Engenharia de Software. O sistema simula sensores IoT para coleta de dados ambientais e de infraestrutura, disponibilizando informações em tempo real através de dashboards interativos para cidadãos e gestores públicos.

## 🎯 Objetivo
Centralizar dados de sensores IoT espalhados pela cidade, oferecer serviços digitais à população e apoiar a tomada de decisão por parte dos gestores públicos, promovendo transparência e eficiência na gestão urbana.

## 📁 Estrutura do Projeto

```
SMARTHUB CITY
 │
 ├── Executáveis
 │    ├── Protótipo de Aplicativo
 │    │    ├── app.py
 │    │    └── README.md              
 │    ├── Parte do usuário
 │    │    ├── cadastro.cpp
 │    │    ├── README-cadastro.md
 │    │    ├── reclamações.cpp
 │    │    └── README-reclamações.md
 │    ├── Sensores
 │    │    ├── ...arquivos.cpp
 │    │    ├── ...arquivos.txt
 │    │    └── ...readme's.md
 │    ├── Gráficos
 │    │    ├── dashboard.py
 │    │    ├── bibliotecas.txt
 │    │    └── README.md
 │    └── Testes
 │         ├── load_generator.cpp
 │         └── carga.txt
 │ 
 ├── Apresentação
 │    └── Slides.pdf
 │
 └── Documentação
      ├── Diagramas Casos de Uso.png
      └── Qualidade e Riscos.pdf
```

## 🚀 Funcionalidades Principais

### 📊 Dashboard de Monitoramento
- **Qualidade do Ar (AQI)**: Monitoramento em tempo real
- **Nível de Ruído (dB)**: Medição de poluição sonora
- **Consumo de Energia (kWh)**: Acompanhamento energético
- **Tráfego Veicular**: Volume de veículos por hora
- **Alertas Inteligentes**: Notificações baseadas em limites

### 🚦 Sistemas de Sensores Simulados
- **Semáforos Inteligentes**: Otimização de fluxo veicular
- **Coleta de Lixo Inteligente**: Sensores IoT em lixeiras
- **Dados Circadianos**: Padrões realistas de comportamento urbano

### 👥 Módulo do Cidadão
- **Cadastro de Usuários**: Diferentes perfis (cidadão, gestor, técnico)
- **Sistema de Reclamações**: Reporte de problemas urbanos
- **Aplicativo Web**: Interface acessível para população

## 🛠 Tecnologias Utilizadas

### Backend & Sensores
- **C++**: Sistemas de semáforos e coleta de lixo
- **Multithreading**: Simulação simultânea de sensores
- **Arquivos de Configuração**: `.txt` para parâmetros dos sistemas

### Dashboard & Visualização
- **Python 3.11+**: Linguagem principal
- **Streamlit**: Framework web para dashboard
- **Plotly**: Gráficos interativos e em tempo real
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Cálculos numéricos e simulações

## ⚡ Como Executar

### Pré-requisitos
```bash
Python 3.11+
pip install streamlit pandas plotly numpy
Compilador C++ (g++/clang++)
```

### Dashboard Principal
```bash
cd Executáveis/Gráficos
streamlit run dashboard.py
```

### Sistemas de Sensores
```bash
cd Executáveis/Sensores
g++ -std=c++11 -pthread semaforos_inteligentes.cpp -o semaforos
./semaforos
```

## 📈 Métricas Monitoradas

| Sensor | Unidade | Limites |
|--------|---------|---------|
| Qualidade do Ar | AQI | 0-50 (Bom), 51-60 (Moderado), 61+ (Ruim) |
| Nível de Ruído | dB | ≤65 (Aceitável), 66-75 (Alerta), 76+ (Perigoso) |
| Consumo de Energia | kWh | Monitoramento contínuo |
| Tráfego Veicular | v/h | Volume por hora |

## 🎓 Contexto Acadêmico
Projeto desenvolvido para a disciplina de **Engenharia de Software**, demonstrando o ciclo completo de desenvolvimento:
- Engenharia de Requisitos
- Arquitetura de Software
- Implementação (MVP)
- Testes e Qualidade
- Documentação

## 👨‍💻 Autores
- **Alisson Guilherme Ferreira Silva Soares**
- **Felipe Vilela de Oliveira**
- **Hugo Soares Lopes**
- **João Antônio de Souza Martins**
- **Lucas Freire Mesquita**
- **Otavio Augusto Miguel**
- **Petronio Dias de Carvalho Junior**

*Equipe de Desenvolvimento - SmartCity Hub*

## 📄 Licença
Projeto acadêmico para fins educacionais.

---

**🏙️ SmartCity Hub - Transformando dados em decisões inteligentes para cidades mais eficientes e transparentes.**
