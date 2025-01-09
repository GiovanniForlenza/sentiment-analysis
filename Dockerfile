FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt update && apt install -y build-essential
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U spacy

CMD ["bash"]