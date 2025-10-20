import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuração da página para layout wide
st.set_page_config(
    page_title="Dados da Cidade de Alfenas",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card-good {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .metric-card-warning {
        background: linear-gradient(135deg, #f46b45 0%, #eea849 100%);
    }
    .metric-card-danger {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    }
    .metric-title {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-delta {
        font-size: 0.8rem;
        font-weight: 500;
    }
    .stMetric {
        background-color: transparent !important;
    }
    .weather-info {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Título profissional
st.markdown('<h1 class="main-header">🏙️ Dashboard de Monitoramento - Cidade Inteligente</h1>', unsafe_allow_html=True)

# Gerar dados mais realistas com padrão de 24 horas
def generate_sensor_data():
    # Gerar 24 horas de dados, da hora atual até 24 horas atrás
    now = datetime.now()
    timestamps = [now - timedelta(hours=i) for i in range(24, -1, -1)]  # Invertido para mostrar do mais antigo ao mais recente
    
    # Ordenar do mais antigo para o mais recente
    timestamps.sort()
    
    time_of_day = [t.hour for t in timestamps]
    
    # Dados mais realistas com padrões circadianos
    aqi = [45 + 8 * np.sin(2 * np.pi * (h-6)/24) + np.random.normal(0, 2) for h in time_of_day]
    noise = [58 + 10 * np.sin(2 * np.pi * (h-12)/24) + np.random.normal(0, 3) for h in time_of_day]
    energy = [110 + 40 * np.sin(2 * np.pi * (h-18)/24) + np.random.normal(0, 8) for h in time_of_day]
    traffic = [300 + 250 * np.sin(2 * np.pi * (h-8)/24) + np.random.normal(0, 30) for h in time_of_day]
    
    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Hora": [t.strftime("%H:%M") for t in timestamps],
        "Data_Hora": [t.strftime("%d/%m %H:%M") for t in timestamps],
        "Qualidade do Ar (AQI)": [max(30, min(80, x)) for x in aqi],
        "Nível de Ruído (dB)": [max(45, min(85, x)) for x in noise],
        "Consumo de Energia (kWh)": [max(80, min(200, x)) for x in energy],
        "Tráfego (veículos/h)": [max(50, min(800, x)) for x in traffic]
    })
    
    return df

# Simular dados de clima
def get_weather_data():
    now = datetime.now()
    # Simular temperatura baseada na hora do dia
    base_temp = 22 + 8 * np.sin(2 * np.pi * (now.hour - 14)/24)
    temperature = max(15, min(35, base_temp + np.random.normal(0, 2)))
    
    # Condições climáticas baseadas na hora e aleatoriedade
    conditions = ["Ensolarado", "Parcialmente Nublado", "Nublado", "Chuvoso Leve", "Tempestuoso"]
    weights = [0.3, 0.25, 0.2, 0.15, 0.1]
    
    # Mais chance de sol durante o dia
    if 6 <= now.hour <= 18:
        weights = [0.4, 0.3, 0.15, 0.1, 0.05]
    else:  # Noite
        weights = [0.1, 0.2, 0.4, 0.2, 0.1]
    
    condition = np.random.choice(conditions, p=weights)
    
    return {
        "temperature": round(temperature, 1),
        "condition": condition,
        "humidity": np.random.randint(40, 85),
        "wind_speed": np.random.uniform(0, 15)
    }

# Inicializar dados na session state
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = generate_sensor_data()

if 'weather_data' not in st.session_state:
    st.session_state.weather_data = get_weather_data()

df = st.session_state.sensor_data
weather = st.session_state.weather_data

# Sidebar para filtros
st.sidebar.header("🔧 Filtros e Controles")

# Informações de clima na sidebar
st.sidebar.markdown('<div class="weather-info">', unsafe_allow_html=True)
st.sidebar.subheader("🌤️ Condições Atuais")
st.sidebar.write(f"**Hora:** {datetime.now().strftime('%H:%M')}")
st.sidebar.write(f"**Temperatura:** {weather['temperature']}°C")
st.sidebar.write(f"**Clima:** {weather['condition']}")
st.sidebar.write(f"**Umidade:** {weather['humidity']}%")
st.sidebar.write(f"**Vento:** {weather['wind_speed']:.1f} km/h")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Filtro de horário com valores padrão que mostram o dia todo
hour_range = st.sidebar.select_slider(
    "Selecione o período:",
    options=list(range(24)),
    value=(0, 23),
    format_func=lambda x: f"{x:02d}:00"
)

# Filtrar dados baseado na seleção
filtered_df = df[
    (df['Timestamp'].dt.hour >= hour_range[0]) & 
    (df['Timestamp'].dt.hour <= hour_range[1])
]

# Cálculos para métricas
current_aqi = filtered_df['Qualidade do Ar (AQI)'].iloc[-1]
current_noise = filtered_df['Nível de Ruído (dB)'].iloc[-1]
current_energy = filtered_df['Consumo de Energia (kWh)'].iloc[-1]
current_traffic = filtered_df['Tráfego (veículos/h)'].iloc[-1]

# Calcular variações (deltas) - comparando com 1 hora anterior
if len(filtered_df) > 1:
    delta_aqi = current_aqi - filtered_df['Qualidade do Ar (AQI)'].iloc[-2]
    delta_noise = current_noise - filtered_df['Nível de Ruído (dB)'].iloc[-2]
    delta_energy = current_energy - filtered_df['Consumo de Energia (kWh)'].iloc[-2]
    delta_traffic = current_traffic - filtered_df['Tráfego (veículos/h)'].iloc[-2]
else:
    delta_aqi = delta_noise = delta_energy = delta_traffic = 0

# Determinar classes CSS baseado nos valores
aqi_class = "metric-card-good" if current_aqi <= 50 else "metric-card-warning" if current_aqi <= 60 else "metric-card-danger"
noise_class = "metric-card-good" if current_noise <= 65 else "metric-card-warning" if current_noise <= 75 else "metric-card-danger"
energy_class = "metric-card"
traffic_class = "metric-card"

# Métricas principais em colunas
st.subheader("📈 Indicadores em Tempo Real")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="metric-card {aqi_class}">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">QUALIDADE DO AR</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{current_aqi:.1f} AQI</div>', unsafe_allow_html=True)
    st.metric("", "", f"{delta_aqi:+.1f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="metric-card {noise_class}">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">NÍVEL DE RUÍDO</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{current_noise:.1f} dB</div>', unsafe_allow_html=True)
    st.metric("", "", f"{delta_noise:+.1f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="metric-card {energy_class}">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">CONSUMO DE ENERGIA</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{current_energy:.1f} kWh</div>', unsafe_allow_html=True)
    st.metric("", "", f"{delta_energy:+.1f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown(f'<div class="metric-card {traffic_class}">', unsafe_allow_html=True)
    st.markdown('<div class="metric-title">TRÁFEGO VEHICULAR</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{current_traffic:.0f} v/h</div>', unsafe_allow_html=True)
    st.metric("", "", f"{delta_traffic:+.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

# Gráficos principais
st.subheader("📊 Análise Detalhada dos Sensores")

# Dois gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    fig_comparison = go.Figure()
    
    # Adicionar todas as métricas no mesmo gráfico (normalizadas)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    metrics = list(filtered_df.columns[3:7])  # Ajustado para pular Timestamp, Hora e Data_Hora
    
    for i, metric in enumerate(metrics):
        normalized = (filtered_df[metric] - filtered_df[metric].min()) / (filtered_df[metric].max() - filtered_df[metric].min())
        fig_comparison.add_trace(go.Scatter(
            x=filtered_df['Data_Hora'],  # Usar Data_Hora formatada
            y=normalized,
            mode='lines+markers',
            name=metric,
            line=dict(width=3, color=colors[i]),
            marker=dict(size=6)
        ))
    
    fig_comparison.update_layout(
        title='Comparação Normalizada - Últimas 24 Horas',
        xaxis_title='Data e Hora',
        yaxis_title='Valor Normalizado (0-1)',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_comparison, use_container_width=True)

with col2:
    # Gráfico de barras comparativo
    fig_bars = go.Figure(data=[
        go.Bar(name='Mínimo', x=metrics, y=[filtered_df[col].min() for col in metrics], marker_color='#636efa'),
        go.Bar(name='Médio', x=metrics, y=[filtered_df[col].mean() for col in metrics], marker_color='#00cc96'),
        go.Bar(name='Máximo', x=metrics, y=[filtered_df[col].max() for col in metrics], marker_color='#ef553b')
    ])
    
    fig_bars.update_layout(
        title='Comparação: Mínimo, Médio e Máximo',
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_bars, use_container_width=True)

# Gráficos individuais em abas
tab1, tab2, tab3, tab4 = st.tabs(["🌫️ Qualidade do Ar", "🔊 Nível de Ruído", "⚡ Energia", "🚗 Tráfego"])

with tab1:
    fig_air = px.area(
        filtered_df, 
        x="Data_Hora",  # Usar Data_Hora formatada
        y="Qualidade do Ar (AQI)",
        title="Qualidade do Ar - Últimas 24 Horas",
        color_discrete_sequence=['#2E86AB']
    )
    fig_air.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Bom")
    fig_air.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="Moderado")
    fig_air.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Ruim")
    fig_air.update_layout(
        height=400,
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_air, use_container_width=True)

with tab2:
    fig_noise = px.line(
        filtered_df, 
        x="Data_Hora",  # Usar Data_Hora formatada
        y="Nível de Ruído (dB)",
        title="Nível de Ruído - Últimas 24 Horas",
        color_discrete_sequence=['#FFA15A'],
        markers=True
    )
    fig_noise.add_hline(y=65, line_dash="dash", line_color="green", annotation_text="Aceitável")
    fig_noise.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="Alto")
    fig_noise.update_layout(
        height=400,
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_noise, use_container_width=True)

with tab3:
    fig_energy = px.area(
        filtered_df, 
        x="Data_Hora",  # Usar Data_Hora formatada
        y="Consumo de Energia (kWh)",
        title="Consumo de Energia - Últimas 24 Horas",
        color_discrete_sequence=['#00CC96']
    )
    fig_energy.update_layout(
        height=400,
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_energy, use_container_width=True)

with tab4:
    fig_traffic = px.bar(
        filtered_df, 
        x="Data_Hora",  # Usar Data_Hora formatada
        y="Tráfego (veículos/h)",
        title="Volume de Tráfego - Últimas 24 Horas",
        color="Tráfego (veículos/h)",
        color_continuous_scale="Viridis"
    )
    fig_traffic.update_layout(
        height=400,
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_traffic, use_container_width=True)

# Status do sistema
st.subheader("🔍 Status do Sistema")

# Alertas automáticos
alerts = []
if current_aqi > 60:
    alerts.append("🚨 ALERTA: Qualidade do AR acima do limite moderado")
elif current_aqi > 50:
    alerts.append("⚠️ AVISO: Qualidade do AR em nível moderado")

if current_noise > 75:
    alerts.append("🔊 ALERTA: Nível de ruído muito alto")
elif current_noise > 65:
    alerts.append("🔊 AVISO: Nível de ruído elevado")

if current_energy > 180:
    alerts.append("⚡ ALERTA: Alto consumo de energia detectado")

# Alertas baseados no clima
if weather['condition'] == "Tempestuoso":
    alerts.append("⛈️ ALERTA: Condições tempestuosas - monitore os sensores")
elif weather['condition'] == "Chuvoso Leve":
    alerts.append("🌧️ AVISO: Chuva leve - tráfego pode ser afetado")

if alerts:
    for alert in alerts:
        if "ALERTA" in alert:
            st.error(alert)
        else:
            st.warning(alert)
else:
    st.success("✅ Todos os sistemas operando dentro dos parâmetros normais")

# Informações adicionais na sidebar
st.sidebar.subheader("📋 Resumo do Período")
st.sidebar.metric("Horas analisadas", f"{len(filtered_df)}h")
st.sidebar.metric("Qualidade do Ar média", f"{filtered_df['Qualidade do Ar (AQI)'].mean():.1f}")
st.sidebar.metric("Ruído médio", f"{filtered_df['Nível de Ruído (dB)'].mean():.1f} dB")

st.sidebar.subheader("⚙️ Controles")
if st.sidebar.button("🔄 Atualizar Dados"):
    st.session_state.sensor_data = generate_sensor_data()
    st.session_state.weather_data = get_weather_data()
    st.rerun()

# Rodapé
st.markdown("---")
st.markdown(
    "📡 *Sistema de monitoramento em tempo real - Dados simulados para demonstração* • "
    f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} • "
    f"Temperatura: {weather['temperature']}°C • Clima: {weather['condition']}"
)