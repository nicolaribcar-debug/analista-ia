import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import time
import re # Para extrair a nota e o veredito do relatório

# --- 1. CONFIGURAÇÃO INICIAL ---
st.set_page_config(
    page_title="Financial Analyst AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS DE LIMPEZA E ESTILO FINTECH ---
st.markdown("""
<style>
    /* Fundo Geral - Mais limpo */
    .stApp {
        background-color: #F8F9FA; /* Cinza muito claro */
        font-family: 'Inter', sans-serif;
    }
    
    /* Remover elementos padrão (para não parecer Streamlit) */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Título Principal Limpo */
    .css-1ht1c9b { /* Seletor específico para o título principal do Streamlit */
        color: #004D99; /* Azul Corporativo */
        font-weight: 700;
        margin-bottom: 5px;
        padding-top: 20px;
    }
    
    /* Cartões de Conteúdo (Containers Brancos com Sombra) */
    .css-card {
        background-color: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Sombra suave */
        border: 1px solid #e9ecef; /* Borda finíssima */
        margin-bottom: 20px;
        min-height: 150px;
    }

    /* Botão Principal Estilizado (Azul Limpo) */
    .stButton>button {
        background-color: #007bff; /* Azul padrão clean */
        color: white;
        border-radius: 8px;
        height: 55px;
        width: 100%;
        font-weight: 600;
        font-size: 16px;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Estilo para Tabela (Relatório) */
    table {
        font-size: 14px;
    }
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
    st.header("Financial AI")
    st.caption("Sistema de Auditoria de Balanços.")
    
    if not api_key:
        st.warning("⚠️ Chave de API não configurada. Insira manualmente:")
        api_key = st.text_input("API Key:", type="password")
    else:
        st.success("✅ Sistema operacional.")

# --- 4. CABEÇALHO E UPLOAD ---
st.title("Financial Intelligence AI")
st.markdown("Auditoria de Balanços & Análise Fundamentalista Automatizada")
st.markdown("---")

# Card de Upload (Centralizado e limpo)
with st.container():
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.markdown("### 📂 Iniciar Nova Análise")
    uploaded_file = st.file_uploader("Arraste o Release de Resultados (PDF) aqui", type="pdf", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. LÓGICA DE PROCESSAMENTO ---
if uploaded_file and api_key:
    
    # --- Passo 1: Leitura e Status ---
    with st.status("🔍 Analisando documento...", expanded=True) as status:
        st.write("Extraindo texto do PDF...")
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        st.write("Configurando motor neural...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.5-flash") # Modelo de alta capacidade
        
        status.update(label="Documento pronto. Clique para gerar o relatório.", state="complete", expanded=False)

    # --- Passo 2: Botão de Ação ---
    if st.button("GERAR RELATÓRIO EXECUTIVO"):
        
        # Simulação de Carregamento
        progress_text = "Auditando Balanço..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text="Processando indicadores e riscos...")
        my_bar.empty()

        # --- Passo 3: Prompt de Elite ---
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
            
            # --- Passo 4: EXIBIÇÃO AVANÇADA DO RESULTADO ---
            st.markdown("---")
            st.subheader("✅ Resultado da Análise")
            
            # Tenta extrair a nota e o veredito para mostrar em CARDS de Destaque
            nota_match = re.search(r'\*\*NOTA \(0-10\):\*\* (\d+)', relatorio)
            rec_match = re.search(r'\*\*RECOMENDAÇÃO:\*\* (COMPRA|MANTER|VENDA)', relatorio)
            
            if nota_match and rec_match:
                nota = nota_match.group(1)
                recomendacao = rec_match.group(1)
                
                # Define cor para a Recomendação
                if recomendacao == "COMPRA": cor = "#28A745"; icone = "⬆️"
                elif recomendacao == "VENDA": cor = "#DC3545"; icone = "⬇️"
                else: cor = "#FFC107"; icone = "↔️"
                
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    st.markdown(f'<div class="css-card" style="border-left: 5px solid #004D99;">', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 14px; color: #6c757d; margin-bottom: 0px;">Nota do Analista</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 36px; font-weight: 700; color: #004D99; margin-top: 5px;">{nota}/10</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with c2:
                    st.markdown(f'<div class="css-card" style="border-left: 5px solid {cor};">', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 14px; color: #6c757d; margin-bottom: 0px;">Recomendação</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 36px; font-weight: 700; color: {cor}; margin-top: 5px;">{icone} {recomendacao}</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with c3:
                    st.markdown('<div class="css-card" style="border-left: 5px solid #6C757D;">', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 14px; color: #6c757d; margin-bottom: 0px;">Modelo de IA</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 36px; font-weight: 700; color: #6C757D; margin-top: 5px;">Gemini 2.5</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Exibe o resto do relatório dentro de um Card
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.markdown("## Relatório Detalhado")
            st.markdown(relatorio)
            st.markdown('</div>', unsafe_allow_html=True)

            st.warning("⚖️ Disclaimer: Análise gerada por IA. Não constitui recomendação de investimento.")

        except Exception as e:
            st.error(f"Erro na API: {e}")

elif uploaded_file and not api_key:
    st.error("⚠️ Chave de API não encontrada. Por favor, insira no menu lateral (Sidebar).")
