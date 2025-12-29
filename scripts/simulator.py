import json
import random
import uuid
from airflow.providers.postgres.hooks.postgres import PostgresHook

def simulate_new_reviews():
    # 1. Hammadde Deposunu (JSON) Oku
    json_path = "/opt/airflow/data/source/data.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    # JSON liste mi sözlük mü kontrolü
    reviews_pool = all_data if isinstance(all_data, list) else all_data.get('root', [])

    # 2. Havuzdan rastgele seçim yap
    num_to_sample = random.randint(3, 6) # Her seferinde 1-5 arası yorum
    new_samples = random.sample(reviews_pool, num_to_sample)

    # 3. Veritabanına "Yeni Veri" olarak bas
    hook = PostgresHook(postgres_conn_id='postgres_default')
    
    for item in new_samples:
        new_id = f"sim_{str(uuid.uuid4())[:6]}" # Simülasyon olduğu belli olsun
        sql = """
            INSERT INTO movie_reviews (review_id, movie, review_detail, spoiler_tag, model_prediction)
            VALUES (%s, %s, %s, %s, NULL)
            ON CONFLICT (review_id) DO NOTHING;
        """
        params = (new_id, item.get('movie'), item.get('review_detail'), item.get('spoiler_tag'))
        hook.run(sql, parameters=params)
    
    print(f"Sisteme {num_to_sample} adet yeni yorum 'canlı' olarak eklendi.")