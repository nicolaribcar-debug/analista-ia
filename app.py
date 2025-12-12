import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import time

# --- 1. CONFIGURAÇÃO INICIAL (Obrigatório ser a primeira linha) ---
st.set_page_config(
    page_title="Analista IA - Enterprise",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS DE ELITE (A Mágica do Design) ---
st.markdown("""
<style>
    /* Importando fonte profissional (Roboto/Inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Fundo Geral */
    .stApp {
        background-color: #F4F6F9; /* Cinza gelo muito suave */
        font-family: 'Inter', sans-serif;
    }

    /* BARRA DE NAVEGAÇÃO SUPERIOR (NAVBAR) */
    .navbar {
        background-color: #0E1117; /* Preto/Azul Profundo */
        padding: 20px;
        border-radius: 0px 0px 15px 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .navbar h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    .navbar p {
        margin: 5px 0 0 0;
        font-size: 14px;
        color: #a0a0a0;
    }

    /* ESTILO DOS CARDS (CAIXAS BRANCAS) */
    .css-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }

    /* BOTÃO ESTILIZADO */
    .stButton>button {
        background-color: #2563EB; /* Azul Royal */
        color: white;
        border-radius: 8px;
        height: 50px;
        width: 100%;
        font-weight: 600;
        font-size: 16px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }

    /* LIMPEZA VISUAL */
    header {visibility: hidden;} /* Esconde a barra colorida padrão do topo */
    footer {visibility: hidden;} /* Esconde o rodapé */
    
    /* Ajuste de Texto */
    h2, h3 {color: #1F2937;}
    p {color: #4B5563;}
    
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE API (Secrets ou Manual) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # Fallback para teste local se não tiver secrets
    api_key = None

# --- 4. BARRA LATERAL (MENU) ---
with st.sidebar:
    st.markdown("### ⚙️ Painel de Controle")
    
    if not api_key:
        api_key = st.text_input("🔑 API Key (Google):", type="password")
        st.caption("Cole sua chave AIza... aqui se estiver rodando local.")
    
    st.info("💡 **Status:** Sistema Operacional")
    st.markdown("---")
    st.markdown("**Sobre:**")
    st.caption("Ferramenta de auditoria automatizada para investidores Buy Side. Utiliza LLMs para detectar riscos e validar teses.")
    st.markdown("---")
    st.caption("© 2025 Financial AI Ltd.")

# --- 5. CABEÇALHO PERSONALIZADO (HTML) ---
# Isso substitui o st.title padrão que estava sumindo
st.markdown("""
<div class="navbar">
    <h1>🏛️ Financial Intelligence AI</h1>
    <p>Auditoria Fundamentalista de Balanços Trimestrais</p>
</div>
""", unsafe_allow_html=True)

# --- 6. ÁREA PRINCIPAL ---

# Card de Upload (Container visual)
with st.container():
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("### 📂 Nova Análise")
    st.markdown("Faça o upload do **Release de Resultados (PDF)** para iniciar a auditoria.")
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

# Se não tiver arquivo, mostra instruções bonitas
if not uploaded_file:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="css-card"><h4>1. Upload Seguro</h4><p>Suba o PDF oficial da RI da empresa.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="css-card"><h4>2. Leitura Neural</h4><p>A IA extrai dados e ignora o marketing.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="css-card"><h4>3. Relatório Pro</h4><p>Receba análise de valuation e riscos.</p></div>', unsafe_allow_html=True)

# --- 7. PROCESSAMENTO E RESULTADO ---
if uploaded_file and api_key:
    # Mostra barra de status visual
    with st.status("🔍 Iniciando protocolos de análise...", expanded=True) as status:
        st.write("Leitura e extração de texto estruturado...")
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        st.write("Conectando ao modelo Gemini 2.5 Flash...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        status.update(label="Documento processado. Pronto para gerar.", state="complete", expanded=False)

    # Botão de Ação
    if st.button("GERAR RELATÓRIO DE INTELIGÊNCIA 🚀"):
        
        # Barra de progresso fake para dar sensação de trabalho pesado
        progress_text = "Auditando Balanço..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text="Processando indicadores e riscos...")
        my_bar.empty()

        # Prompt
        prompt = f"""
        ATUAR COMO: Senior Equity Research Analyst (Buy Side).
        TAREFA: Analise o release abaixo.

        GERE O RELATÓRIO EM MARKDOWN USANDO ESTES ÍCONES E FORMATO:

        # 🎯 Painel Executivo
        
        ### Veredito
        **NOTA (0-10):** [Nota]
        **RECOMENDAÇÃO:** [COMPRA / MANTER / VENDA]
        > *"[Resumo do veredito em 2 linhas impactantes]"*

        ---
        ### 📊 Indicadores Financeiros (Destaques)
        | Indicador | Valor Atual | Variação (YoY) |
        | :--- | :--- | :--- |
        | Receita Líquida | ... | ... |
        | EBITDA Ajustado | ... | ... |
        | Margem Líquida | ... | ... |
        | Dívida Líq/EBITDA | ... | ... |

        ---
        ### 🕵️ Auditoria de Riscos ("O que ninguém viu")
        * **Efeitos Não Recorrentes:** [Análise]
        * **Qualidade do Lucro:** [Análise]
        * **Geração de Caixa:** [Análise]

        ### 🗣️ Análise de Discurso da Gestão
        [Resumo cético do que o CEO disse]

        ---
        **TEXTO BASE:**
        {text[:50000]}
        """

        try:
            with st.spinner('Escrevendo relatório...'):
                response = model.generate_content(prompt)
            
            # Resultado dentro de um Card Branco ("Papel")
            st.markdown("---")
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.markdown("## 📑 Relatório Final")
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.warning("⚖️ Disclaimer: Análise gerada por IA. Não constitui recomendação de investimento.")

        except Exception as e:
            st.error(f"Erro na API: {e}")

elif uploaded_file and not api_key:
    st.error("⚠️ Chave de API não encontrada. Configure no Secrets ou na Barra Lateral."))

