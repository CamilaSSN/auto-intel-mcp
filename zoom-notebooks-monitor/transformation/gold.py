import pandas as pd
import os

def run_gold():
    # Detecta a pasta do projeto (sobe um nível a partir de /transformation)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    silver_path = os.path.join(base_dir, "data", "2_silver", "produtos_silver.csv")
    gold_dir = os.path.join(base_dir, "data", "3_gold")
    gold_path = os.path.join(gold_dir, "historico_precos.csv")
    media_marca_path = os.path.join(gold_dir, "media_marca.csv")

    if not os.path.exists(silver_path):
        print(f" Erro: Arquivo Silver não encontrado em {silver_path}")
        return

    os.makedirs(gold_dir, exist_ok=True)
    df = pd.read_csv(silver_path)

    # Agregações
    df.groupby("marca", as_index=False)["preco"].mean().round(2).to_csv(media_marca_path, index=False)
    
    # Salva o histórico (Gold)
    df.to_csv(gold_path, index=False)
    
    print(f"✅ Camada Gold (Veículos) atualizada em: {gold_path}")

if __name__ == "__main__":
    run_gold()