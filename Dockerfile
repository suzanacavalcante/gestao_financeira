# 1. Imagem base
FROM python:3.11-slim

# 2. Impede que o Python gere arquivos .pyc e permite ver logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# 3. Define a pasta onde o código vai morar dentro do container
WORKDIR /app

# 4. Instala dependências do sistema necessárias para o Banco de Dados PostgreSQL
# O Rocky Linux é RHEL, mas dentro do container será utilizar o Debian (slim), pois é o padrão de mercado para imagens Python
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# 6. Instala as bibliotecas do projeto 
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copia todo o conteúdo do projeto 
COPY . .

# 8. Porta onde o app vai rodar
EXPOSE 8000