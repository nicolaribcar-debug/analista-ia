import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA (VISUAL) ---
st.set_page_config(
    page_title="Analista IA Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed" # Começa fechado pra focar no app
)

# --- 2. CSS AVANÇADO (O BANHO DE LOJA) ---
st.markdown("""
<style>
    /* Fundo levemente cinza para destacar os cartões brancos */
    .stApp {background-color: #f0f2f6;}
    
    /* Botão Principal Estilizado */
    .stButton>button {
        background-color: #002B5B; /* Azul Navy */
        color: white;
        border-radius: 10px;
        height: 3.5em;
        width: 100%;
        font-weight: 700;
        font-size: 16px;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #004080;
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(0,0,0,0.2);
    }
    
    /* Estilo dos Containers (Cartões) */
    div[data-testid="stVerticalBlock"] > div {
        background-color: transparent;
    }
    
    /* Remover elementos padrões */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Títulos */
    h1 {color: #002B5B; font-family: 'Helvetica Neue', sans-serif;}
    h3 {color: #444;}
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE SEGURANÇA (API KEY) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # Se não achar no servidor (Secrets), tenta pegar da sidebar (para testes locais)
    with st.sidebar:
        st.warning("⚠️ Modo Local Detectado")
        api_key = st.text_input("Insira sua API Key manualmente:", type="password")

# --- 4. CABEÇALHO (HERO SECTION) ---
col1, col2 = st.columns([1, 4])
with col1:
    # Um logo ou ícone grande
    st.image("https://cdn-icons-png.flaticon.com/512/781/781760.png", width=80)
with col2:
    st.title("Financial Intelligence AI")
    st.markdown("**Auditoria de Balanços & Análise Fundamentalista Automatizada**")

st.markdown("---")

# --- 5. INSTRUÇÕES VISUAIS (SÓ APARECE SE NÃO TIVER ARQUIVO) ---
if "analise_feita" not in st.session_state:
    st.session_state.analise_feita = False

uploaded_file = st.file_uploader("📂 Arraste o PDF do Release de Resultados aqui", type="pdf")

if not uploaded_file:
    # Mostra 3 colunas explicando como funciona (pra não ficar vazio)
    st.markdown("### 🚀 Como funciona?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("1. Upload")
        st.markdown("Suba o **Release de Resultados** (PDF) da empresa listada na B3.")
    with c2:
        st.info("2. Processamento Neural")
        st.markdown("A IA lê cada linha, separa o marketing dos números e audita o texto.")
    with c3:
        st.info("3. Relatório Executivo")
        st.markdown("Receba uma análise de **Buy Side** com veredito, riscos e valuation.")

# --- 6. PROCESSAMENTO ---
if uploaded_file and api_key:
    # Container Branco para o status
    with st.container():
        st.success(f"📄 Documento identificado: {uploaded_file.name}")
        
        if st.button("GERAR RELATÓRIO DE INTELIGÊNCIA 📊"):
            
            # Barra de progresso visual
            progress_text = "Iniciando protocolos de análise..."
            my_bar = st.progress(0, text=progress_text)
            
            try:
                # Leitura
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                my_bar.progress(30, text="Lendo dados contábeis...")
                
                # Configuração IA
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("models/gemini-2.5-flash") # O melhor modelo
                
                my_bar.progress(60, text="Auditando indicadores financeiros (EBITDA, Dívida, Margens)...")
                
                # Prompt Otimizado para Markdown Visual
                prompt = f"""
                ATUAR COMO: Senior Equity Research Analyst (Buy Side).
                TAREFA: Analise o Release de Resultados abaixo.
                
                GERAR RESPOSTA ESTRITAMENTE NESTE FORMATO MARKDOWN:

                # 📊 Painel Executivo
                
                ## 🎯 Veredito
                **NOTA (0-10):** [Nota]
                **RECOMENDAÇÃO:** [COMPRA / MANTER / VENDA]
                > *"[Resumo do veredito em uma frase de impacto]"*

                ---
                ## 💎 Destaques Financeiros (YoY)
                | Indicador | Valor Atual | Variação % |
                | :--- | :--- | :--- |
                | Receita Líquida | ... | ... |
                | EBITDA | ... | ... |
                | Margem Líquida | ... | ... |
                | Dívida Líq/EBITDA | ... | ... |

                ---
                ## 🔎 Auditoria de Riscos & "Maquiagem"
                * **Efeitos Não Recorrentes:** [Análise]
                * **Qualidade do Lucro:** [Análise]
                * **Geração de Caixa:** [Análise]

                ## 🗣️ Tradução do Management
                [Análise cética do discurso da diretoria]

                ---
                **DADOS EXTRAÍDOS DO PDF:**
                {text[:50000]}
                """
                
                response = model.generate_content(prompt)
                
                my_bar.progress(100, text="Concluído!")
                time.sleep(0.5)
                my_bar.empty() # Some com a barra
                
                # --- 7. EXIBIÇÃO DO RELATÓRIO (COM CONTAINER ESTILIZADO) ---
                st.markdown("---")
                
                # Container com fundo branco e borda arredondada (Simula uma folha A4)
                with st.container():
                    st.markdown("""
                    <div style="background-color: white; padding: 30px; border-radius: 15px; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(response.text)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Disclaimer Final
                st.markdown("###")
                st.warning("⚖️ **Disclaimer:** Esta ferramenta utiliza IA para fins educacionais. Não é recomendação de investimento (CVM).")

            except Exception as e:
                st.error(f"Erro no processamento: {e}")

elif not api_key:
    st.error("⚠️ Erro Crítico: Chave de API não configurada no Sistema.")
