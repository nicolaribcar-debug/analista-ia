import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Analista IA",
    page_icon="📊",
    layout="wide"
)

# --- ESTILO VISUAL (CORREÇÃO DE CONTRASTE) ---
st.markdown("""
<style>
    /* CSS para o Botão (Mantido) */
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

    /* CORREÇÃO CRÍTICA DO CARD (Garante contraste e estabilidade) */
    .intro-card {
        background-color: var(--secondary-background-color); /* Usa a cor de fundo do Streamlit (muda com o tema) */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color); /* Usa a cor de borda do tema */
        min-height: 150px;
        text-align: center;
    }
    .intro-card h4 {
        color: var(--text-color); /* Usa a cor do texto do tema */
        font-weight: 600;
        margin-top: 5px;
    }
    .intro-card p {
        color: var(--text-color); /* Garante que o parágrafo também use a cor do tema */
    }
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

# --- NOVA SEÇÃO: 3 TÓPICOS EM CARDS SEPARADOS ---
st.markdown("### Sobre o Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    # Atenção: O texto dentro do card agora é texto simples (Markdown), não HTML, para herdar a cor nativa.
    st.markdown("""
        <div class="intro-card">
            <h4>1. Auditoria Neural</h4>
            <p>Utilizamos o motor Gemini 2.5 de alta capacidade para ler e interpretar centenas de páginas de relatórios complexos em segundos.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="intro-card">
            <h4>2. Foco Cético (Risco)</h4>
            <p>A IA é treinada para ignorar o marketing do CEO e focar em discrepâncias: lucro contábil vs. geração de caixa operacional.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="intro-card">
            <h4>3. Relatórios Executivos</h4>
            <p>Entregamos o veredito (COMPRA/VENDA/MANTER) e a justificativa em formato profissional, pronto para sua decisão.</p>
        </div>
    """, unsafe_allow_html=True)

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
