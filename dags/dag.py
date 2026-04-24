from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import psycopg2

# 1. FETCH
def fetch_data(ti):
    response = requests.get("http://host.docker.internal:8000/articles")
    data = response.json()["articles"]

    ti.xcom_push(key="raw_data", value=data)


# 2. TRANSFORM
def transform_data(ti):
    data = ti.xcom_pull(key="raw_data", task_ids="fetch_data")

    cleaned = []

    for article in data:
        author = article["author"].replace("By", "").strip()

        cleaned.append({
            "title": article["title"],
            "url": article["url"],
            "description": article["description"],
            "author": author,
            "scraped_at": article["scraped_at"],
            "source": article["source"]
        })

    ti.xcom_push(key="clean_data", value=cleaned)


# 3. LOAD
def load_to_postgres(ti):
    data = ti.xcom_pull(key="clean_data", task_ids="transform_data")

    conn = psycopg2.connect(
        host="postgres",
        database="wired_db",
        user="postgres",
        password="postgres"
    )

    cursor = conn.cursor()

    for article in data:
        cursor.execute("""
        INSERT INTO wired_articles (title, url, description, author, scraped_at, source)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            article["title"],
            article["url"],
            article["description"],
            article["author"],
            article["scraped_at"],
            article["source"]
        ))

    conn.commit()
    cursor.close()
    conn.close()


with DAG(
    dag_id="wired_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    fetch = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch_data
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )

    load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres
    )

    fetch >> transform >> load