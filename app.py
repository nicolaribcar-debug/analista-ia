import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import time
import re
import os

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(
    page_title="Financial Analyst AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- 2. CSS DE ESTABILIDADE E CONTRASTE (O FIX FINAL) ---
st.markdown("""
<style>
    /* ---------------------------------------------------- */
    /* 1. ESTILO GERAL E FONTES */
    /* ---------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background-color: #F8F9FA; /* Fundo cinza suave */
        font-family: 'Inter', sans-serif;
    }
    
    /* FIX: Garante que o texto seja legível (preto) no modo claro */
    body, p, h1, h2, h3, h4, .stText {
        color: #333333; 
    }
    
    /* ---------------------------------------------------- */
    /* 2. BARRA DE NAVEGAÇÃO SUPERIOR (Navbar) */
    /* ---------------------------------------------------- */
    .navbar {
        background-color: #002B5B; /* Azul Institucional Forte */
        padding: 15px 0;
        margin: -20px -20px 30px -20px; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        width: 100vw; 
    }
    .navbar-content {
        max-width: 1200px; 
        margin: auto;
        padding: 0 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .navbar h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .navbar p {
        margin: 0;
        font-size: 14px;
        color: #A0A0A0;
    }
    
    /* ---------------------------------------------------- */
    /* 3. ELEMENTOS E CARDS */
    /* ---------------------------------------------------- */
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #004D99; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .stButton>button {
        background-color: #007bff; 
        color: white;
        border-radius: 8px;
        height: 55px;
        width: 100%;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }

    [data-testid="stFileUploader"] {
        border: 2px dashed #D1D5DB;
        border-radius: 8px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Limpeza */
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- INJEÇÃO DA BARRA DE NAVEGAÇÃO ---
st.markdown(
    """
    <div class="navbar">
        <div class="navbar-content">
            <h1><span style="color: #FFD700;">💎</span> Financial Intelligence AI</h1>
            <p>Auditoria & Research</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 3. LÓGICA DE API (SECRETS) ---
try:
    api_key = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]
except:
    api_key = None

if 'limite_excedido' not in st.session_state:
    st.session_state.limite_excedido = False

# --- BARRA LATERAL (Controles) ---
with st.sidebar:
    st.title("Painel de Controle")
    st.caption("Acesso ao motor de análise neural.")
    st.divider()
    
    if not api_key:
        st.warning("⚠️ Chave de Servidor não encontrada.")
        api_key = st.text_input("🔑 API Key (Manual):", type="password")
    else:
        st.success("✅ Servidor Operacional (Chave carregada).")
    
    st.divider()
    st.info("💡 **Dica:** O sistema usa o modelo Gemini 2.5 Flash, ideal para volumes grandes de dados.")
    st.caption("© 2025 Financial AI Ltd.")


# --- 4. ÁREA PRINCIPAL ---
st.subheader("Análise Fundamentalista Automatizada")
st.markdown("Arraste o documento **Release de Resultados (ITR/DFP)** para iniciar a auditoria neural.")

uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")


# --- INÍCIO DA LÓGICA DE PROCESSAMENTO ---
if uploaded_file:
    if not api_key:
        st.error("🚨 Chave de API não configurada. Por favor, insira a chave no painel lateral para liberar o sistema.")
    
    elif st.session_state.limite_excedido:
        st.error("🚨 Limite de uso da API excedido. Tente novamente mais tarde ou insira uma chave válida no painel lateral.")
        
    else:
        # --- Lógica de Leitura e Configuração ---
        with st.status("🔍 Iniciando protocolos de análise...", expanded=True) as status:
            try:
                st.write("Extraindo texto do PDF...")
                reader = PdfReader(uploaded_file)
                text = "".join(page.extract_text() for page in reader.pages)
                
                st.write("Configurando motor neural...")
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("models/gemini-2.5-flash")
                
                status.update(label="Documento processado. Clique para gerar o relatório.", state="complete", expanded=False)

            except Exception as e:
                st.error(f"⚠️ Erro Crítico durante a leitura ou configuração: {e}")
                st.stop()

        # Botão de Ação
        st.markdown("###")
        if st.button("GERAR RELATÓRIO EXECUTIVO 🚀"):
            
            # Simulação de Carregamento (UX)
            my_bar = st.progress(0, text="Auditando Balanço...")
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text="Processando indicadores e riscos...")
            my_bar.empty()

            # O PROMPT FINAL É GERADO AQUI
            try:
                from analyst_prompt import gerar_prompt_final
                prompt_final = gerar_prompt_final(text)
            except ImportError:
                st.error("ERRO: Arquivo 'analyst_prompt.py' não encontrado. Recarregue o código.")
                st.stop()

            try:
                with st.spinner('Gerando o relatório...'):
                    response = model.generate_content(prompt_final)
                
                relatorio = response.text
                st.session_state.limite_excedido = False 
                
                # --- EXIBIÇÃO AVANÇADA DO RESULTADO (Cartões de Métrica) ---
                st.markdown("---")
                
                # Regex para extrair nota e recomendação
                nota_match = re.search(r'\*\*NOTA \(0-10\):\*\* (\d+)', relatorio)
                rec_match = re.search(r'\*\*RECOMENDAÇÃO:\*\* (COMPRA|MANTER|VENDA)', relatorio)
                
                if nota_match and rec_match:
                    nota = nota_match.group(1)
                    recomendacao = rec_match.group(1)
                    
                    c1, c2, c3 = st.columns(3)
                    
                    with c1: st.metric("Nota do Analista", f"{nota}/10", delta_color="off")
                    with c2: st.metric("Recomendação", recomendacao)
                    with c3: st.metric("Motor de Análise", "Gemini 2.5 Flash")
                
                # Relatório Detalhado
                st.markdown("---")
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("📑 Relatório Detalhado")
                st.markdown(relatorio)
                st.markdown('</div>', unsafe_allow_html=True)

                st.warning("⚖️ Disclaimer: Análise gerada por IA. Não constitui recomendação de investimento.")

            except Exception as e:
                st.session_state.limite_excedido = True
                st.error(f"🚨 Erro de Execução: {e}")

elif not uploaded_file:
    st.info("O sistema está online. Insira o PDF para gerar seu primeiro relatório de auditoria.")
    
