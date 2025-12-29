import torch
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd

MODEL_PATH = "/opt/airflow/models" # Docker içindeki yol

def run_inference():
    start_time = time.time()
    # 1. Modeli ve Tokenizer'ı Yükle
    # Not: Modelin hangi base modelden eğitildiyse (örn: 'distilbert-base-uncased') onu belirtmelisin
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, use_safetensors=True)

    # 2. Veritabanından tahmin bekleyen verileri çek
    hook = PostgresHook(postgres_conn_id='postgres_default')
    df = hook.get_pandas_df("SELECT review_id, review_detail FROM movie_reviews")

    if df.empty:
        print("Tahmin edilecek yeni veri yok.")
        return

    # 3. Tahmin Yap (Batch processing)
    inputs = tokenizer(df['review_detail'].tolist(), padding=True, truncation=True, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)

    # 4. Tahminleri Veritabanına Geri Yaz
    # (Bunun için tablona yeni bir sütun eklememiz gerekecek: model_prediction)
    for idx, row in df.iterrows():
        pred = int(predictions[idx])
        sql = "UPDATE movie_reviews SET model_prediction = %s WHERE review_id = %s"
        hook.run(sql, parameters=(pred, row['review_id']))

    print(f"{len(df)} adet yorum için tahminler kaydedildi.")
    end_time = time.time()
    latency = end_time - start_time
    print(f"İşlem {latency:.4f} saniye sürdü.")