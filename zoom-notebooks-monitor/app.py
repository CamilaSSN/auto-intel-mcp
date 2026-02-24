import streamlit as st
import pandas as pd
import plotly.express as px
import os
from mcp.mcp_engine import MCPEngine

if 'mcp' not in st.session_state:
    st.session_state.mcp = MCPEngine()

mcp = st.session_state.mcp
st.set_page_config(page_title="AutoIntel Pro", layout="wide")

# --- CSS PARA AUMENTAR AS LETRAS ---
st.markdown("""
    <style>
    html, body, [class*="st-"] {
        font-size: 1.2rem !important; /* Aumenta a fonte geral */
    }
    h1 { font-size: 3rem !important; }
    h2 { font-size: 2.2rem !important; }
    h3 { font-size: 1.8rem !important; }
    .stMarkdown p { font-size: 1.3rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 AutoIntel: Dashboard & Consultoria")

st.sidebar.header("⚙️ Controle")
if st.sidebar.button("🔄 Sincronizar Dados"):
    with st.spinner("Sincronizando..."):
        st.sidebar.success(mcp.run_full_pipeline())
        st.rerun()

tab_dash, tab_insight = st.tabs(["📊 Dashboard & Consultoria", "🤖 Insight Executivo"])

gold_path = mcp.gold_path
if not os.path.exists(gold_path):
    st.warning("⚠️ Sincronize os dados na barra lateral.")
else:
    df_completo = pd.read_csv(gold_path)
    df = df_completo[df_completo['categoria'].isin(['Carro', 'Moto'])].copy()

    with tab_dash:
        col_graf, col_chat = st.columns([0.6, 0.4])

        with col_graf:
            # --- NOMES DOS GRÁFICOS AJUSTADOS ---
            st.subheader("📌 Análise de Preços por Fabricante")
            df_marca = df.groupby("marca")["preco"].mean().reset_index().sort_values("preco")
            fig_marca = px.bar(df_marca, x="marca", y="preco", 
                               template="plotly_dark", color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_marca, use_container_width=True)

            st.subheader("📌 Distribuição de Ofertas por Categoria")
            fig_dist = px.histogram(df, x="preco", color="categoria", 
                                    nbins=20, barmode="group",
                                    template="plotly_dark",
                                    color_discrete_map={"Carro": "#EF553B", "Moto": "#00CC96"})
            st.plotly_chart(fig_dist, use_container_width=True)

            st.subheader("📌 Comparativo: Preço vs. Quilometragem")
            fig_scatter = px.scatter(df, x="km", y="preco", color="categoria", 
                                     hover_name="produto", template="plotly_dark",
                                     color_discrete_map={"Carro": "#EF553B", "Moto": "#00CC96"})
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_chat:
            st.subheader("💬 Consultoria Especializada IA")
            st.write("Tire suas dúvidas sobre carros e motos da base:")
            pergunta = st.text_input("Ex: Qual o carro mais barato e qual a km dele?")
            if st.button("Enviar Pergunta"):
                with st.spinner("Analisando base completa..."):
                    resposta = mcp.responder_pergunta_livre(pergunta)
                    st.info(resposta)

    with tab_insight:
        st.subheader("📑 Resumo Executivo Detalhado")
        st.markdown("---")
        # O resumo agora será maior e com escrita corrigida
        st.markdown(mcp.generate_llm_summary())