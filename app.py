import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Analista IA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO VISUAL ---
st.markdown("""
<style>
    .stButton>button {
        background-color: #004080;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #003366;
        transform: translateY(-2px);
    }
    footer {visibility: hidden;}
    .stTextInput>div>div>input {border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔐 Acesso")
    st.markdown("---")
    
    # Única coisa que o usuário precisa preencher
    api_key = st.text_input("Sua Chave Google API:", type="password")
    
    st.markdown("###")
    st.info("ℹ️ **Como funciona:** O sistema utiliza o motor neural *Gemini 2.5 Flash* para ler documentos contábeis complexos em segundos.")
    
    st.divider()
    st.caption("v1.1 | Enterprise Edition")

# --- CORPO PRINCIPAL ---
st.title("📊 Financial Intelligence AI")
st.markdown("#### Análise Fundamentalista de Balanços Trimestrais")
st.markdown("---")

# Definição Silenciosa do Modelo (O usuário não vê, mas o código usa o melhor)
MODELO_ESCOLHIDO = "models/gemini-2.5-flash"

uploaded_file = st.file_uploader("📂 Arraste o Release de Resultados (PDF) aqui", type="pdf")

if uploaded_file and api_key:
    with st.status("Processando documento...", expanded=True) as status:
        try:
            st.write("Leitura do arquivo PDF...")
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            st.write("Conectando ao motor neural...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(MODELO_ESCOLHIDO)
            
            status.update(label="Pronto para análise!", state="complete", expanded=False)
            
            st.markdown("###")
            if st.button("GERAR RELATÓRIO DE INTELIGÊNCIA 🚀"):
                
                with st.spinner('Examinando indicadores financeiros...'):
                    prompt = f"""
                    ATUAR COMO: Senior Equity Research Analyst (Buy Side).
                    TAREFA: Analise o texto financeiro abaixo e gere um relatório executivo.
                    
                    FORMATO DE SAÍDA (Markdown):
                    
                    ## 🎯 Veredito Executivo
                    **Nota (0-10):** [Nota]
                    **Recomendação:** [COMPRA / NEUTRO / VENDA]
                    > *[Justificativa em itálico e direta em 2 linhas]*

                    ---
                    ## 📊 Indicadores Chave (YoY)
                    | Indicador Financeiro | Valor Atual | Variação % |
                    | :--- | :--- | :--- |
                    | Receita Líquida | ... | ... |
                    | EBITDA Ajustado | ... | ... |
                    | Margem Líquida | ... | ... |
                    | Dívida Líq/EBITDA | ... | ... |

                    ---
                    ## 🔎 Auditoria de Qualidade
                    * **Efeitos Não Recorrentes:** [Análise crítica]
                    * **Qualidade do Lucro:** [Operacional vs Contábil]
                    * **Geração de Caixa:** [Análise do FCO]

                    ## 🗣️ Análise de Discurso (Management)
                    [Resuma o tom da diretoria com ceticismo profissional]

                    ---
                    **DADOS BRUTOS:**
                    {text}
                    """
                    
                    try:
                        response = model.generate_content(prompt)
                        
                        st.markdown("---")
                        st.subheader("📑 Relatório de Análise Fundamentalista")
                        
                        with st.container():
                            st.markdown(response.text)
                        
                        st.markdown("---")
                        st.warning("⚖️ **Disclaimer:** Ferramenta de análise automatizada. Não constitui recomendação de investimento.")
                        
                    except Exception as e:
                        st.error(f"Erro de conexão com API: {e}")
                        
        except Exception as e:
            st.error(f"Erro na leitura do PDF: {e}")

elif not api_key:
    st.info("👈 Insira sua Chave de API no menu lateral para liberar o sistema.")
