import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import os
from datetime import datetime
import time

st.set_page_config(page_title="Busca Movimentos 711/712", layout="wide")

# ==================== SELETOR DE TEMA ====================
st.sidebar.markdown("### 🎨 Tema de Aparência")
tema_selecionado = st.sidebar.selectbox(
    "Escolha o tema:",
    [
        "Tema 1: Preto e Amarelo", 
        "Tema 2: Azul Marinho e Branco", 
        "Tema 3: Cinza Escuro e Verde Fluorescente", 
        "Tema 4: Futurista",
        "Tema 5: Vermelho Escuro e Branco"
    ],
    index=0
)

# Definir cores baseado no tema
if tema_selecionado == "Tema 1: Preto e Amarelo":
    cor_fundo = "#000000"
    cor_texto = "#FFD700"
    cor_secundaria = "#FFA500"
    cor_destaque = "#FFFF00"
    animacao_led = ""
elif tema_selecionado == "Tema 2: Azul Marinho e Branco":
    cor_fundo = "#001F3F"
    cor_texto = "#FFFFFF"
    cor_secundaria = "#7FDBFF"
    cor_destaque = "#39CCCC"
    animacao_led = ""
elif tema_selecionado == "Tema 3: Cinza Escuro e Verde Fluorescente":
    cor_fundo = "#2C2C2C"
    cor_texto = "#00FF00"
    cor_secundaria = "#39FF14"
    cor_destaque = "#7FFF00"
    animacao_led = ""
elif tema_selecionado == "Tema 4: Futurista":
    cor_fundo = "#0D0221"
    cor_texto = "#00FF41"
    cor_secundaria = "#FF006E"
    cor_destaque = "#8338EC"
    # Animação de LED piscando por 10 segundos
    animacao_led = """
    @keyframes ledBlink {
        0%, 100% { opacity: 1; text-shadow: 0 0 10px #00FF41, 0 0 20px #00FF41, 0 0 30px #00FF41; }
        25% { opacity: 0.3; text-shadow: 0 0 5px #00FF41; }
        50% { opacity: 1; text-shadow: 0 0 15px #8338EC, 0 0 25px #8338EC, 0 0 35px #8338EC; }
        75% { opacity: 0.5; text-shadow: 0 0 8px #FF006E; }
    }
    
    @keyframes ledPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .tema-futurista h1, .tema-futurista h2, .tema-futurista h3 {
        animation: ledBlink 2s ease-in-out infinite, ledPulse 3s ease-in-out infinite;
        animation-duration: 10s;
    }
    
    .tema-futurista .relogio {
        animation: ledBlink 1.5s ease-in-out infinite !important;
        animation-duration: 10s !important;
    }
    
    .tema-futurista .stButton>button {
        animation: ledBlink 2.5s ease-in-out infinite;
        animation-duration: 10s;
    }
    
    .tema-futurista {
        animation-play-state: running;
    }
    """
else:  # Tema 5: Vermelho Escuro e Branco
    cor_fundo = "#8B0000"
    cor_texto = "#FFFFFF"
    cor_secundaria = "#DC143C"
    cor_destaque = "#FF6347"
    animacao_led = ""

# CSS customizado baseado no tema
st.markdown(f"""
    <style>
    /* Tema de cores */
    .stApp {{
        background-color: {cor_fundo};
    }}
    
    {animacao_led if tema_selecionado == "Tema 4: Futurista" else ""}
    
    /* Aplicar classe futurista se tema 4 */
    {"body { } .stApp { }" if tema_selecionado != "Tema 4: Futurista" else "body .stApp, body .stApp * { } .stApp { }"}
    
    /* Textos principais */
    h1, h2, h3, h4, h5, h6, p, span, div, label {{
        color: {cor_texto} !important;
    }}
    
    /* Relógio digital */
    .relogio-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
        margin: 20px 0;
        background: linear-gradient(135deg, {cor_secundaria}22, {cor_destaque}22);
        border-radius: 15px;
        border: 2px solid {cor_destaque};
        box-shadow: 0 0 20px {cor_destaque}44;
    }}
    
    .relogio {{
        font-size: 48px;
        font-weight: bold;
        color: {cor_destaque};
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px {cor_destaque};
    }}
    
    .data {{
        font-size: 24px;
        color: {cor_texto};
        font-weight: bold;
        margin-top: 10px;
        text-align: center;
    }}
    
    /* Rodapé */
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: {cor_fundo}EE;
        color: {cor_texto};
        text-align: center;
        padding: 10px;
        font-size: 11px;
        border-top: 2px solid {cor_destaque};
        z-index: 999;
    }}
    
    /* Espaçamento para o rodapé */
    .main {{
        padding-bottom: 60px;
    }}
    
    /* Botões */
    .stButton>button {{
        background-color: {cor_destaque};
        color: {cor_fundo};
        border: 2px solid {cor_secundaria};
        font-weight: bold;
    }}
    
    .stButton>button:hover {{
        background-color: {cor_secundaria};
        color: {cor_fundo};
    }}
    
    /* Inputs */
    .stTextInput>div>div>input {{
        background-color: {cor_fundo};
        color: {cor_texto};
        border: 1px solid {cor_destaque};
    }}
    
    .stSelectbox>div>div>select {{
        background-color: {cor_fundo};
        color: {cor_texto};
        border: 1px solid {cor_destaque};
    }}
    
    /* DataFrames */
    .dataframe {{
        background-color: {cor_fundo};
        color: {cor_texto};
    }}
    
    /* Métricas */
    .css-1xarl3l {{
        background-color: {cor_secundaria}22;
        border: 1px solid {cor_destaque};
        border-radius: 10px;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {cor_fundo}DD;
    }}
    
    section[data-testid="stSidebar"] * {{
        color: {cor_texto} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Adicionar classe tema-futurista ao body se tema 4
if tema_selecionado == "Tema 4: Futurista":
    st.markdown("""
        <script>
        document.body.classList.add('tema-futurista');
        document.querySelector('.stApp').classList.add('tema-futurista');
        </script>
    """, unsafe_allow_html=True)

# ==================== LOGOS ====================
try:
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    possiveis_logos_petrobras = [
        'logo_petrobras.png', 'logo petrobras.png', 'petrobras.png',
        'logo_petrobras.jpg', 'logo petrobras.jpg', 'petrobras.jpg'
    ]
    
    logo_petrobras_path = None
    for nome_logo in possiveis_logos_petrobras:
        caminho = os.path.join(pasta_atual, nome_logo)
        if os.path.exists(caminho):
            logo_petrobras_path = caminho
            break
    
    possiveis_logos_jsl = [
        'logo_jsl.png', 'logo jsl.png', 'jsl.png',
        'logo_jsl.jpg', 'logo jsl.jpg', 'jsl.jpg'
    ]
    
    logo_jsl_path = None
    for nome_logo in possiveis_logos_jsl:
        caminho = os.path.join(pasta_atual, nome_logo)
        if os.path.exists(caminho):
            logo_jsl_path = caminho
            break
    
    col_logo1, col_espaco, col_logo2 = st.columns([1, 3, 1])
    
    with col_logo1:
        if logo_petrobras_path:
            logo_petrobras = Image.open(logo_petrobras_path)
            st.image(logo_petrobras, width=120)
        else:
            st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: {cor_texto}; opacity: 0.7;'>⛽ PETROBRAS</div>", unsafe_allow_html=True)
    
    with col_logo2:
        if logo_jsl_path:
            logo_jsl = Image.open(logo_jsl_path)
            st.image(logo_jsl, width=120)
        else:
            st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: {cor_texto}; opacity: 0.7;'>🚛 JSL</div>", unsafe_allow_html=True)

except Exception as e:
    col_logo1, col_espaco, col_logo2 = st.columns([1, 3, 1])
    with col_logo1:
        st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: {cor_texto}; opacity: 0.7;'>⛽ PETROBRAS</div>", unsafe_allow_html=True)
    with col_logo2:
        st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: {cor_texto}; opacity: 0.7;'>🚛 JSL</div>", unsafe_allow_html=True)

# ==================== RELÓGIO DIGITAL ====================
agora = datetime.now()
hora_atual = agora.strftime("%H:%M:%S")

# Traduzir dia da semana
dias_semana = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}
dia_semana_pt = dias_semana.get(agora.strftime("%A"), agora.strftime("%A"))
data_formatada = agora.strftime(f"%d/%m/%Y - {dia_semana_pt}")

# Adicionar classe tema-futurista ao relógio se tema 4
classe_relogio = "tema-futurista" if tema_selecionado == "Tema 4: Futurista" else ""

st.markdown(f"""
    <div class="relogio-container {classe_relogio}">
        <div>
            <div class="relogio">{hora_atual}</div>
            <div class="data">{data_formatada}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.title("🔍 Sistema de Análise - Movimentos SAP 711/712")

# ==================== MENU DE NAVEGAÇÃO ====================
st.sidebar.markdown("---")
st.sidebar.title("📋 Menu de Navegação")
opcao_menu = st.sidebar.radio(
    "Selecione a funcionalidade:",
    ["🔍 Busca de Movimentos", "🔄 Análise de Materiais Duplicados"],
    index=0
)

st.sidebar.markdown("---")

# Upload do arquivo
st.sidebar.markdown("### 📤 Carregar Planilha")
uploaded_file = st.sidebar.file_uploader("Selecione o arquivo Excel", type=["xlsx", "xls"])

# ==================== FUNCIONALIDADE 1: BUSCA DE MOVIMENTOS ====================
if opcao_menu == "🔍 Busca de Movimentos":
    st.markdown("## 🔍 Busca de Movimentos")
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"✅ Arquivo carregado com sucesso! Total de {len(df)} registros.")
        except Exception as e:
            st.error(f"❌ Erro ao carregar o arquivo: {e}")
            st.stop()
        
        st.markdown("---")
        st.markdown("### 🔍 Buscar por Tipo de Movimento")
        
        col_movimento = None
        for col in df.columns:
            col_lower = str(col).lower()
            if any(palavra in col_lower for palavra in ['movimento', 'tpmv', 'bwart', 'tipo']):
                col_movimento = col
                break
        
        if col_movimento is None:
            col_movimento = df.columns[0]
        
        col_usuario = None
        for col in df.columns:
            col_lower = str(col).lower()
            if any(palavra in col_lower for palavra in ['usuario', 'user', 'nome', 'criado']):
                col_usuario = col
                break
        
        col_filtro1, col_filtro2 = st.columns([1, 2])
        
        with col_filtro1:
            tipo_movimento = st.selectbox(
                "Selecione o Tipo de Movimento *",
                options=["711", "712"],
                help="Escolha qual tipo de movimento deseja buscar"
            )
        
        with col_filtro2:
            if col_usuario:
                filtro_usuario = st.text_input(
                    "👤 Nome do Usuário (opcional)",
                    placeholder="Digite o nome do usuário ou deixe em branco",
                    help="Deixe em branco para buscar todos os usuários"
                )
            else:
                st.warning("⚠️ Coluna de usuário não identificada automaticamente")
                filtro_usuario = ""
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
        with col_btn1:
            buscar = st.button("🔍 BUSCAR", type="primary", use_container_width=True)
        with col_btn2:
            limpar = st.button("🔄 LIMPAR", use_container_width=True)
        
        if limpar:
            st.rerun()
        
        if buscar:
            try:
                df_resultado = df[df[col_movimento].astype(str).str.strip() == tipo_movimento].copy()
                filtros_aplicados = [f"Tipo Movimento = **{tipo_movimento}**"]
                
                if filtro_usuario and col_usuario:
                    df_resultado = df_resultado[
                        df_resultado[col_usuario].astype(str).str.contains(filtro_usuario, case=False, na=False)
                    ]
                    filtros_aplicados.append(f"Usuário contém **'{filtro_usuario}'**")
                
                st.markdown("---")
                st.markdown(f"### 📊 Resultados da Busca")
                
                if len(df_resultado) > 0:
                    st.success(f"✅ Encontrados **{len(df_resultado)}** registros")
                    
                    with st.expander("🔍 Filtros aplicados"):
                        for filtro in filtros_aplicados:
                            st.markdown(f"• {filtro}")
                    
                    col_material = None
                    col_data = None
                    col_montante = None
                    col_lote = None
                    col_qtd = None
                    col_texto = None
                    
                    for col in df.columns:
                        col_lower = str(col).lower().replace(" ", "").replace(".", "")
                        col_original = str(col).lower()
                        
                        if col_material is None and 'material' in col_lower and 'texto' not in col_lower and 'breve' not in col_lower:
                            col_material = col
                        elif col_data is None and any(palavra in col_lower for palavra in ['data', 'documento', 'budat', 'dtdoc']):
                            col_data = col
                        elif col_montante is None and any(palavra in col_original for palavra in ['montante', 'valor', 'qtd.em', 'quantidade em']):
                            col_montante = col
                        elif col_lote is None and ('lote' in col_lower or 'charg' in col_lower or 'batch' in col_lower):
                            col_lote = col
                        elif col_qtd is None and any(palavra in col_original for palavra in ['qtd.um', 'um registro', 'unidade medida']):
                            col_qtd = col
                        elif col_texto is None and any(palavra in col_original for palavra in ['texto breve', 'descrição', 'maktx', 'descr.material']):
                            col_texto = col
                    
                    colunas_exibir = [col_movimento]
                    nomes_exibir = ['Tipo Movimento']
                    
                    if col_usuario:
                        colunas_exibir.append(col_usuario)
                        nomes_exibir.append('Usuário')
                    
                    colunas_interesse = {
                        'Material': col_material,
                        'Data Documento': col_data,
                        'Montante em MI': col_montante,
                        'Lote': col_lote,
                        'Qtd. UM Registro': col_qtd,
                        'Texto Breve Material': col_texto
                    }
                    
                    for nome_campo, coluna_real in colunas_interesse.items():
                        if coluna_real:
                            colunas_exibir.append(coluna_real)
                            nomes_exibir.append(nome_campo)
                    
                    df_exibicao = df_resultado[colunas_exibir].copy()
                    df_exibicao.columns = nomes_exibir
                    
                    if 'Qtd. UM Registro' in df_exibicao.columns:
                        if pd.api.types.is_datetime64_any_dtype(df_exibicao['Qtd. UM Registro']):
                            df_exibicao['Qtd. UM Registro'] = df_exibicao['Qtd. UM Registro'].dt.strftime('%Y-%m-%d')
                    
                    st.dataframe(df_exibicao, use_container_width=True, height=400)
                    
                    soma_montante = 0
                    if col_montante:
                        try:
                            valores_montante = pd.to_numeric(df_resultado[col_montante], errors='coerce')
                            soma_montante = abs(valores_montante.sum())
                        except:
                            soma_montante = 0
                    
                    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                    with col_stat1:
                        st.metric("📋 Total de Registros", len(df_resultado))
                    with col_stat2:
                        if col_usuario:
                            st.metric("👥 Usuários Únicos", df_resultado[col_usuario].nunique())
                    with col_stat3:
                        if col_material:
                            st.metric("📦 Materiais Únicos", df_resultado[col_material].nunique())
                    with col_stat4:
                        if col_montante:
                            st.metric("💰 Total Montante em MI", f"{soma_montante:,.2f}")
                    
                    st.markdown("---")
                    st.markdown("### 📥 Exportar Resultados")
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_exibicao.to_excel(writer, index=False, sheet_name=f'Movimento_{tipo_movimento}')
                    output.seek(0)
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    nome_arquivo = f"movimento_{tipo_movimento}"
                    if filtro_usuario:
                        nome_arquivo += f"_usuario"
                    nome_arquivo += f"_{timestamp}.xlsx"
                    
                    st.download_button(
                        label=f"📥 Baixar Resultados em Excel",
                        data=output,
                        file_name=nome_arquivo,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                else:
                    st.warning(f"⚠️ Nenhum registro encontrado com os filtros aplicados")
            
            except Exception as e:
                st.error(f"❌ Erro ao processar a busca: {e}")
    
    else:
        st.info("📤 **Faça o upload do arquivo Excel** na barra lateral para começar")

# ==================== FUNCIONALIDADE 2: ANÁLISE DE MATERIAIS DUPLICADOS ====================
elif opcao_menu == "🔄 Análise de Materiais Duplicados":
    st.markdown("## 🔄 Análise de Materiais Duplicados entre 711 e 712")
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"✅ Arquivo carregado com sucesso! Total de {len(df)} registros.")
        except Exception as e:
            st.error(f"❌ Erro ao carregar o arquivo: {e}")
            st.stop()
        
        st.markdown("---")
        
        col_movimento = None
        for col in df.columns:
            col_lower = str(col).lower()
            if any(palavra in col_lower for palavra in ['movimento', 'tpmv', 'bwart', 'tipo']):
                col_movimento = col
                break
        
        if col_movimento is None:
            col_movimento = df.columns[0]
        
        col_material = None
        for col in df.columns:
            col_lower = str(col).lower().replace(" ", "").replace(".", "")
            if 'material' in col_lower and 'texto' not in col_lower and 'breve' not in col_lower:
                col_material = col
                break
        
        if col_material is None:
            st.error("❌ Não foi possível identificar a coluna de Material na planilha.")
            st.stop()
        
        st.info(f"📊 Analisando coluna: **{col_movimento}** (Movimento) e **{col_material}** (Material)")
        
        if st.button("🔍 ANALISAR MATERIAIS DUPLICADOS", type="primary", use_container_width=True):
            try:
                df_711 = df[df[col_movimento].astype(str).str.strip() == "711"]
                df_712 = df[df[col_movimento].astype(str).str.strip() == "712"]
                
                materiais_711 = set(df_711[col_material].dropna().astype(str).str.strip())
                materiais_712 = set(df_712[col_material].dropna().astype(str).str.strip())
                
                materiais_duplicados = materiais_711.intersection(materiais_712)
                
                st.markdown("---")
                st.markdown("### 📊 Resultados da Análise")
                
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                with col_stat1:
                    st.metric("📦 Materiais em 711", len(materiais_711))
                with col_stat2:
                    st.metric("📦 Materiais em 712", len(materiais_712))
                with col_stat3:
                    st.metric("🔄 Materiais Duplicados", len(materiais_duplicados))
                with col_stat4:
                    percentual = (len(materiais_duplicados) / max(len(materiais_711), 1)) * 100
                    st.metric("📊 % Duplicação", f"{percentual:.1f}%")
                
                if len(materiais_duplicados) > 0:
                    st.success(f"✅ Encontrados **{len(materiais_duplicados)}** materiais que aparecem tanto em 711 quanto em 712")
                    
                    materiais_duplicados_lista = sorted(list(materiais_duplicados))
                    df_duplicados = pd.DataFrame({'Material': materiais_duplicados_lista})
                    
                    col_texto = None
                    for col in df.columns:
                        col_original = str(col).lower()
                        if any(palavra in col_original for palavra in ['texto breve', 'descrição', 'maktx', 'descr.material']):
                            col_texto = col
                            break
                    
                    if col_texto:
                        descricoes = []
                        for material in materiais_duplicados_lista:
                            desc = df[df[col_material].astype(str).str.strip() == material][col_texto].iloc[0] if len(df[df[col_material].astype(str).str.strip() == material]) > 0 else ""
                            descricoes.append(desc)
                        df_duplicados['Descrição'] = descricoes
                    
                    st.markdown("### 📋 Lista de Materiais Duplicados")
                    st.dataframe(df_duplicados, use_container_width=True, height=400)
                    
                    st.markdown("---")
                    st.markdown("### 📥 Exportar Análise")
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_duplicados.to_excel(writer, index=False, sheet_name='Materiais_Duplicados')
                    output.seek(0)
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    st.download_button(
                        label="📥 Baixar Lista de Materiais Duplicados",
                        data=output,
                        file_name=f"materiais_duplicados_711_712_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    st.info("ℹ️ Não foram encontrados materiais que aparecem tanto em 711 quanto em 712")
            
            except Exception as e:
                st.error(f"❌ Erro ao processar análise: {e}")
    
    else:
        st.info("📤 **Faça o upload do arquivo Excel** na barra lateral para começar a análise")

# Rodapé
st.markdown(f"""
    <div class="footer">
        Programa desenvolvido por Djalma A Barbosa 2026. Todos os direitos reservados. ®
    </div>
""", unsafe_allow_html=True)