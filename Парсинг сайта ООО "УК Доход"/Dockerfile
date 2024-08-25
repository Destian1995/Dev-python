FROM python:3.11-slim

RUN  apt-get update && \ 
     apt-get install -y --no-install-recommends \
     chromium-driver \
     wget \
     unzip \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY /parser/parser-script.py /app
WORKDIR /app

ENV PATH="/usr/lib/chromium:/usr/local/sbin:/usr/local/bin:/usr/sbin:.usr/bin:/sbin:/bin"

CMD ["python3", "/app/parser-script.py"]
