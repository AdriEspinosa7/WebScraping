# Usa Python 3.11 slim como base
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalamos dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
        tesseract-ocr \
        poppler-utils \
        cron \
        unzip \
        chromium \
        chromium-driver \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Creamos un enlace “google-chrome” que apunte a Chromium,
#    de modo que ChromeDriver lo encuentre automáticamente.
RUN ln -s /usr/bin/chromium /usr/bin/google-chrome

# 3. Directorio de trabajo
WORKDIR /app

# 4. Copiamos todo el código al contenedor
COPY . .

# 5. Instalamos las dependencias Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 6. Programamos cron para ejecutar main.py cada día a las 20:00
RUN echo "0 20 * * * cd /app && /usr/local/bin/python main.py >> /app/log.txt 2>&1" > /etc/cron.d/bolsa-cron
RUN chmod 0644 /etc/cron.d/bolsa-cron && crontab /etc/cron.d/bolsa-cron

# 7. Por defecto arrancamos cron en primer plano
CMD ["cron", "-f"]