import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import os

st.set_page_config(page_title="Busca Movimentos 711/712", layout="wide")

# CSS customizado para rodapé
st.markdown("""
    <style>
    /* Rodapé */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(240, 242, 246, 0.9);
        color: #666;
        text-align: center;
        padding: 10px;
        font-size: 11px;
        border-top: 1px solid #ddd;
        z-index: 999;
    }
    /* Espaçamento para o rodapé não sobrepor conteúdo */
    .main {
        padding-bottom: 60px;
    }
    </style>
""", unsafe_allow_html=True)

# Tentar carregar logos da pasta
try:
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar logo Petrobras
    possiveis_logos_petrobras = [
        'logo_petrobras.png',
        'logo petrobras.png',
        'petrobras.png',
        'logo_petrobras.jpg',
        'logo petrobras.jpg',
        'petrobras.jpg'
    ]
    
    logo_petrobras_path = None
    for nome_logo in possiveis_logos_petrobras:
        caminho = os.path.join(pasta_atual, nome_logo)
        if os.path.exists(caminho):
            logo_petrobras_path = caminho
            break
    
    # Buscar logo JSL
    possiveis_logos_jsl = [
        'logo_jsl.png',
        'logo jsl.png',
        'jsl.png',
        'logo_jsl.jpg',
        'logo jsl.jpg',
        'jsl.jpg'
    ]
    
    logo_jsl_path = None
    for nome_logo in possiveis_logos_jsl:
        caminho = os.path.join(pasta_atual, nome_logo)
        if os.path.exists(caminho):
            logo_jsl_path = caminho
            break
    
    # Exibir logos
    col_logo1, col_espaco, col_logo2 = st.columns([1, 3, 1])
    
    with col_logo1:
        if logo_petrobras_path:
            logo_petrobras = Image.open(logo_petrobras_path)
            st.image(logo_petrobras, width=120)
        else:
            st.markdown("<div style='font-size: 24px; font-weight: bold; color: #006699; opacity: 0.7;'>⛽ PETROBRAS</div>", unsafe_allow_html=True)
    
    with col_logo2:
        if logo_jsl_path:
            logo_jsl = Image.open(logo_jsl_path)
            st.image(logo_jsl, width=120)
        else:
            st.markdown("<div style='font-size: 24px; font-weight: bold; color: #FF6600; opacity: 0.7;'>🚛 JSL</div>", unsafe_allow_html=True)

except Exception as e:
    col_logo1, col_espaco, col_logo2 = st.columns([1, 3, 1])
    with col_logo1:
        st.markdown("<div style='font-size: 24px; font-weight: bold; color: #006699; opacity: 0.7;'>⛽ PETROBRAS</div>", unsafe_allow_html=True)
    with col_logo2:
        st.markdown("<div style='font-size: 24px; font-weight: bold; color: #FF6600; opacity: 0.7;'>🚛 JSL</div>", unsafe_allow_html=True)

st.title("🔍 Sistema de Análise - Movimentos SAP 711/712")

# Menu de navegação na sidebar
st.sidebar.title("📋 Menu de Navegação")
opcao_menu = st.sidebar.radio(
    "Selecione a funcionalidade:",
    ["🔍 Busca de Movimentos", "🔄 Análise de Materiais Duplicados"],
    index=0
)

st.sidebar.markdown("---")

# Upload do arquivo (comum para ambas as funcionalidades)
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
        
        # Identificar automaticamente a coluna de tipo de movimento
        col_movimento = None
        for col in df.columns:
            col_lower = str(col).lower()
            if any(palavra in col_lower for palavra in ['movimento', 'tpmv', 'bwart', 'tipo']):
                col_movimento = col
                break
        
        if col_movimento is None:
            col_movimento = df.columns[0]
        
        # Identificar coluna de usuário
        col_usuario = None
        for col in df.columns:
            col_lower = str(col).lower()
            if any(palavra in col_lower for palavra in ['usuario', 'user', 'nome', 'criado']):
                col_usuario = col
                break
        
        # Seleção do tipo de movimento
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
        
        # Botões de ação
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
        with col_btn1:
            buscar = st.button("🔍 BUSCAR", type="primary", use_container_width=True)
        with col_btn2:
            limpar = st.button("🔄 LIMPAR", use_container_width=True)
        
        if limpar:
            st.rerun()
        
        # Realizar busca
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
                    
                    # Identificar colunas
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
                    
                    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
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
                    
                    st.write("💡 **Sugestões:**")
                    st.write("• Verifique se digitou o nome do usuário corretamente")
                    st.write("• Tente usar apenas parte do nome")
                    st.write("• Deixe o campo de usuário em branco para ver todos")
            
            except Exception as e:
                st.error(f"❌ Erro ao processar a busca: {e}")
                st.error("Verifique se a planilha está no formato correto.")
    
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
        
        # Identificar coluna de movimento
        col_movimento = None
        for col in df.columns:
            col_lower = str(col).lower()
            if any(palavra in col_lower for palavra in ['movimento', 'tpmv', 'bwart', 'tipo']):
                col_movimento = col
                break
        
        if col_movimento is None:
            col_movimento = df.columns[0]
        
        # Identificar coluna de material
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
        
        # Botão para análise
        if st.button("🔍 ANALISAR MATERIAIS DUPLICADOS", type="primary", use_container_width=True):
            try:
                # Filtrar movimentos 711 e 712
                df_711 = df[df[col_movimento].astype(str).str.strip() == "711"]
                df_712 = df[df[col_movimento].astype(str).str.strip() == "712"]
                
                # Obter materiais únicos de cada movimento
                materiais_711 = set(df_711[col_material].dropna().astype(str).str.strip())
                materiais_712 = set(df_712[col_material].dropna().astype(str).str.strip())
                
                # Encontrar materiais em comum
                materiais_duplicados = materiais_711.intersection(materiais_712)
                
                st.markdown("---")
                st.markdown("### 📊 Resultados da Análise")
                
                # Estatísticas
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
                    
                    # Criar dataframe com materiais duplicados
                    materiais_duplicados_lista = sorted(list(materiais_duplicados))
                    df_duplicados = pd.DataFrame({
                        'Material': materiais_duplicados_lista
                    })
                    
                    # Adicionar informações adicionais se disponível
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
                    
                    # Exportar
                    st.markdown("---")
                    st.markdown("### 📥 Exportar Análise")
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_duplicados.to_excel(writer, index=False, sheet_name='Materiais_Duplicados')
                    output.seek(0)
                    
                    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
                    
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
        st.markdown("""
        ### 📖 Sobre esta funcionalidade:
        
        Esta análise identifica **materiais que aparecem tanto nos movimentos 711 quanto nos 712**.
        
        **O que você verá:**
        - Total de materiais únicos em cada movimento
        - Lista completa dos materiais duplicados
        - Percentual de duplicação
        - Opção de exportar a lista em Excel
        
        **Como usar:**
        1. Carregue o arquivo Excel na barra lateral
        2. Clique em "ANALISAR MATERIAIS DUPLICADOS"
        3. Visualize os resultados
        4. Exporte a lista se necessário
        """)

# Rodapé
st.markdown("""
    <div class="footer">
        Programa desenvolvido por Djalma A Barbosa 2026. Todos os direitos reservados. ®
    </div>
""", unsafe_allow_html=True)