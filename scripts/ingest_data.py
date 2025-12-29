import pandas as pd
import json
import os
from datetime import datetime

SOURCE_JSON = "/opt/airflow/data/source/data.json"
INGEST_PATH = "/opt/airflow/data/ingested"

def simulate_ingestion():
    if not os.path.exists(SOURCE_JSON):
        print("Hata: Kaynak JSON dosyası bulunamadı!")
        return

    with open(SOURCE_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Senin yapına göre 'root' anahtarındaki listeyi alıyoruz
        reviews = data.get('root', [])

    if not reviews:
        print("Hata: JSON içeriği boş!")
        return

    # DataFrame'e çevir ve rastgele 5 örnek seç
    df = pd.DataFrame(reviews)
    sample = df.sample(min(len(df), 5))
    
    # Timestamp ile kaydet
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"batch_{timestamp}.parquet"
    
    os.makedirs(INGEST_PATH, exist_ok=True)
    output_path = os.path.join(INGEST_PATH, filename)
    
    # Veriyi kaydet
    sample.to_parquet(output_path, index=False)
    print(f"Başarıyla işlendi: {filename}")

if __name__ == "__main__":
    simulate_ingestion()