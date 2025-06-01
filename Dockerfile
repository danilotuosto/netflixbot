# Usa una base Python ufficiale
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl unzip xvfb \
    libxi6 libgconf-2-4 libnss3 libasound2 libx11-xcb1 gpg supervisor \
    && rm -rf /var/lib/apt/lists/*

# Aggiunge la chiave di Google e il repository di Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*
# Crea la directory dell'app
WORKDIR /app

# Copia i file necessari
COPY . /app

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando di default
CMD ["python", "netflixbot.py"]
