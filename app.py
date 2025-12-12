import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Analista IA",
    page_icon="📊",
    layout="wide"
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
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Agora só informativa) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3309/3309991.png", width=50)
    st.header("Financial AI")
    st.info("ℹ️ **Sistema Autônomo:** Este software utiliza processamento neural avançado para auditar balanços automaticamente.")
    st.divider()
    st.caption("Enterprise Edition v2.0")

# --- CORPO PRINCIPAL ---
st.title("📊 Financial Intelligence AI")
st.markdown("#### Análise Fundamentalista de Balanços Trimestrais")
st.markdown("---")

# --- NOVA SEÇÃO: 3 TÓPICOS SOBRE O SITE ---
st.markdown("### Sobre o Sistema")
st.markdown("""
Esta ferramenta foi desenvolvida para acelerar a análise de mercado e focar no que realmente importa:
* **Auditoria Neural:** Utilizamos o motor Gemini 2.5 para ler e interpretar centenas de páginas de relatórios complexos.
* **Foco Cético:** A IA é treinada para ignorar o marketing e buscar por discrepâncias entre lucro contábil e geração de caixa.
* **Relatórios Executivos:** Entregamos o veredito (COMPRA/VENDA/MANTER) e a justificativa em formato profissional, pronto para sua decisão.
""")
st.markdown("---")
# --- FIM DA NOVA SEÇÃO ---


# --- CONFIGURAÇÃO AUTOMÁTICA DA IA (O SEGREDO) ---
# Aqui ele tenta pegar a chave do cofre do Streamlit
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ Erro de Configuração: Chave de API não encontrada no servidor.")
    st.stop()

# Modelo fixo no melhor disponível
MODELO_ESCOLHIDO = "models/gemini-2.5-flash"

# --- ÁREA DE UPLOAD ---
uploaded_file = st.file_uploader("📂 Arraste o Release de Resultados (PDF) aqui", type="pdf")

if uploaded_file:
    with st.status("Iniciando protocolos de análise...", expanded=True) as status:
        try:
            st.write("Extraindo dados do documento...")
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            st.write("Conectando ao motor neural...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(MODELO_ESCOLHIDO)
            
            status.update(label="Análise pronta para geração!", state="complete", expanded=False)
            
            st.markdown("###")
            if st.button("GERAR RELATÓRIO DE INTELIGÊNCIA 🚀"):
                
                with st.spinner('Processando indicadores financeiros e auditoria de texto...'):
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
