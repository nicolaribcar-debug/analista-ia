import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Analista IA Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded" # Força a barra lateral a começar aberta
)

# --- ESTILO VISUAL (CSS SEGURO) ---
st.markdown("""
<style>
    /* Estilo do Botão Principal (Azul Profissional) */
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
        box-shadow: 0px 6px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Apenas esconde o rodapé "Made with Streamlit", mas mantém o menu superior */
    footer {visibility: hidden;}
    
    /* Melhoria nas caixas de texto */
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (Sidebar) ---
with st.sidebar:
    st.header("⚙️ Painel de Controle")
    st.markdown("---")
    
    api_key = st.text_input("🔑 Chave Google API:", type="password")
    
    st.markdown("### Configurações da IA")
    # Seletor Manual (Segurança Máxima)
    model_options = [
        "models/gemini-2.5-flash", 
        "models/gemini-2.0-flash",
        "models/gemini-pro"
    ]
    model_name = st.selectbox("Motor de Análise:", model_options)
    
    st.info("💡 **Dica:** O modelo '2.5-flash' é o mais rápido para balanços.")
    st.divider()
    st.caption("v1.0.0 | Enterprise Edition")

# --- CORPO PRINCIPAL ---

st.title("📊 Financial Intelligence AI")
st.markdown("#### Análise Fundamentalista de Balanços Trimestrais")
st.markdown("---")

# Área de Upload
uploaded_file = st.file_uploader("📂 Arraste o Release de Resultados (PDF) aqui", type="pdf")

if uploaded_file and api_key:
    # Container de Status visualmente agradável
    with st.status("Processando documento...", expanded=True) as status:
        try:
            st.write("Leitura do arquivo PDF...")
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            st.write(f"✅ Arquivo lido: {len(reader.pages)} páginas extraídas.")
            
            st.write("Conectando ao motor neural do Google...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            status.update(label="Documento pronto! Clique no botão abaixo.", state="complete", expanded=False)
            
            # Botão de Ação Azul
            st.markdown("###")
            if st.button("GERAR RELATÓRIO DE INTELIGÊNCIA 🚀"):
                
                with st.spinner('O Analista Virtual está examinando os números...'):
                    # PROMPT DE ELITE
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
                        
                        # Exibição do Resultado
                        st.markdown("---")
                        st.subheader("📑 Relatório de Análise Fundamentalista")
                        
                        # Container branco/cinza para destacar o texto
                        with st.container():
                            st.markdown(response.text)
                        
                        st.markdown("---")
                        st.warning("⚖️ **Disclaimer:** Ferramenta de análise automatizada. Não constitui recomendação de investimento.")
                        
                    except Exception as e:
                        st.error(f"Erro de conexão com API: {e}")
                        
        except Exception as e:
            st.error(f"Erro na leitura do PDF: {e}")

elif not api_key:
    st.info("👈 Para começar, insira sua Chave de API no painel lateral.")