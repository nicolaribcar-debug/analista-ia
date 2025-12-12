import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import time
import re

# --- 1. CONFIGURAÇÃO INICIAL E METADADOS ---
st.set_page_config(
    page_title="Financial Analyst AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- 2. CSS DE NAVEGAÇÃO E ESTILO (O SEGREDO DA NAV-BAR) ---
st.markdown("""
<style>
    /* ---------------------------------------------------- */
    /* 1. ESTILO GERAL E FONTES */
    /* ---------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background-color: #F8F9FA; /* Fundo cinza suave (Fintech) */
        font-family: 'Inter', sans-serif;
    }
    
    /* ---------------------------------------------------- */
    /* 2. BARRA DE NAVEGAÇÃO SUPERIOR (Navbar) */
    /* ---------------------------------------------------- */
    .navbar {
        background-color: #002B5B; /* Azul Institucional Escuro */
        padding: 10px 0;
        color: white;
        margin: -20px -20px 30px -20px; /* Hack para ocupar a largura total */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        width: calc(100% + 40px);
    }
    .navbar-content {
        padding-left: 30px;
        padding-right: 30px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .navbar h1 {
        margin: 0;
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
    }
    .navbar p {
        margin: 0;
        font-size: 14px;
        color: #A0A0A0;
    }
    
    /* ---------------------------------------------------- */
    /* 3. ELEMENTOS INTERATIVOS E LIMPEZA */
    /* ---------------------------------------------------- */
    /* Esconder o cabeçalho e rodapé Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Botão Principal Estilizado */
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

    /* Estilo do container de upload para parecer um card */
    [data-testid="stFileUploader"] {
        border: 2px dashed #D1D5DB;
        border-radius: 8px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Estilo dos Cartões de Métrica */
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #004D99; /* Barra de cor sutil */
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
</style>
""", unsafe_allow_html=True)

# --- INJEÇÃO DA BARRA DE NAVEGAÇÃO ---
st.markdown(
    """
    <div class="navbar">
        <div class="navbar-content">
            <h1>💎 Financial Intelligence AI</h1>
            <p>Auditoria & Research</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --- 3. LÓGICA DE API (SECRETS) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = None

# --- BARRA LATERAL (Informativa) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/781/781760.png", width=60)
    st.title("Painel de Controle")
    st.caption("Sistema de Auditoria de Balanços.")
    
    if not api_key:
        st.warning("⚠️ Chave de API não configurada. Insira manualmente:")
        # Aqui, se o usuário não tiver acesso, ele pode tentar novamente
        api_key = st.text_input("API Key (Manual):", type="password")
    else:
        st.success("✅ Sistema operacional.")
    
    st.divider()
    st.info("💡 **Dica:** Use o menu (⋮) para mudar para o Modo Escuro (Dark Mode).")


# --- 4. ÁREA PRINCIPAL ---

# Destaques visuais para a ação
st.subheader("Análise Fundamentalista Automatizada")
st.markdown("Arraste o documento **Release de Resultados (ITR/DFP)** para iniciar a auditoria neural.")

# Layout de Upload (sem o container extra para simplificar)
uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")


# --- 5. LÓGICA DE PROCESSAMENTO ---
if uploaded_file and api_key:
    
    # Validação do limite de uso
    if 'limite_excedido' in st.session_state and st.session_state.limite_excedido:
        st.error("🚨 Limite de uso do Gemini excedido. Tente novamente mais tarde ou insira uma nova chave.")
        st.stop()
        
    # Status visual de análise
    with st.status("🔍 Analisando documento...", expanded=True) as status:
        try:
            st.write("Extraindo texto do PDF...")
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            st.write("Configurando motor neural...")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            
            status.update(label="Documento pronto. Clique para gerar o relatório.", state="complete", expanded=False)

        except Exception as e:
            st.session_state.limite_excedido = True
            st.error(f"⚠️ Erro na API (Limite/Chave Inválida): {e}")
            st.stop()


    # Botão de Ação
    st.markdown("###")
    if st.button("GERAR RELATÓRIO EXECUTIVO 🚀"):
        
        # Simulação de Carregamento
        my_bar = st.progress(0, text="Auditando Balanço...")
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text="Processando indicadores e riscos...")
        my_bar.empty()

        # Prompt
        prompt = f"""
        ATUAR COMO: Senior Equity Research Analyst (Buy Side) com foco em detecção de risco. Sua missão é fornecer uma análise concisa, crítica e bem estruturada para um investidor.

        GERE O RELATÓRIO EM MARKDOWN USANDO O SEGUINTE FORMATO:

        ## 🎯 Veredito Executivo
        **NOTA (0-10):** [Nota]
        **RECOMENDAÇÃO:** [COMPRA / MANTER / VENDA]
        > *"[Justificativa concisa em 2 linhas]"*

        ---
        ## 📊 Indicadores Financeiros (Tabela com Destaques)
        | Indicador | Valor Atual | Variação (YoY) |
        | :--- | :--- | :--- |
        | Receita Líquida | ... | ... |
        | EBITDA Ajustado | ... | ... |
        | Margem Líquida | ... | ... |
        | Dívida Líq/EBITDA | ... | ... |

        ---
        ## 🕵️ Auditoria de Risco & Qualidade do Lucro
        * **Efeitos Não Recorrentes:** [Análise detalhada sobre itens não-caixa ou pontuais]
        * **Qualidade do Lucro:** [O lucro é operacional ou contábil? Fundamente a resposta]
        * **Fluxo de Caixa:** [A empresa gerou caixa (FCO) ou dependeu de financiamento?]

        ## 🗣️ Análise de Discurso (Management)
        [Resumo cético do que o CEO disse, destacando os desafios que foram suavizados]

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
            
            # Extração de Métricas (Para Cartões de Destaque)
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
            st.subheader("📑 Relatório Detalhado")
            st.markdown(relatorio)

            st.warning("⚖️ Disclaimer: Análise gerada por IA. Não constitui recomendação de investimento.")

        except Exception as e:
            st.error(f"Erro na API: {e}")

elif uploaded_file and not api_key:
    st.error("⚠️ Chave de API não configurada. Por favor, insira no menu lateral (Sidebar).")

elif not uploaded_file:
    # Instruções visuais de como usar o site
    st.info("O site está pronto para uso! Após resolver o limite da API, insira o PDF e gere seu primeiro relatório.")
