# Usa uma imagem base Python leve e estável
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto (servidor e prompt)
# O .gitignore impede que o .env suba
COPY . .

# O Railway define esta variável, mas a colocamos para clareza.
ENV PORT 8080

# Comando para rodar a aplicação quando o container iniciar
# O Railway exige que ele ligue na porta 8080 ou na variável $PORT
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8080"]

