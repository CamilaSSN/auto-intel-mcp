import os
import pandas as pd
from datetime import datetime

def run_ingestion():
    os.system("python ingestion/scraper_zoom.py")

def run_silver():
    os.system("python transformation/silver.py")

def run_gold():
    os.system("python transformation/gold.py")

BRONZE_PATH = "data/1_bronze/produtos_bronze.csv"

def validate_data():
    df = pd.read_csv(BRONZE_PATH)

    if df.empty:
        raise ValueError("❌ Dataset vazio")

    if df["preco"].isnull().sum() > 0:
        raise ValueError("❌ Existem preços nulos")

    if (df["preco"] <= 0).sum() > 0:
        raise ValueError("❌ Existem preços inválidos")

    print("✅ Validação de dados OK")

def run_pipeline():
    print("🔄 Rodando ingestion...")
    run_ingestion()

    print("🔍 Validando dados...")
    validate_data()

    print("🧹 Rodando silver...")
    run_silver()

    print("📊 Rodando gold...")
    run_gold()

    print(f"✅ Pipeline finalizado em {datetime.now()}")

if __name__ == "__main__":
    run_pipeline()