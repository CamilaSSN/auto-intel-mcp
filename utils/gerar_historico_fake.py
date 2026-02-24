import pandas as pd
import random
from datetime import datetime, timedelta

df = pd.read_csv("data/2_silver/produtos_silver.csv")

historico = []

for i in range(30):
    for _, row in df.iterrows():
        data = datetime.now() - timedelta(days=i*7)
        preco = row["preco"] * random.uniform(0.85, 1.15)
        historico.append([row["produto"], row["categoria"], row["produto"].split()[0], round(preco,2), data.strftime("%Y-%m-%d")])

hist = pd.DataFrame(historico, columns=["produto","categoria","marca","preco","data_coleta"])
hist.to_csv("data/3_gold/historico_precos.csv", index=False)

print("Histórico fake gerado")