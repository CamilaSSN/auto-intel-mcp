import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (onde está sua chave)
load_dotenv()

class MCPEngine:
    def __init__(self):
        # Responsabilidade: Definir a Raiz do Projeto dinamicamente
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Caminhos Absolutos para os dados
        self.gold_path = os.path.join(self.base_dir, "data", "3_gold", "historico_precos.csv")
        self.media_marca_path = os.path.join(self.base_dir, "data", "3_gold", "media_marca.csv")
        
        # Carrega a chave de forma segura a partir da variável de ambiente
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            print(" AVISO: Variável GROQ_API_KEY não encontrada no arquivo .env")
            
        self.client = Groq(api_key=self.api_key)

    def run_full_pipeline(self):
        """Orquestrador: Executa as 3 etapas do pipeline (Bronze -> Silver -> Gold)"""
        print(f" MCP: Iniciando orquestração em {self.base_dir}")
        
        scripts = [
            os.path.join("ingestion", "scraper_zoom.py"),
            os.path.join("transformation", "silver.py"),
            os.path.join("transformation", "gold.py")
        ]
        
        for rel_path in scripts:
            script_full_path = os.path.join(self.base_dir, rel_path)
            resultado = os.system(f'python "{script_full_path}"')
            if resultado != 0:
                return f" Erro crítico no script: {rel_path}"
        
        return " Pipeline sincronizado e dados atualizados com sucesso!"

    def generate_llm_summary(self):
        """Gera um Resumo Executivo detalhado para a aba de Insight"""
        try:
            if not os.path.exists(self.gold_path):
                return " Base de dados vazia. Sincronize o pipeline primeiro."

            df = pd.read_csv(self.gold_path)
            media = df['preco'].mean()
            
            # Localiza os destaques reais do banco de dados
            carro_top = df[df['categoria'] == 'Carro'].sort_values('preco').iloc[0]
            moto_top = df[df['categoria'] == 'Moto'].sort_values('preco').iloc[0]

            prompt = f"""
            Escreva um Resumo Executivo detalhado e profissional (mínimo 4 parágrafos) sobre o mercado automotivo.
            
            DADOS REAIS PARA O TEXTO:
            - Preço médio geral do estoque: R$ {media:,.2f}
            - Destaque Carro (Mais Barato): {carro_top['produto']} custando R$ {carro_top['preco']:,.2f}
            - Destaque Moto (Mais Barata): {moto_top['produto']} custando R$ {moto_top['preco']:,.2f}
            
            REGRAS OBRIGATÓRIAS:
            1. NÃO use caracteres especiais como \\c, \\o, \\a. Escreva em PORTUGUÊS fluído e correto.
            2. Estruture em: Visão Geral, Análise de Carros, Análise de Motos e Sugestão de Investimento.
            3. Use um tom de consultoria sênior.
            """

            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.6
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"O MCP encontrou um erro no resumo: {str(e)}"

    def responder_pergunta_livre(self, pergunta):
        """Consultoria IA: Responde perguntas baseadas no contexto de Carros e Motos"""
        try:
            if not os.path.exists(self.gold_path):
                return " Por favor, sincronize os dados primeiro."

            df = pd.read_csv(self.gold_path)
            
            # Pega os 10 mais baratos de cada categoria para dar contexto à IA
            carros = df[df['categoria'] == 'Carro'].sort_values("preco").head(10)
            motos = df[df['categoria'] == 'Moto'].sort_values("preco").head(10)
            contexto_veiculos = pd.concat([carros, motos])[['produto', 'categoria', 'preco', 'km']].to_string()

            prompt = f"""
            Você é um consultor automotivo inteligente. Abaixo está uma amostra dos dados disponíveis:
            {contexto_veiculos}
            
            Pergunta do usuário: "{pergunta}"
            
            INSTRUÇÕES:
            - Se o usuário perguntar por carros, foque nos modelos da categoria 'Carro'.
            - Se perguntar por motos, foque na categoria 'Moto'.
            - Seja prestativo e cite valores reais da lista acima.
            """

            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f" Erro ao processar pergunta: {str(e)}"