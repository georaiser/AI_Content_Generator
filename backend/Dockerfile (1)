FROM python:3.9-slim

WORKDIR /backend

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libxss1 \
    libgdk-pixbuf2.0-0 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html

# Set environment variable for Chromium and Chromedriver path
ENV PATH="/usr/lib/chromium/:${PATH}"

# Copiar el resto de los archivos
COPY . .

EXPOSE 8004

ENTRYPOINT ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8004"]

