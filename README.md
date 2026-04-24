# Wired Data Pipeline

## Deskripsi
Pipeline data otomatis yang melakukan:
- Web scraping Wired.com (Selenium)
- Penyajian data via API (FastAPI)
- Orkestrasi pipeline (Airflow DAG)
- Penyimpanan ke PostgreSQL (Docker)
- Analisis data menggunakan SQL

## Arsitektur
Scraping → JSON → API → Airflow → PostgreSQL → SQL Query

## Tools
- Selenium
- FastAPI
- Airflow
- PostgreSQL (Docker)

## Cara Menjalankan

### 1. Scraping
python scraping/scrape.py

### 2. API
uvicorn api.main:app --reload

### 3. Docker (Airflow + Postgres)
docker-compose up

### 4. Airflow
http://localhost:8080  
(username: admin | password: admin)

## Query SQL
- Clean author
- Top 3 author
- Keyword search (AI, Climate, Security)