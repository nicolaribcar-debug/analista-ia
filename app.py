from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import io
import os
from PyPDF2 import PdfReader
import google.generativeai as genai
from pydantic import BaseModel

# Importa o cérebro do Analista
try:
    from analyst_prompt import gerar_prompt_final
except ImportError:
    # Se o arquivo não existir, usa uma string vazia (erro na produção)
    gerar_prompt_final = lambda x: f"Prompt Error: {x}" 

# --- CONFIGURAÇÃO INICIAL E SERVIDOR ---
app = FastAPI(title="Financial Analyst API", 
              description="Serviço de Análise Fundamentalista com Gemini 2.5", 
              version="1.0.0")

# --- LÓGICA DE SEGURANÇA E API KEY ---
try:
    API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = None # A chave deve ser configurada no servidor de deploy

# Modelo de resposta para garantir a estrutura (pydantic)
class AnaliseResponse(BaseModel):
    status: str
    message: str
    analise_texto: str
    empresa_chave: str

# --- ROTA PRINCIPAL DA ANÁLISE (O MOTOR) ---
@app.post("/api/v1/analisar-pdf/", response_model=AnaliseResponse)
async def analisar_pdf(
    file: UploadFile = File(..., description="Arquivo PDF do Release de Resultados"),
    empresa_id: str = "XP_TESTE" # Simula a chave de acesso B2B
):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Chave de API do Gemini não configurada no servidor.")

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Arquivo inválido. Por favor, envie um PDF.")

    # 1. Leitura do PDF
    try:
        conteudo = await file.read()
        reader = PdfReader(io.BytesIO(conteudo))
        text = "".join(page.extract_text() for page in reader.pages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na leitura do PDF: {e}")

    # 2. Configuração e Geração da IA
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        prompt_final = gerar_prompt_final(text)
        
        response = model.generate_content(prompt_final)
        
        # 3. Retorno Sucesso
        return AnaliseResponse(
            status="success",
            message=f"Análise concluída para Empresa ID: {empresa_id}",
            analise_texto=response.text,
            empresa_chave=empresa_id
        )

    except Exception as e:
        # Se falhar aqui, é provável que seja limite de uso ou chave inválida
        print(f"Erro na geração da IA: {e}")
        raise HTTPException(status_code=503, 
                            detail="Serviço de IA Indisponível (Limite de uso ou chave inválida)")

# Rota de Status Simples
@app.get("/")
def status_check():
    return {"status": "ok", "service": "Financial Analyst API v1"}
