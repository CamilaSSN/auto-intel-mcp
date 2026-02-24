import pandas as pd
import os

def run_silver():
    bronze_path = "data/1_bronze/produtos_bronze.csv"
    silver_path = "data/2_silver/produtos_silver.csv"
    os.makedirs("data/2_silver", exist_ok=True)

    if not os.path.exists(bronze_path): return

    df = pd.read_csv(bronze_path)
    
    # Extração da Marca (Primeira palavra do nome)
    df["marca"] = df["produto"].str.split().str[0]
    
    # Limpeza de duplicados
    df = df.drop_duplicates(subset=["produto", "preco", "km"])
    
    df.to_csv(silver_path, index=False)
    print("Silver finalizada com sucesso.")

if __name__ == "__main__":
    run_silver()