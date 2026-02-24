import pandas as pd
from datetime import datetime
import os
import random

def run_scraper():
    bronze_path = "data/1_bronze/produtos_bronze.csv"
    
    # Remove dados antigos de eletrônicos se o arquivo existir
    if os.path.exists(bronze_path):
        os.remove(bronze_path)
        print(" Dados antigos removidos.")

    veiculos = []
    print(f" Iniciando coleta de Veículos...")
    
    modelos = [
        ("Toyota Corolla", "Carro"), ("Honda Civic", "Carro"), ("Fiat Uno", "Carro"),
        ("VW Gol", "Carro"), ("Chevrolet Onix", "Carro"), ("Hyundai HB20", "Carro"),
        ("Honda CG 160", "Moto"), ("Yamaha Fazer 250", "Moto"), ("BMW R1250 GS", "Moto"),
        ("Honda Biz", "Moto"), ("Kawasaki Ninja 400", "Moto"), ("Yamaha MT-03", "Moto")
    ]

    for modelo, tipo in modelos:
        for _ in range(random.randint(8, 12)):
            base_price = random.randint(35000, 150000) if tipo == "Carro" else random.randint(9000, 58000)
            preco = round(base_price * random.uniform(0.7, 1.3), 2)
            km = random.randint(0, 130000)
            data_coleta = datetime.now().strftime("%Y-%m-%d")
            veiculos.append([modelo, tipo, preco, km, data_coleta])

    df = pd.DataFrame(veiculos, columns=["produto", "categoria", "preco", "km", "data_coleta"])
    os.makedirs("data/1_bronze", exist_ok=True)
    df.to_csv(bronze_path, index=False)
    print(f" Sucesso! {len(df)} veículos registrados.")

if __name__ == "__main__":
    run_scraper()