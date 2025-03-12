# Usa uma imagem base do Python
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /api

# Copia os arquivos do projeto para o container
COPY . /api

# Instala as dependências da API
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000 (ou a que sua API usa)
EXPOSE 5000

# Comando para iniciar a API
CMD ["python", "api.py"]