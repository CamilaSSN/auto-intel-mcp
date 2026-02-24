
🚗 AutoIntel: Dashboard Automotivo com Consultoria IA
O AutoIntel é uma plataforma inteligente desenvolvida em Streamlit que não apenas exibe dados, mas ajuda o usuário a interpretá-los. O objetivo principal é transformar informações brutas de preços de carros e motos em decisões inteligentes através de um Dashboard Interativo e um Agente de IA que gera resumos executivos e responde perguntas em tempo real.

🎯 O Objetivo do Projeto
Diferente de dashboards estáticos, o AutoIntel foi construído para:
Simplificar a Análise: Responder perguntas diretas sobre o mercado (Ex: "Qual o carro mais barato da base?").
Gerar Insights Automáticos: Produzir um resumo executivo profissional sem que o usuário precise analisar gráfico por gráfico.
Orquestrar Dados: Gerenciar todo o fluxo de dados (coleta, limpeza e análise) de forma automatizada através do motor MCP.

🏗️ Como o Projeto Funciona (Etapa por Etapa)
O sistema segue a arquitetura de medalhão para garantir que a informação chegue limpa e confiável à IA:

1. Coleta Inteligente (Camada Bronze)
O sistema simula a captura de dados (Scraping) do mercado de veículos, registrando modelo, categoria, preço e quilometragem.

2. Refino e Padronização (Camada Silver)
Nesta fase, os dados são "limpos". Removendo duplicatas e garantindo que apenas Carros e Motos sigam no pipeline, eliminando ruídos de outras categorias.

3. Inteligência de Negócio (Camada Gold)
Os dados são agregados por marca e média de preço. Aqui, o sistema prepara as tabelas que alimentam tanto os gráficos quanto o contexto da IA.

4. Consultoria e Resumo IA (MCP Engine + LLM)
Resumo Executivo: O sistema lê a base final e utiliza o modelo Llama 3.3 (via Groq) para escrever um parecer técnico sobre o momento do mercado.

Perguntas e Respostas: Uma interface de chat permite que o usuário faça perguntas simples e receba respostas baseadas nos dados reais do dashboard.

🚀 Funcionalidades Principais
📈 Dashboard Visual: Gráficos de barras, histogramas e dispersão (Preço vs KM) com visual moderno e fontes otimizadas para leitura.
💬 Chat Consultivo: Uma aba dedicada para perguntar à IA sobre oportunidades específicas na base de dados.
📑 Relatório Automático: Uma aba que gera instantaneamente um texto analítico longo e detalhado com recomendações de compra
🔄 Sincronização em um Clique: Botão na barra lateral que dispara todo o pipeline de dados e atualiza o dashboard.

💻 Tecnologias
Front-end: Streamlit (Python)
IA: Groq Cloud API (Llama 3.1 & 3.3)
Manipulação de Dados: Pandas
Gráficos: Plotly Express