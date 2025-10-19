# smartcity_hub_com_transicao.py
import customtkinter as ctk
from datetime import datetime
import json
import os
from PIL import Image, ImageTk
import requests
import folium
import webbrowser
from folium.plugins import MarkerCluster, HeatMap
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from openpyxl import Workbook
import tempfile
import random
import threading
import time
import sys

# -------------------------
# Configuração inicial
# -------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Variável global para controlar tela atual
tela_atual = None

janela = ctk.CTk()
janela.title("SmartCity Hub - Login")
janela.geometry("820x540")
janela.resizable(False, False)

# -------------------------
# Arquivos de dados (JSON)
# -------------------------
ARQUIVO_USUARIOS = "usuarios.json"
ARQ_PROBLEMAS = "problemas.json"
ARQUIVO_CACHE = "coordenadas_cache.json"
ARQUIVO_DADOS_CIDADE = "dados_cidade.json"

# Garante existência dos arquivos
for fpath, pad in [(ARQUIVO_USUARIOS, {}), (ARQ_PROBLEMAS, []), (ARQUIVO_CACHE, {}), (ARQUIVO_DADOS_CIDADE, {"eventos": [], "alertas": [], "coleta": {}})]:
    if not os.path.exists(fpath):
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(pad, f, indent=4, ensure_ascii=False)

def carregar_json(arquivo, padrao):
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return padrao
    return padrao

def salvar_json(arquivo, dados):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

usuarios = carregar_json(ARQUIVO_USUARIOS, {})

def salvar_usuarios():
    salvar_json(ARQUIVO_USUARIOS, usuarios)

def carregar_cache():
    return carregar_json(ARQUIVO_CACHE, {})

def salvar_cache(cache):
    salvar_json(ARQUIVO_CACHE, cache)

def carregar_dados_cidade():
    dados = carregar_json(ARQUIVO_DADOS_CIDADE, {"eventos": [], "alertas": [], "coleta": {}})
    if "coleta" not in dados or not dados["coleta"]:
        dados["coleta"] = {
            "Centro": "Segunda, Quarta e Sexta - 07h às 10h",
            "Jardim Aeroporto": "Terça e Quinta - 08h às 11h",
            "Bairro Bárbaras": "Segunda e Quinta - 09h às 11h",
            "Balsa da Harmonia": "Quarta e Sexta - 10h às 12h"
        }
        salvar_json(ARQUIVO_DADOS_CIDADE, dados)
    return dados

def salvar_dados_cidade(dados):
    salvar_json(ARQUIVO_DADOS_CIDADE, dados)

# -------------------------
# Sistema de gerenciamento de telas
# -------------------------
def mostrar_tela(nova_tela_func, *args, **kwargs):
    """Remove a tela atual e mostra uma nova tela na janela principal"""
    global tela_atual
    
    # Remove a tela atual se existir
    if tela_atual:
        try:
            tela_atual.destroy()
        except:
            pass
    
    # Cria nova tela
    tela_atual = nova_tela_func(*args, **kwargs)
    tela_atual.pack(fill="both", expand=True)  # CORREÇÃO: Adiciona pack aqui
    return tela_atual

def voltar_para_dashboard(usuario, tipo):
    """Volta para o dashboard principal"""
    mostrar_tela(criar_tela_dashboard, usuario, tipo)

# -------------------------
# Mensagens estilizadas
# -------------------------
def mostrar_mensagem(titulo, texto, tipo="info"):
    cores = {
        "info": ("#3B8ED0", "ℹ️"),
        "erro": ("#B22222", "❌"),
        "sucesso": ("#2E8B57", "✅"),
        "aviso": ("#DAA520", "⚠️")
    }
    cor, icone = cores.get(tipo, ("#3B8ED0", "ℹ️"))

    popup = ctk.CTkToplevel(janela)
    popup.title(titulo)
    popup.geometry("380x200")
    popup.resizable(False, False)
    popup.grab_set()
    popup.configure(fg_color="#111214")
    
    popup.attributes("-alpha", 0.95)
    popup.transient(janela)

    frame_msg = ctk.CTkFrame(popup, corner_radius=12)
    frame_msg.pack(expand=True, fill="both", padx=12, pady=12)

    ctk.CTkLabel(frame_msg, text=icone, font=("Segoe UI Emoji", 28)).pack(pady=(8, 4))
    ctk.CTkLabel(frame_msg, text=texto, wraplength=340, font=("Segoe UI", 12)).pack(pady=(0, 12))
    
    def fechar_popup():
        try:
            popup.destroy()
        except:
            pass
            
    ctk.CTkButton(frame_msg, text="OK", fg_color=cor, hover_color="#1E90FF", command=fechar_popup).pack()

# -------------------------
# Dados de transporte (estáticos)
# -------------------------
horarios_linhas = {
    "Alfenas → Fama": ["06:50", "10:05", "12:20", "15:20", "17:40", "22:30"],
    "Jardim Aeroporto → Centro": ["06:15", "07:15", "08:15", "11:15", "12:15", "13:15", "16:15", "17:15", "18:15"],
    "Centro → Balsa da Harmonia": ["06:30", "16:30"],
    "Centro → Bairro Bárbaras": ["07:30", "17:30"],
}

rotas_coords = {
    "Alfenas → Fama": [(-21.4258, -45.9477), (-21.4088, -45.8280)],
    "Jardim Aeroporto → Centro": [(-21.4200, -45.9300), (-21.4258, -45.9477)],
    "Centro → Balsa da Harmonia": [(-21.4258, -45.9477), (-21.4400, -45.9600)],
    "Centro → Bairro Bárbaras": [(-21.4258, -45.9477), (-21.4300, -45.9550)],
}

# -------------------------
# Funções de transição / animação (fade) - VERSÃO SEGURA
# -------------------------
def fade_in_seguro(win, interval=0.02, step=0.08):
    """Versão segura do fade_in com verificações"""
    try:
        if not win.winfo_exists():
            return
        win.attributes("-alpha", 0.0)
    except Exception:
        return
        
    def _in():
        alpha = 0.0
        while alpha < 1.0:
            try:
                if not win.winfo_exists():
                    break
                alpha += step
                if alpha > 1.0:
                    alpha = 1.0
                win.attributes("-alpha", alpha)
            except Exception:
                break
            time.sleep(interval)
    threading.Thread(target=_in, daemon=True).start()

# -------------------------
# Funções de mapa
# -------------------------
def abrir_mapa_folium(linha):
    if linha not in rotas_coords:
        mostrar_mensagem("Erro", f"Rota '{linha}' não encontrada.", "erro")
        return

    inicio, fim = rotas_coords[linha]
    url = f"http://router.project-osrm.org/route/v1/driving/{inicio[1]},{inicio[0]};{fim[1]},{fim[0]}?overview=full&geometries=geojson"

    try:
        resp = requests.get(url, timeout=12)
        resp.raise_for_status()
        dados = resp.json()
        coords = dados["routes"][0]["geometry"]["coordinates"]
        rota_convertida = [(lat, lon) for lon, lat in coords]

        m = folium.Map(location=[inicio[0], inicio[1]], zoom_start=13, tiles="CartoDB positron")
        folium.PolyLine(rota_convertida, color="#1E90FF", weight=5, opacity=0.9).add_to(m)
        folium.Marker(rota_convertida[0], tooltip="Início", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker(rota_convertida[-1], tooltip="Fim", icon=folium.Icon(color="red")).add_to(m)

        nome_arquivo = os.path.abspath("mapa_rota.html")
        m.save(nome_arquivo)
        webbrowser.open(f"file:///{nome_arquivo.replace(os.sep, '/')}")

    except Exception as e:
        mostrar_mensagem("Erro", f"Falha ao gerar mapa: {e}", "erro")

def gerar_mapa_html(problemas, filename=None, tiles="CartoDB.Positron", heatmap=False):
    if filename is None:
        filename = os.path.join(tempfile.gettempdir(), "mapa_ocorrencias_alfenas.html")

    mapa = folium.Map(location=[-21.4258, -45.9477], zoom_start=13, tiles=tiles)

    fg_pendente = folium.FeatureGroup(name="Pendente")
    fg_andamento = folium.FeatureGroup(name="Em andamento")
    fg_resolvido = folium.FeatureGroup(name="Resolvido")

    cluster_pend = MarkerCluster(name="Pendentes").add_to(fg_pendente)
    cluster_and = MarkerCluster(name="Em andamento").add_to(fg_andamento)
    cluster_res = MarkerCluster(name="Resolvidos").add_to(fg_resolvido)

    heat_data = []
    cache = carregar_cache()

    icones = {
        "Iluminação Pública": "⚡",
        "Buraco na rua": "🕳️",
        "Lixo acumulado": "🗑️",
        "Semáforo quebrado": "🚦",
        "Outros": "❓"
    }

    for p in problemas:
        local = p.get("localizacao", "")
        if not local or local == "Não informada":
            continue
        try:
            if local in cache:
                lat, lon = cache[local]
            else:
                url = f"https://nominatim.openstreetmap.org/search?format=json&q={local}, Alfenas, MG, Brasil"
                resp = requests.get(url, headers={"User-Agent": "SmartCityHub"}, timeout=8)
                dados = resp.json()
                if not dados:
                    continue
                lat, lon = float(dados[0]["lat"]), float(dados[0]["lon"])
                cache[local] = (lat, lon)
                salvar_cache(cache)

            tipo = p.get('tipo', 'Outros')
            icone = icones.get(tipo, "❓")
            status = p.get('status', 'Desconhecido')

            popup_html = f"""
            <b>{icone} {tipo}</b><br>
            <b>Status:</b> {status}<br>
            <b>Descrição:</b> {p.get('descricao','')}<br>
            <i>{p.get('localizacao','')}</i>
            """

            popup = folium.Popup(popup_html, max_width=300)
            color = {"Pendente": "red", "Em andamento": "orange", "Resolvido": "green"}.get(status, "gray")

            if status == "Pendente":
                folium.CircleMarker([lat, lon], radius=7, popup=popup, color=color, fill=True, fill_color=color).add_to(cluster_pend)
            elif status == "Em andamento":
                folium.CircleMarker([lat, lon], radius=7, popup=popup, color=color, fill=True, fill_color=color).add_to(cluster_and)
            else:
                folium.CircleMarker([lat, lon], radius=7, popup=popup, color=color, fill=True, fill_color=color).add_to(cluster_res)

            heat_data.append([lat, lon])

        except Exception as e:
            continue

    fg_pendente.add_to(mapa)
    fg_andamento.add_to(mapa)
    fg_resolvido.add_to(mapa)

    if heatmap and heat_data:
        HeatMap(heat_data, radius=18, blur=25, min_opacity=0.4).add_to(mapa)

    folium.LayerControl(collapsed=False).add_to(mapa)

    mapa.save(filename)
    return filename

# -------------------------
# Exportar Excel
# -------------------------
def exportar_relatorio_excel(filename="relatorio_ocorrencias.xlsx", problemas=None):
    if problemas is None:
        problemas = carregar_json(ARQ_PROBLEMAS, [])
    if not problemas:
        mostrar_mensagem("Exportar", "Nenhuma ocorrência para exportar.", "aviso")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Ocorrencias"
    headers = ["id", "usuario", "tipo", "descricao", "data", "localizacao", "status"]
    ws.append(headers)
    for p in problemas:
        ws.append([p.get(h, '') for h in headers])

    try:
        wb.save(filename)
        mostrar_mensagem("Exportado", f"Relatório salvo: {filename}", "sucesso")
    except Exception as e:
        mostrar_mensagem("Erro", f"Falha ao salvar relatório: {e}", "erro")

# -------------------------
# Inicialização de Dados de Teste
# -------------------------
def inicializar_dados_teste():
    """Inicializa o banco de dados com dados de teste"""
    
    # 1. INICIALIZAR USUÁRIOS
    usuarios_teste = {
        "gestor@alfenas": {"senha": "123", "tipo": "Gestor"},
        "tecnico@alfenas": {"senha": "123", "tipo": "Técnico"},
        "joao.silva": {"senha": "123", "tipo": "Cidadão"},
        "maria.oliveira": {"senha": "123", "tipo": "Cidadão"},
        "carlos.souza": {"senha": "123", "tipo": "Cidadão"},
        "ana.rodrigues": {"senha": "123", "tipo": "Cidadão"}
    }
    
    # Atualiza os usuários existentes sem sobrescrever completamente
    usuarios_atual = carregar_json(ARQUIVO_USUARIOS, {})
    usuarios_atual.update(usuarios_teste)
    salvar_json(ARQUIVO_USUARIOS, usuarios_atual)
    
    # 2. INICIALIZAR OCORRÊNCIAS DE TESTE
    ocorrencias_teste = [
        {
            "id": 1,
            "usuario": "joao.silva",
            "tipo": "Buraco na rua",
            "descricao": "Buraco grande na Avenida Machado de Assis, próximo ao número 250",
            "data": "2024-01-15 09:30",
            "localizacao": "Avenida Machado de Assis, 250, Centro",
            "status": "Pendente"
        },
        {
            "id": 2,
            "usuario": "maria.oliveira",
            "tipo": "Iluminação Pública",
            "descricao": "Poste de luz queimado na Rua das Flores, altura do número 150",
            "data": "2024-01-16 14:20",
            "localizacao": "Rua das Flores, 150, Jardim Aeroporto",
            "status": "Em andamento"
        },
        {
            "id": 3,
            "usuario": "carlos.souza",
            "tipo": "Lixo acumulado",
            "descricao": "Acúmulo de lixo e entulho no terreno baldio da Rua Bárbaras",
            "data": "2024-01-17 11:45",
            "localizacao": "Rua Bárbaras, 340, Bairro Bárbaras",
            "status": "Pendente"
        },
        {
            "id": 4,
            "usuario": "ana.rodrigues",
            "tipo": "Semáforo quebrado",
            "descricao": "Semáforo não funciona no cruzamento da Avenida Principal com Rua Harmonia",
            "data": "2024-01-18 08:15",
            "localizacao": "Avenida Principal com Rua Harmonia, Balsa da Harmonia",
            "status": "Resolvido"
        }
    ]
    
    # Verifica se já existem ocorrências para não duplicar
    ocorrencias_existentes = carregar_json(ARQ_PROBLEMAS, [])
    if not ocorrencias_existentes:
        salvar_json(ARQ_PROBLEMAS, ocorrencias_teste)
    
    # 3. INICIALIZAR EVENTOS E ALERTAS
    dados_cidade_teste = {
        "eventos": [
            {
                "titulo": "Feira de Artesanato Municipal",
                "data": "27/01/2024",
                "local": "Praça Getúlio Vargas - Centro",
                "descricao": "Feira tradicional com artesanato local, comidas típicas e apresentações culturais. Das 08h às 18h."
            },
            {
                "titulo": "Festival de Música de Alfenas",
                "data": "10/02/2024 a 15/02/2024",
                "local": "Parque Municipal - Jardim Aeroporto",
                "descricao": "Festival com bandas locais e regionais. Ingressos à venda na Secretaria de Cultura."
            }
        ],
        "alertas": [
            {
                "titulo": "Interdição de Rua para Obras",
                "data": "22/01/2024 a 26/01/2024",
                "local": "Rua Bárbaras, entre números 300 e 400",
                "descricao": "Rua interditada para obras de drenagem. Utilize rotas alternativas."
            },
            {
                "titulo": "Falta de Água Programada",
                "data": "24/01/2024",
                "local": "Bairro Bárbaras e região central",
                "descricao": "Manutenção no sistema de abastecimento das 08h às 16h. Armazene água."
            }
        ],
        "coleta": {
            "Centro": "Segunda, Quarta e Sexta - 07h às 10h",
            "Jardim Aeroporto": "Terça e Quinta - 08h às 11h",
            "Bairro Bárbaras": "Segunda e Quinta - 09h às 11h",
            "Balsa da Harmonia": "Quarta e Sexta - 10h às 12h"
        }
    }
    
    # Atualiza dados da cidade mantendo estrutura existente
    dados_cidade_existentes = carregar_dados_cidade()
    if not dados_cidade_existentes["eventos"] and not dados_cidade_existentes["alertas"]:
        salvar_dados_cidade(dados_cidade_teste)
    
    # 4. INICIALIZAR CACHE DE COORDENADAS PARA OS TESTES
    cache_coordenadas = {
        "Avenida Machado de Assis, 250, Centro": (-21.4276, -45.9492),
        "Rua das Flores, 150, Jardim Aeroporto": (-21.4205, -45.9318),
        "Rua Bárbaras, 340, Bairro Bárbaras": (-21.4321, -45.9553),
        "Avenida Principal com Rua Harmonia, Balsa da Harmonia": (-21.4398, -45.9612),
        "Praça Getúlio Vargas - Centro": (-21.4259, -45.9465),
        "Parque Municipal - Jardim Aeroporto": (-21.4187, -45.9283),
        "Rua Bárbaras, entre números 300 e 400": (-21.4325, -45.9558)
    }
    
    # Atualiza cache existente
    cache_existente = carregar_cache()
    cache_existente.update(cache_coordenadas)
    salvar_cache(cache_existente)

    print("✅ Banco de dados inicializado com dados de teste!")

# -------------------------
# Splash screen - VERSÃO SEGURA
# -------------------------
def splash_and_open_main():
    splash = ctk.CTkToplevel(janela)
    splash.geometry("400x250")
    splash.title("SmartCity Hub")
    splash.resizable(False, False)
    splash.attributes("-alpha", 0.0)
    splash.transient(janela)
    splash.grab_set()

    label = ctk.CTkLabel(splash, text="SmartCity Hub", font=("Arial", 28, "bold"))
    label.pack(pady=40)

    barra = ctk.CTkProgressBar(splash, width=300)
    barra.pack(pady=20)
    barra.set(0)

    texto = ctk.CTkLabel(splash, text="Iniciando sistema...", font=("Arial", 14))
    texto.pack()

    def atualizar_barra():
        for i in range(101):
            try:
                if not splash.winfo_exists():
                    break
                barra.set(i/100)
                splash.update()
                time.sleep(0.02)
            except:
                break
        try:
            if splash.winfo_exists():
                splash.destroy()
        except:
            pass
        janela.after(300, lambda: fade_in_seguro(janela))

    fade_in_seguro(splash)
    threading.Thread(target=atualizar_barra, daemon=True).start()

# -------------------------
# Tela do Técnico - VERSÃO MODIFICADA PARA JANELA PRINCIPAL
# -------------------------
def criar_tela_tecnico(usuario, tipo):
    frame = ctk.CTkFrame(janela, fg_color="#0f1112")
    
    # Header com botão voltar
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkButton(header_frame, text="← Voltar", width=100,
                 command=lambda: voltar_para_dashboard(usuario, tipo)).pack(side="left")
    ctk.CTkLabel(header_frame, text="🛠️ Painel de Ocorrências", font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)
    
    # Conteúdo principal
    main_frame = ctk.CTkScrollableFrame(frame, width=580, height=400)
    main_frame.pack(pady=10, padx=20, fill="both", expand=True)

    def atualizar_lista():
        try:
            for w in main_frame.winfo_children():
                w.destroy()
        except:
            pass
            
        problemas = carregar_json(ARQ_PROBLEMAS, [])
        if not problemas:
            ctk.CTkLabel(main_frame, text="Nenhuma ocorrência registrada.").pack(pady=10)
            return
            
        for p in problemas:
            try:                    
                bloco = ctk.CTkFrame(main_frame, corner_radius=12)
                bloco.pack(fill="x", padx=8, pady=6)
                ctk.CTkLabel(bloco, text=f"#{p['id']} - {p['tipo']}", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=8)
                ctk.CTkLabel(bloco, text=f"{p['descricao']}", wraplength=500).pack(anchor="w", padx=8)
                ctk.CTkLabel(bloco, text=f"📍 {p['localizacao']} | {p['data']}", text_color="gray").pack(anchor="w", padx=8)

                status = ctk.StringVar(value=p["status"])
                menu = ctk.CTkOptionMenu(bloco, values=["Pendente", "Em andamento", "Resolvido"], variable=status)
                menu.pack(side="left", padx=8, pady=6)

                def salvar(pid=p["id"], var=status):
                    try:
                        dados = carregar_json(ARQ_PROBLEMAS, [])
                        for d in dados:
                            if d["id"] == pid:
                                d["status"] = var.get()
                                break
                        salvar_json(ARQ_PROBLEMAS, dados)
                        mostrar_mensagem("Atualizado", f"Status do problema #{pid} alterado para '{var.get()}'.", "sucesso")
                        atualizar_lista()
                    except Exception as e:
                        print(f"Erro ao salvar: {e}")

                ctk.CTkButton(bloco, text="💾 Salvar", width=80, command=salvar).pack(side="right", padx=8)
            except Exception as e:
                print(f"Erro ao criar bloco: {e}")
                continue

    atualizar_lista()
    
    # Botões de ação
    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(pady=10)
    
    ctk.CTkButton(btn_frame, text="🔄 Atualizar Lista", command=atualizar_lista, width=200).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="🗺️ Ver Mapa (navegador)", fg_color="#1E90FF", width=260,
                  command=lambda: webbrowser.open(f"file:///{gerar_mapa_html(carregar_json(ARQ_PROBLEMAS, []), filename=os.path.join(tempfile.gettempdir(),'mapa_ocorrencias_alfenas.html')).replace(os.sep, '/')}")).pack(side="left", padx=5)

    return frame

# -------------------------
# Tela para reportar problema - VERSÃO MODIFICADA
# -------------------------
def criar_tela_reportar_problema(usuario="Anônimo", tipo_usuario="Cidadão"):
    frame = ctk.CTkFrame(janela, fg_color="#0f1112")
    
    # Header com botão voltar
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkButton(header_frame, text="← Voltar", width=100,
                 command=lambda: voltar_para_dashboard(usuario, tipo_usuario)).pack(side="left")
    ctk.CTkLabel(header_frame, text="📢 Reportar Problema na Cidade", font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)
    
    # Conteúdo principal
    content_frame = ctk.CTkFrame(frame, fg_color="transparent")
    content_frame.pack(pady=20, padx=40, fill="both", expand=True)

    tipos = ["Iluminação Pública", "Buraco na rua", "Lixo acumulado", "Semáforo quebrado", "Outros"]
    tipo_var = ctk.StringVar(value=tipos[0])
    ctk.CTkLabel(content_frame, text="Tipo de problema:").pack(anchor="w", pady=(0,5))
    ctk.CTkOptionMenu(content_frame, values=tipos, variable=tipo_var, width=400).pack(pady=8, fill="x")

    ctk.CTkLabel(content_frame, text="Descrição detalhada:").pack(anchor="w", pady=(10,5))
    txt_desc = ctk.CTkTextbox(content_frame, width=400, height=120)
    txt_desc.pack(pady=8, fill="x")

    ctk.CTkLabel(content_frame, text="Localização (opcional):").pack(anchor="w", pady=(10,5))
    entry_local = ctk.CTkEntry(content_frame, width=400, placeholder_text="Ex: Rua José Carlos, nº 100, Centro")
    entry_local.pack(pady=6, fill="x")

    def salvar_problema():
        try:
            tipo = tipo_var.get()
            desc = txt_desc.get("0.0", "end").strip()
            local = entry_local.get().strip()
            if not desc:
                mostrar_mensagem("Atenção", "Por favor, descreva o problema.", "aviso")
                return
            dados = carregar_json(ARQ_PROBLEMAS, [])
            novo = {
                "id": (dados[-1]["id"] + 1) if dados else 1,
                "usuario": usuario,
                "tipo": tipo,
                "descricao": desc,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "localizacao": local if local else "Não informada",
                "status": "Pendente"
            }
            dados.append(novo)
            salvar_json(ARQ_PROBLEMAS, dados)
            mostrar_mensagem("Sucesso", "Seu relato foi enviado com sucesso!", "sucesso")
            voltar_para_dashboard(usuario, tipo_usuario)
        except Exception as e:
            print(f"Erro ao salvar problema: {e}")

    ctk.CTkButton(content_frame, text="✅ Enviar Relato", fg_color="#2E8B57", width=240, command=salvar_problema).pack(pady=18)

    return frame

# -------------------------
# Dashboard Gestor COM GRÁFICOS - VERSÃO CORRIGIDA
# -------------------------
def criar_tela_dashboard_gestor(usuario, tipo):
    problemas = carregar_json(ARQ_PROBLEMAS, [])
    frame = ctk.CTkFrame(janela, fg_color="#0f1112")
    
    # Header com botão voltar
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkButton(header_frame, text="← Voltar", width=100,
                 command=lambda: voltar_para_dashboard(usuario, tipo)).pack(side="left")
    ctk.CTkLabel(header_frame, text="📊 Dashboard - Gestor", font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)

    # Frame principal com scroll
    main_frame = ctk.CTkScrollableFrame(frame)
    main_frame.pack(fill="both", expand=True, padx=12, pady=12)

    # Container para estatísticas e gráficos
    stats_container = ctk.CTkFrame(main_frame)
    stats_container.pack(fill="x", padx=10, pady=10)

    # Linha superior - KPIs
    kpi_frame = ctk.CTkFrame(stats_container)
    kpi_frame.pack(fill="x", pady=(0, 20))

    total = len(problemas)
    pendente = sum(1 for p in problemas if p.get('status') == 'Pendente')
    andamento = sum(1 for p in problemas if p.get('status') == 'Em andamento')
    resolvidas = sum(1 for p in problemas if p.get('status') == 'Resolvido')
    
    # Taxa de resolução
    taxa_resolucao = (resolvidas / total * 100) if total > 0 else 0

    def criar_kpi(parent, title, value, color=None, subtitle=""):
        kpi = ctk.CTkFrame(parent, width=180, height=100, corner_radius=12)
        kpi.pack(side="left", padx=8, pady=8, fill="both", expand=True)
        kpi.pack_propagate(False)
        
        ctk.CTkLabel(kpi, text=title, font=("Segoe UI", 12), text_color="gray").pack(pady=(12, 4))
        ctk.CTkLabel(kpi, text=str(value), font=("Segoe UI", 24, "bold"), text_color=color).pack(pady=4)
        if subtitle:
            ctk.CTkLabel(kpi, text=subtitle, font=("Segoe UI", 10), text_color="gray").pack(pady=(0, 12))
        return kpi

    criar_kpi(kpi_frame, "Total de Ocorrências", total)
    criar_kpi(kpi_frame, "Pendentes", pendente, "#FF6B6B")
    criar_kpi(kpi_frame, "Em Andamento", andamento, "#FFA500")
    criar_kpi(kpi_frame, "Resolvidas", resolvidas, "#4CAF50")
    criar_kpi(kpi_frame, "Taxa de Resolução", f"{taxa_resolucao:.1f}%", "#4CAF50")

    # Linha do meio - Gráficos
    charts_frame = ctk.CTkFrame(stats_container)
    charts_frame.pack(fill="x", pady=10)

    # Gráfico 1: Ocorrências por Tipo
    chart1_frame = ctk.CTkFrame(charts_frame, width=400, height=300)
    chart1_frame.pack(side="left", padx=(0, 10), pady=10, fill="both", expand=True)
    chart1_frame.pack_propagate(False)

    ctk.CTkLabel(chart1_frame, text="📊 Distribuição por Tipo de Problema", 
                font=("Segoe UI", 14, "bold")).pack(pady=(10, 5))

    try:
        # Coletar dados por tipo
        tipos_contagem = {}
        for p in problemas:
            tipo = p.get('tipo', 'Outros')
            tipos_contagem[tipo] = tipos_contagem.get(tipo, 0) + 1

        # Criar gráfico de pizza
        fig1 = Figure(figsize=(5, 3), dpi=80, facecolor='#0f1112')
        ax1 = fig1.add_subplot(111)
        
        if tipos_contagem:
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
            wedges, texts, autotexts = ax1.pie(
                tipos_contagem.values(), 
                labels=tipos_contagem.keys(), 
                autopct='%1.1f%%',
                colors=cores[:len(tipos_contagem)],
                startangle=90,
                textprops={'color': 'white', 'fontsize': 8}
            )
            
            # Melhorar legibilidade
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            ax1.set_title('Distribuição por Tipo', color='white', fontsize=12, pad=10)
        else:
            ax1.text(0.5, 0.5, 'Sem dados\n disponíveis', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax1.transAxes, color='white', fontsize=12)
            ax1.set_facecolor('#0f1112')
        
        fig1.patch.set_facecolor('#0f1112')
        ax1.set_facecolor('#0f1112')
        
        canvas1 = FigureCanvasTkAgg(fig1, chart1_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
    except Exception as e:
        print(f"Erro ao criar gráfico 1: {e}")
        ctk.CTkLabel(chart1_frame, text="Erro ao carregar gráfico", text_color="red").pack(pady=20)

    # Gráfico 2: Evolução Temporal
    chart2_frame = ctk.CTkFrame(charts_frame, width=400, height=300)
    chart2_frame.pack(side="right", padx=(10, 0), pady=10, fill="both", expand=True)
    chart2_frame.pack_propagate(False)

    ctk.CTkLabel(chart2_frame, text="📈 Evolução de Status (Últimos 6 Meses)", 
                font=("Segoe UI", 14, "bold")).pack(pady=(10, 5))

    try:
        # Gerar dados históricos para os últimos 6 meses
        meses_hist = {}
        ano_atual = 2024
        meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        # Coletar dados reais
        for p in problemas:
            try:
                dt = datetime.strptime(p.get('data', '2024-01-01 00:00'), "%Y-%m-%d %H:%M")
                mes_key = dt.strftime('%Y-%m')
                if mes_key not in meses_hist:
                    meses_hist[mes_key] = {'Pendente': 0, 'Em andamento': 0, 'Resolvido': 0}
                
                status = p.get('status', 'Pendente')
                if status in meses_hist[mes_key]:
                    meses_hist[mes_key][status] += 1
            except:
                continue
        
        # Preencher com dados simulados se necessário
        meses_para_mostrar = 6
        for i in range(meses_para_mostrar):
            mes = (datetime.now().month - i - 1) % 12 + 1
            ano = ano_atual if mes <= datetime.now().month else ano_atual - 1
            chave = f"{ano}-{mes:02d}"
            
            if chave not in meses_hist:
                # Dados simulados realistas
                base = max(2, 10 - i)
                meses_hist[chave] = {
                    'Pendente': base + random.randint(-2, 3),
                    'Em andamento': max(1, base // 2 + random.randint(-1, 2)),
                    'Resolvido': min(15, base * 2 + random.randint(-2, 4))
                }
        
        # Ordenar e pegar últimos 6 meses
        meses_ordenados = sorted(meses_hist.keys())[-6:]
        rotulos = []
        for mes in meses_ordenados:
            ano, mes_num = mes.split('-')
            rotulos.append(f"{meses_nomes[int(mes_num)-1]}/{ano[2:]}")

        # Criar gráfico de linha
        fig2 = Figure(figsize=(5, 3), dpi=80, facecolor='#0f1112')
        ax2 = fig2.add_subplot(111)
        
        if meses_ordenados:
            pendentes_data = [meses_hist[mes].get('Pendente', 0) for mes in meses_ordenados]
            andamento_data = [meses_hist[mes].get('Em andamento', 0) for mes in meses_ordenados]
            resolvidos_data = [meses_hist[mes].get('Resolvido', 0) for mes in meses_ordenados]
            
            ax2.plot(rotulos, pendentes_data, marker='o', linewidth=2, label='Pendente', color='#FF6B6B')
            ax2.plot(rotulos, andamento_data, marker='s', linewidth=2, label='Em Andamento', color='#FFA500')
            ax2.plot(rotulos, resolvidos_data, marker='^', linewidth=2, label='Resolvido', color='#4CAF50')
            
            ax2.set_title('Evolução Mensal', color='white', fontsize=12, pad=10)
            ax2.legend(facecolor='#0f1112', edgecolor='white', labelcolor='white', fontsize=8)
            ax2.tick_params(axis='x', rotation=45, colors='white')
            ax2.tick_params(axis='y', colors='white')
            ax2.grid(True, alpha=0.3)
            ax2.set_facecolor('#0f1112')
            
            # Configurar cores do gráfico
            for spine in ax2.spines.values():
                spine.set_color('white')
        else:
            ax2.text(0.5, 0.5, 'Sem dados\n disponíveis', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax2.transAxes, color='white', fontsize=12)
            ax2.set_facecolor('#0f1112')
        
        fig2.patch.set_facecolor('#0f1112')
        
        canvas2 = FigureCanvasTkAgg(fig2, chart2_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
    except Exception as e:
        print(f"Erro ao criar gráfico 2: {e}")
        ctk.CTkLabel(chart2_frame, text="Erro ao carregar gráfico", text_color="red").pack(pady=20)

    # Seção do Mapa
    mapa_section = ctk.CTkFrame(main_frame, corner_radius=12)
    mapa_section.pack(fill="x", pady=20, padx=10)

    ctk.CTkLabel(mapa_section, text="🗺️ Mapa Interativo de Ocorrências", 
                font=("Segoe UI", 16, "bold")).pack(pady=(15, 10))

    mapa_info_frame = ctk.CTkFrame(mapa_section)
    mapa_info_frame.pack(fill="x", padx=20, pady=10)

    info_text = """
    • 🔴 Vermelho: Ocorrências Pendentes
    • 🟠 Laranja: Ocorrências em Andamento  
    • 🟢 Verde: Ocorrências Resolvidas

    💡 Clique no botão abaixo para abrir o mapa completo no navegador com:
    - Agrupamento por região
    - Filtros por status  
    - Heatmap de densidade
    - Informações detalhadas
    """

    ctk.CTkLabel(mapa_info_frame, text=info_text, font=("Segoe UI", 12), 
                 justify="left", wraplength=600).pack(pady=15)

    def abrir_mapa_completo():
        try:
            mapa_path = gerar_mapa_html(problemas, filename=os.path.join(tempfile.gettempdir(),'mapa_ocorrencias_alfenas.html'))
            webbrowser.open(f"file:///{mapa_path.replace(os.sep, '/')}")
        except Exception as e:
            mostrar_mensagem("Erro", f"Erro ao abrir mapa: {e}", "erro")

    ctk.CTkButton(mapa_section, text="🗺️ Abrir Mapa Completo no Navegador", 
                  fg_color="#1E90FF", command=abrir_mapa_completo, 
                  height=40, font=("Segoe UI", 14)).pack(pady=15)

    # Ações rápidas
    acoes_frame = ctk.CTkFrame(main_frame, corner_radius=12)
    acoes_frame.pack(fill="x", pady=10, padx=10)

    ctk.CTkLabel(acoes_frame, text="⚡ Ações Rápidas", 
                font=("Segoe UI", 16, "bold")).pack(pady=(15, 10))

    botoes_frame = ctk.CTkFrame(acoes_frame, fg_color="transparent")
    botoes_frame.pack(pady=10)

    ctk.CTkButton(botoes_frame, text="📅 Cadastrar Evento/Aviso", 
                  command=lambda: mostrar_tela(criar_tela_cadastro_evento_gestor, usuario, tipo),
                  width=200, height=40).pack(side="left", padx=10)
    
    ctk.CTkButton(botoes_frame, text="🛠️ Gerenciar Ocorrências", 
                  command=lambda: mostrar_tela(criar_tela_tecnico, usuario, tipo),
                  width=200, height=40).pack(side="left", padx=10)
    
    ctk.CTkButton(botoes_frame, text="📊 Exportar Relatório", 
                  command=lambda: exportar_relatorio_excel(),
                  width=200, height=40, fg_color="#2E8B57").pack(side="left", padx=10)

    return frame

# -------------------------
# Tela de Consulta de Transporte - VERSÃO MODIFICADA
# -------------------------
def criar_tela_consultar_transporte(usuario, tipo):
    frame = ctk.CTkFrame(janela, fg_color="#0f1112")
    
    # Header com botão voltar
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkButton(header_frame, text="← Voltar", width=100,
                 command=lambda: voltar_para_dashboard(usuario, tipo)).pack(side="left")
    ctk.CTkLabel(header_frame, text="🚍 Consultar Transporte - Alfenas/MG", font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)

    # Conteúdo principal
    content_frame = ctk.CTkFrame(frame, fg_color="transparent")
    content_frame.pack(pady=20, padx=40, fill="both", expand=True)

    var_linha = ctk.StringVar(value=list(horarios_linhas.keys())[0])
    combo = ctk.CTkOptionMenu(content_frame, values=list(horarios_linhas.keys()), variable=var_linha, width=380)
    combo.pack(pady=8)

    frame_info = ctk.CTkFrame(content_frame, corner_radius=12)
    frame_info.pack(padx=14, pady=10, fill="both", expand=False)

    txt_horarios = ctk.CTkLabel(frame_info, text="", font=("Segoe UI", 13), wraplength=420)
    txt_horarios.pack(padx=10, pady=(12,6))

    txt_proximo = ctk.CTkLabel(frame_info, text="", font=("Segoe UI", 14, "italic"))
    txt_proximo.pack(padx=10, pady=(0,12))

    def atualizar():
        try:
            linha = var_linha.get()
            hrs = horarios_linhas.get(linha, [])
            txt_horarios.configure(text="\n".join(hrs) if hrs else "Sem horários disponíveis.")
            agora = datetime.now().time()
            try:
                prox = next((datetime.strptime(h, "%H:%M").time() for h in hrs if datetime.strptime(h, "%H:%M").time() > agora), None)
                txt_proximo.configure(text=f"Próximo ônibus: {prox.strftime('%H:%M')}" if prox else "Nenhum ônibus restante hoje.")
            except Exception:
                txt_proximo.configure(text="Erro ao calcular próximo horário.")
        except:
            pass

    def ver_mapa():
        try:
            abrir_mapa_folium(var_linha.get())
        except:
            pass

    ctk.CTkButton(content_frame, text="🔄 Atualizar", command=atualizar, width=200).pack(pady=(8,6))
    ctk.CTkButton(content_frame, text="🗺️ Ver rota no mapa", fg_color="#1E90FF", command=ver_mapa, width=200).pack(pady=(0,10))

    atualizar()

    return frame

# -------------------------
# Tela de Coleta de Lixo - VERSÃO MODIFICADA
# -------------------------
def criar_tela_coleta_lixo(usuario, tipo):
    dados = carregar_dados_cidade()
    coleta = dados.get("coleta", {})
    frame = ctk.CTkFrame(janela, fg_color="#0f1112")
    
    # Header com botão voltar
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkButton(header_frame, text="← Voltar", width=100,
                 command=lambda: voltar_para_dashboard(usuario, tipo)).pack(side="left")
    ctk.CTkLabel(header_frame, text="🗑️ Horários de Coleta de Lixo", font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)
    
    # Frame scrollable para os horários
    scroll_frame = ctk.CTkScrollableFrame(frame, width=450, height=400)
    scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    if not coleta:
        ctk.CTkLabel(scroll_frame, text="Nenhum horário de coleta cadastrado.", font=("Segoe UI", 14)).pack(pady=20)
    else:
        for bairro, horario in coleta.items():
            card = ctk.CTkFrame(scroll_frame, corner_radius=10)
            card.pack(fill="x", padx=10, pady=8)
            
            ctk.CTkLabel(card, text=f"🏘️ {bairro}", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=15, pady=(10, 5))
            ctk.CTkLabel(card, text=f"📅 {horario}", font=("Segoe UI", 14)).pack(anchor="w", padx=15, pady=(0, 10))

    return frame

# -------------------------
# Tela de Eventos e Avisos - VERSÃO MODIFICADA
# -------------------------
def criar_tela_eventos_e_avisos(usuario, tipo):
    dados = carregar_dados_cidade()
    eventos = dados.get("eventos", [])
    alertas = dados.get("alertas", [])

    frame = ctk.CTkFrame(janela, fg_color="#0f1112")
    
    # Header com botão voltar
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkButton(header_frame, text="← Voltar", width=100,
                 command=lambda: voltar_para_dashboard(usuario, tipo)).pack(side="left")
    ctk.CTkLabel(header_frame, text="📅 Eventos e Avisos", font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)

    # Abas para eventos e alertas
    tabview = ctk.CTkTabview(frame, width=560, height=500)
    tabview.pack(pady=20, padx=20, fill="both", expand=True)
    
    tab_eventos = tabview.add("🎫 Eventos")
    tab_alertas = tabview.add("⚠️ Avisos")

    # Frame para eventos
    eventos_frame = ctk.CTkScrollableFrame(tab_eventos)
    eventos_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    if not eventos:
        ctk.CTkLabel(eventos_frame, text="Nenhum evento cadastrado.", font=("Segoe UI", 14)).pack(pady=20)
    else:
        for evento in eventos:
            card = ctk.CTkFrame(eventos_frame, corner_radius=10)
            card.pack(fill="x", padx=10, pady=8)
            
            ctk.CTkLabel(card, text=f"🎫 {evento.get('titulo', 'Sem título')}", 
                        font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=15, pady=(10, 5))
            ctk.CTkLabel(card, text=f"📅 {evento.get('data', 'Data não informada')} | 📍 {evento.get('local', 'Local não informado')}", 
                        font=("Segoe UI", 12)).pack(anchor="w", padx=15)
            ctk.CTkLabel(card, text=evento.get('descricao', 'Sem descrição'), 
                        wraplength=500, font=("Segoe UI", 12)).pack(anchor="w", padx=15, pady=(5, 10))

    # Frame para alertas
    alertas_frame = ctk.CTkScrollableFrame(tab_alertas)
    alertas_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    if not alertas:
        ctk.CTkLabel(alertas_frame, text="Nenhum aviso ativo.", font=("Segoe UI", 14)).pack(pady=20)
    else:
        for alerta in alertas:
            card = ctk.CTkFrame(alertas_frame, corner_radius=10, fg_color="#2B1B17")
            card.pack(fill="x", padx=10, pady=8)
            
            ctk.CTkLabel(card, text=f"⚠️ {alerta.get('titulo', 'Sem título')}", 
                        font=("Segoe UI", 16, "bold"), text_color="#FF6B6B").pack(anchor="w", padx=15, pady=(10, 5))
            ctk.CTkLabel(card, text=f"📅 {alerta.get('data', 'Data não informada')} | 📍 {alerta.get('local', 'Local não informado')}", 
                        font=("Segoe UI", 12)).pack(anchor="w", padx=15)
            ctk.CTkLabel(card, text=alerta.get('descricao', 'Sem descrição'), 
                        wraplength=500, font=("Segoe UI", 12)).pack(anchor="w", padx=15, pady=(5, 10))

    return frame

# -------------------------
# Tela de Cadastro de Eventos/Avisos (Gestor) - VERSÃO MODIFICADA
# -------------------------
def criar_tela_cadastro_evento_gestor(usuario, tipo):
    frame = ctk.CTkFrame(janela, fg_color="#0f1112")
    
    # Header com botão voltar
    header_frame = ctk.CTkFrame(frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=20, pady=10)
    
    ctk.CTkButton(header_frame, text="← Voltar", width=100,
                 command=lambda: voltar_para_dashboard(usuario, tipo)).pack(side="left")
    ctk.CTkLabel(header_frame, text="📅 Cadastrar Evento / Aviso (Gestor)", font=("Segoe UI", 18, "bold")).pack(side="left", padx=10)

    # Conteúdo principal
    content_frame = ctk.CTkFrame(frame, fg_color="transparent")
    content_frame.pack(pady=20, padx=40, fill="both", expand=True)

    tipo_var = ctk.StringVar(value="Evento")
    ctk.CTkLabel(content_frame, text="Tipo:").pack(anchor='w', pady=(0,5))
    ctk.CTkOptionMenu(content_frame, values=["Evento", "Aviso"], variable=tipo_var, width=200).pack(pady=6, fill="x")

    titulo_entry = ctk.CTkEntry(content_frame, placeholder_text="Título", width=420)
    titulo_entry.pack(pady=6, fill="x")
    data_entry = ctk.CTkEntry(content_frame, placeholder_text="Data (ex: 25/10/2025)", width=420)
    data_entry.pack(pady=6, fill="x")
    local_entry = ctk.CTkEntry(content_frame, placeholder_text="Local", width=420)
    local_entry.pack(pady=6, fill="x")
    desc_txt = ctk.CTkTextbox(content_frame, width=420, height=140)
    desc_txt.pack(pady=8, fill="x")

    def salvar_evento():
        try:
            titulo = titulo_entry.get().strip()
            data = data_entry.get().strip()
            local = local_entry.get().strip()
            desc = desc_txt.get("1.0", "end").strip()
            if not titulo or not data or not local or not desc:
                mostrar_mensagem("Erro", "Preencha todos os campos!", "aviso")
                return
            dados = carregar_dados_cidade()
            item = {"titulo": titulo, "data": data, "local": local, "descricao": desc}
            if tipo_var.get() == "Evento":
                dados["eventos"].append(item)
                mostrar_mensagem("Sucesso", "Evento cadastrado com sucesso!", "sucesso")
            else:
                dados["alertas"].append(item)
                mostrar_mensagem("Sucesso", "Aviso cadastrado com sucesso!", "sucesso")
            salvar_dados_cidade(dados)
            voltar_para_dashboard(usuario, tipo)
        except Exception as e:
            print(f"Erro ao salvar evento/aviso: {e}")

    ctk.CTkButton(content_frame, text="Salvar", fg_color="#2E8B57", command=salvar_evento, width=180).pack(pady=12)

    return frame

# -------------------------
# Dashboard Principal - VERSÃO MODIFICADA
# -------------------------
def criar_tela_dashboard(usuario, tipo):
    frame = ctk.CTkFrame(janela, fg_color="#0f1112")
    
    ctk.CTkLabel(frame, text=f"Bem-vindo, {usuario}!", font=("Segoe UI", 20, "bold")).pack(pady=(30, 10))

    if tipo == "Cidadão":
        ctk.CTkButton(frame, text="🚌 Consultar Transporte", width=320, 
                     command=lambda: mostrar_tela(criar_tela_consultar_transporte, usuario, tipo)).pack(pady=8)
        ctk.CTkButton(frame, text="📢 Reportar Problema", width=320, fg_color="#DAA520", 
                     command=lambda: mostrar_tela(criar_tela_reportar_problema, usuario, tipo)).pack(pady=8)
        ctk.CTkButton(frame, text="🗑️ Coleta de Lixo", width=320, 
                     command=lambda: mostrar_tela(criar_tela_coleta_lixo, usuario, tipo)).pack(pady=8)
        ctk.CTkButton(frame, text="📅 Eventos & Avisos", width=320, 
                     command=lambda: mostrar_tela(criar_tela_eventos_e_avisos, usuario, tipo)).pack(pady=8)
    elif tipo == "Gestor":
        ctk.CTkButton(frame, text="📅 Cadastrar Evento/Aviso", width=320, 
                     command=lambda: mostrar_tela(criar_tela_cadastro_evento_gestor, usuario, tipo)).pack(pady=12)
        ctk.CTkButton(frame, text="📊 Monitorar Ocorrências", width=320, fg_color="#1E90FF", 
                     command=lambda: mostrar_tela(criar_tela_tecnico, usuario, tipo)).pack(pady=12)
        ctk.CTkButton(frame, text="🚀 Dashboard Completo", width=320, fg_color="#6A5ACD", 
                     command=lambda: mostrar_tela(criar_tela_dashboard_gestor, usuario, tipo)).pack(pady=8)
    elif tipo == "Técnico":
        ctk.CTkButton(frame, text="🛠️ Gerenciar Ocorrências", width=320, fg_color="#1E90FF", 
                     command=lambda: mostrar_tela(criar_tela_tecnico, usuario, tipo)).pack(pady=8)
        ctk.CTkButton(frame, text="🗺️ Ver Mapa (navegador)", width=320, fg_color="#FF8C00",
                     command=lambda: webbrowser.open(f"file:///{gerar_mapa_html(carregar_json(ARQ_PROBLEMAS, []), filename=os.path.join(tempfile.gettempdir(),'mapa_ocorrencias_alfenas.html')).replace(os.sep, '/')}")).pack(pady=8)

    # Botão de logout
    ctk.CTkButton(frame, text="🚪 Sair", width=200, fg_color="#555555", 
                 command=lambda: mostrar_tela(criar_tela_login)).pack(pady=20)

    return frame

# -------------------------
# Tela de Login - VERSÃO MODIFICADA
# -------------------------
def criar_tela_login():
    frame = ctk.CTkFrame(janela, width=400, height=420, corner_radius=20, fg_color=("#0f1112", "#131416"))
    
    ctk.CTkLabel(frame, text="🏙️ SmartCity Hub", font=("Segoe UI", 24, "bold")).pack(pady=(20,8))
    ctk.CTkLabel(frame, text="Acesse sua conta", font=("Segoe UI", 13)).pack(pady=(0,15))

    entry_usuario = ctk.CTkEntry(frame, placeholder_text="Usuário", width=260, height=36)
    entry_usuario.pack(pady=6)
    entry_senha = ctk.CTkEntry(frame, placeholder_text="Senha", width=260, height=36, show="*")
    entry_senha.pack(pady=6)

    mostrar_senha = ctk.BooleanVar(value=False)
    def toggle_senha():
        entry_senha.configure(show="" if mostrar_senha.get() else "*")
    ctk.CTkCheckBox(frame, text="Mostrar senha", variable=mostrar_senha, command=toggle_senha).pack(pady=(4,8))

    tipo_usuario = ctk.StringVar(value="Cidadão")
    ctk.CTkLabel(frame, text="Tipo de usuário:").pack(pady=(4,2))
    ctk.CTkOptionMenu(frame, values=["Cidadão", "Gestor", "Técnico"], variable=tipo_usuario).pack(pady=6)

    def fazer_login():
        user = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        if not user or not senha:
            mostrar_mensagem("Erro", "Preencha todos os campos!", "aviso")
            return
        if user in usuarios and usuarios[user]["senha"] == senha:
            tipo = usuarios[user]["tipo"]
            mostrar_mensagem("Login", f"Bem-vindo, {user}!", "sucesso")
            janela.after(300, lambda: mostrar_tela(criar_tela_dashboard, user, tipo))
        else:
            mostrar_mensagem("Erro", "Usuário ou senha incorretos!", "erro")

    def fazer_cadastro():
        user = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        tipo = tipo_usuario.get()
        if not user or not senha:
            mostrar_mensagem("Erro", "Preencha todos os campos!", "aviso")
            return
        if user in usuarios:
            mostrar_mensagem("Erro", "Usuário já existe!", "erro")
            return
        usuarios[user] = {"senha": senha, "tipo": tipo}
        salvar_usuarios()
        mostrar_mensagem("Cadastro", f"Usuário '{user}' cadastrado como {tipo}!", "sucesso")

    ctk.CTkButton(frame, text="Entrar", width=240, fg_color="#2E8B57", hover_color="#3CB371", command=fazer_login).pack(pady=(15,6))
    ctk.CTkButton(frame, text="Cadastrar", width=240, fg_color="#555555", hover_color="#777777", command=fazer_cadastro).pack(pady=(0,10))
    ctk.CTkButton(frame, text="🗺️ Consultar Transporte", width=240, fg_color="#1E90FF", 
                 command=lambda: mostrar_tela(criar_tela_consultar_transporte, "Visitante", "Cidadão")).pack(pady=(4,10))

    ctk.CTkLabel(frame, text="SmartCity © 2025", font=("Segoe UI", 10), text_color="gray").pack(side="bottom", pady=8)

    return frame

# -------------------------
# Sistema de Login (funções originais mantidas para compatibilidade)
# -------------------------
def login():
    user = entry_usuario.get().strip()
    senha = entry_senha.get().strip()
    if not user or not senha:
        mostrar_mensagem("Erro", "Preencha todos os campos!", "aviso")
        return
    if user in usuarios and usuarios[user]["senha"] == senha:
        tipo = usuarios[user]["tipo"]
        mostrar_mensagem("Login", f"Bem-vindo, {user}!", "sucesso")
        janela.after(300, lambda: mostrar_tela(criar_tela_dashboard, user, tipo))
    else:
        mostrar_mensagem("Erro", "Usuário ou senha incorretos!", "erro")

def cadastrar():
    user = entry_usuario.get().strip()
    senha = entry_senha.get().strip()
    tipo = tipo_usuario.get()
    if not user or not senha:
        mostrar_mensagem("Erro", "Preencha todos os campos!", "aviso")
        return
    if user in usuarios:
        mostrar_mensagem("Erro", "Usuário já existe!", "erro")
        return
    usuarios[user] = {"senha": senha, "tipo": tipo}
    salvar_usuarios()
    mostrar_mensagem("Cadastro", f"Usuário '{user}' cadastrado como {tipo}!", "sucesso")

# -------------------------
# Interface Principal
# -------------------------
try:
    bg = Image.open("background_day_minimal.jpg").resize((820,540))
    bg_photo = ImageTk.PhotoImage(bg)
    bg_label = ctk.CTkLabel(janela, image=bg_photo, text="")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception:
    janela.configure(fg_color="#0B0B0C")

# Variáveis globais para a tela de login (mantidas para compatibilidade)
entry_usuario = None
entry_senha = None
tipo_usuario = None

# -------------------------
# Inicialização
# -------------------------
if __name__ == "__main__":
    # Inicializa com dados de teste
    inicializar_dados_teste()
    
    # Garante que a janela principal comece invisível
    try:
        janela.attributes("-alpha", 0.0)
    except:
        pass
    
    # Inicia com splash screen e depois mostra a tela de login
    def iniciar_app():
        mostrar_tela(criar_tela_login)
    
    splash_and_open_main()
    janela.after(2500, iniciar_app)
    janela.mainloop()
