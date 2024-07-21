# Use a imagem base mais recente do Ubuntu
FROM python:3

WORKDIR /app

# Atualize o sistema e instale dependências necessárias
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get update && apt-get install -y \
    libcap2 \
    sqlite3 \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o container
COPY /server-client_v2/* /app/server-client_v2/
COPY start_system.sh /app/
COPY app.py /app/
COPY sca-start.py /app/
COPY /templates/* /app/templates/
COPY /static/ /app/static/
COPY /db_images/ /app/db_images/

# Exponha a porta em que a aplicação será executada
EXPOSE 5000
EXPOSE 5007/udp
EXPOSE 50051

# Comando para rodar a aplicação Flask
CMD ["./start_system.sh"]