import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import time
import re

# --- 1. CONFIGURAÇÃO INICIAL (LAYOUT WIDE É PROFISSIONAL) ---
st.set_page_config(
    page_title="Financial Analyst AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- 2. CSS SIMPLES E SEGURO (Apenas botão e rodapé) ---
st.markdown("""
<style>
    /* Estilo do Botão Principal */
    .stButton>button {
        background-color: #007bff; 
        color: white;
        border-radius: 8px;
        height: 55px;
        width: 100%;
        font-weight: 600;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    
    /* Esconder o rodapé (Única interferência de design) */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE API (SECRETS) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = None

# --- BARRA LATERAL (Informativa) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/781/781760.png", width=60)
    st.title("Financial AI")
    st.caption("Sistema de Auditoria de Balanços.")
    
    if not api_key:
        st.warning("⚠️ Chave de API não encontrada.")
        api_key = st.text_input("API Key (Manual):", type="password")
    else:
        st.success("✅ Sistema operacional.")
    
    st.divider()
    # Este é o Dark Mode/Light Mode nativo!
    st.info("💡 **Dica:** Use o menu (⋮) no canto superior direito para mudar para o **Modo Escuro (Dark Mode)**.")


# --- 4. CABEÇALHO E UPLOAD ---
st.title("Financial Intelligence AI")
st.markdown("#### Auditoria de Balanços & Análise Fundamentalista Automatizada")
st.markdown("---")

# Card de Upload (Usando container nativo, que é seguro)
with st.container(border=True): # O border=True cria uma caixa nativa!
    st.markdown("### 📂 Iniciar Nova Análise")
    uploaded_file = st.file_uploader("Arraste o Release de Resultados (PDF) aqui", type="pdf", label_visibility="collapsed")


# --- 5. LÓGICA DE PROCESSAMENTO ---
if uploaded_file and api_key:
    
    with st.status("🔍 Analisando documento...", expanded=True) as status:
        st.write("Extraindo texto do PDF...")
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        st.write("Configurando motor neural...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        status.update(label="Documento pronto. Clique para gerar o relatório.", state="complete", expanded=False)

    if st.button("GERAR RELATÓRIO EXECUTIVO"):
        
        # Simulação de Carregamento
        my_bar = st.progress(0, text="Auditando Balanço...")
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text="Processando indicadores e riscos...")
        my_bar.empty()

        # Prompt
        prompt = f"""
        ATUAR COMO: Senior Equity Research Analyst (Buy Side). Sua missão é fornecer uma análise concisa, crítica e bem estruturada para um investidor.

        GERE O RELATÓRIO EM MARKDOWN USANDO O SEGUINTE FORMATO:

        ## 🎯 Veredito Executivo
        **NOTA (0-10):** [Nota]
        **RECOMENDAÇÃO:** [COMPRA / MANTER / VENDA]
        > *"[Justificativa concisa em 2 linhas]"*

        ---
        ## 📊 Indicadores Financeiros (Destaques)
        | Indicador | Valor Atual | Variação (YoY) |
        | :--- | :--- | :--- |
        | Receita Líquida | ... | ... |
        | EBITDA Ajustado | ... | ... |
        | Margem Líquida | ... | ... |
        | Dívida Líq/EBITDA | ... | ... |

        ---
        ## 🔎 Auditoria de Riscos
        * **Efeitos Não Recorrentes:** [Análise]
        * **Qualidade do Lucro:** [Operacional vs Contábil]
        * **Geração de Caixa:** [Análise FCO]

        ## 🗣️ Análise do Discurso
        [Resumo cético do que o Management disse]

        ---
        **DADOS BASE:**
        {text[:50000]}
        """

        try:
            with st.spinner('Gerando o relatório...'):
                response = model.generate_content(prompt)
            
            relatorio = response.text
            
            # --- EXIBIÇÃO AVANÇADA DO RESULTADO ---
            st.markdown("---")
            
            # 1. Cartões de Destaque
            nota_match = re.search(r'\*\*NOTA \(0-10\):\*\* (\d+)', relatorio)
            rec_match = re.search(r'\*\*RECOMENDAÇÃO:\*\* (COMPRA|MANTER|VENDA)', relatorio)
            
            if nota_match and rec_match:
                nota = nota_match.group(1)
                recomendacao = rec_match.group(1)
                
                c1, c2, c3 = st.columns(3)
                
                with c1: st.metric("Nota do Analista", f"{nota}/10", delta_color="off")
                with c2: st.metric("Recomendação", recomendacao)
                with c3: st.metric("Modelo de IA", "Gemini 2.5")
            
            # 2. Relatório Detalhado
            st.markdown("---")
            st.subheader("📑 Relatório Detalhado")
            st.markdown(relatorio)

            st.warning("⚖️ Disclaimer: Análise gerada por IA. Não constitui recomendação de investimento.")

        except Exception as e:
            st.error(f"Erro na API: {e}")

elif uploaded_file and not api_key:
    st.error("⚠️ Chave de API não encontrada. Por favor, insira no menu lateral (Sidebar).")
