# Dashboard de Monitoramento - Cidade Inteligente

## Sobre o Projeto
Dashboard interativo em tempo real para monitoramento urbano da cidade de Alfenas. Desenvolvido por João Antonio de Souza Martins usando Python 3.11.9 no Visual Studio Code.

## Arquivos do Projeto
- dashboard.py (arquivo principal)
- bibliotecas.txt (lista de dependências)

## Como Executar

### Instalação das Dependências
```bash
pip install -r bibliotecas.txt
```

### Executar o Dashboard
```bash
streamlit run dashboard.py
```

### Acessar no Navegador
O sistema abrirá automaticamente em: http://localhost:8501

## Funcionalidades do Dashboard

### 1. Métricas em Tempo Real
- **Qualidade do Ar (AQI)**: Mede a poluição do ar - valores baixos indicam ar mais limpo
- **Nível de Ruído (dB)**: Mede o barulho ambiental - decibéis que afetam a qualidade de vida
- **Consumo de Energia (kWh)**: Monitora uso de energia - quilowatt-hora consumidos
- **Tráfego Veicular (v/h)**: Conta veículos por hora - indica congestionamentos

### 2. Sistema de Alertas Inteligente
- Alertas vermelhos quando valores ultrapassam limites perigosos
- Avisos laranja para situações de atenção
- Status verde quando tudo está normal

### 3. Gráficos Interativos
- Visualização das últimas 24 horas em tempo real
- Comparação entre diferentes métricas
- Análise de tendências temporais
- Gráficos individuais para cada tipo de dado

### 4. Filtros e Controles
- Seletor de horário para analisar períodos específicos
- Atualização manual dos dados simulados
- Informações meteorológicas em tempo real

### 5. Interface Profissional
- Design moderno com cores gradientes
- Layout responsivo e intuitivo
- Cartões coloridos indicando status
- Navegação por abas organizada

## Significado das Unidades de Medida

### Qualidade do Ar (AQI - Air Quality Index)
- **0-50**: BOA - Ar satisfatório, risco mínimo
- **51-60**: MODERADA - Aceitável, mas pode afetar pessoas sensíveis
- **61+**: RUIM - Pode causar efeitos à saúde pública

### Nível de Ruído (dB - Decibéis)
- **Até 65 dB**: ACEITÁVEL - Conversação normal, ambiente tranquilo
- **66-75 dB**: ALERTA - Tráfego moderado, pode causar incômodo
- **76+ dB**: PERIGOSO - Tráfego intenso, risco para audição

### Consumo de Energia (kWh - Quilowatt-hora)
- Unidade que mede consumo de energia elétrica
- 1 kWh = energia de 1000 watts usada por 1 hora
- Valores altos indicam maior demanda energética

### Tráfego Veicular (v/h - Veículos por hora)
- Mede a intensidade do fluxo de carros
- Valores altos indicam congestionamento
- Valores baixos indicam tráfego fluido

## Padrões de Comportamento dos Dados

### Qualidade do Ar
- PIORA: 6h-10h e 18h-20h (horários de pico)
- MELHORA: 14h-16h (ventos fortes, menos carros)

### Nível de Ruído
- MAIS ALTO: 7h-9h e 17h-19h (horário de rush)
- MAIS BAIXO: 2h-5h (madrugada silenciosa)

### Consumo de Energia
- PICOS: 18h-21h (pessoas chegando em casa)
- VALES: 3h-6h (madrugada, menor consumo)

### Tráfego Veicular
- CONGESTIONAMENTO: 7h-9h e 17h-19h
- TRÁFEGO LIVRE: 1h-5h

## Como Navegar no Dashboard

1. **Métricas Principais**: Olhe os 4 cartões coloridos no topo
2. **Gráficos Comparativos**: Veja as relações entre as métricas
3. **Abas Individuais**: Clique nas abas para detalhes de cada métrica
4. **Filtros**: Use a barra lateral para selecionar horários
5. **Alertas**: Fique atento aos avisos automáticos que aparecem

## Tecnologias Utilizadas
- Python 3.11.9
- Streamlit (interface web)
- Pandas (manipulação de dados)
- Plotly (gráficos interativos)
- NumPy (cálculos matemáticos)

## Dicas de Uso
- Use o botão "Atualizar Dados" para gerar novas simulações
- Arraste o seletor de horário para analisar períodos específicos
- Observe as cores dos cartões para verificar rapidamente o status
- Os alertas aparecem automaticamente quando necessário

Este projeto simula um sistema real de monitoramento urbano, perfeito para estudos de cidades inteligentes e análise de dados ambientais.