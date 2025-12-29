import json
import os
from airflow.providers.postgres.hooks.postgres import PostgresHook

def load_json_to_postgres():
    # 1. JSON dosyasını oku
    json_path = "/opt/airflow/data/source/data.json"
    
    if not os.path.exists(json_path):
        print(f"Hata: {json_path} bulunamadı!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Veri tipini kontrol et (Hatanın çözümü burada)
    if isinstance(data, list):
        # Eğer dosya doğrudan [{}, {}] şeklindeyse
        reviews = data
    elif isinstance(data, dict):
        # Eğer dosya {"root": [{}, {}]} şeklindeyse
        reviews = data.get('root', [])
    else:
        print("Bilinmeyen JSON formatı")
        return

    # 3. Postgres'e bağlan
    hook = PostgresHook(postgres_conn_id='postgres_default')
    
    # 4. Verileri ekle (Hız kazanmak için ilk 10 tanesini deneyelim)
    print(f"Toplam {len(reviews)} adet kayıt bulundu. İlk 10 tanesi işleniyor...")
    
    for r in reviews[:10]:
        sql = """
            INSERT INTO movie_reviews (review_id, movie, review_detail, spoiler_tag)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (review_id) DO NOTHING;
        """
        # JSON'daki anahtar isimlerinin tam eşleştiğinden emin olalım
        params = (
            r.get('review_id'), 
            r.get('movie'), 
            r.get('review_detail'), 
            r.get('spoiler_tag')
        )
        hook.run(sql, parameters=params)
    
    print("İşlem başarıyla tamamlandı!")