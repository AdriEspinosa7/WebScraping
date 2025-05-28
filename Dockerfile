FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalación de dependencias
RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils cron unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia todos los archivos al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements_check.py || true
RUN python requirements_check.py

# Crea una tarea cron para ejecutar main.py todos los días a las 20:00
RUN echo "0 20 * * * cd /app && /usr/local/bin/python main.py >> /app/log.txt 2>&1" > /etc/cron.d/bolsa-cron

# Da permisos correctos
RUN chmod 0644 /etc/cron.d/bolsa-cron && crontab /etc/cron.d/bolsa-cron

# Comando por defecto: lanza cron en primer plano
CMD ["cron", "-f"]