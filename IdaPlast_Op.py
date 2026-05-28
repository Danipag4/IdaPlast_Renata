import streamlit as st 
import pandas as pd 
try:
    import plotly.express as px
except ImportError:
    import plotly_express as px
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Ida Plast - Análise de Competências")

# 1. CSS Global de Impressão (aplicado apenas ao imprimir)
st.markdown("""
<style>
@media print {
    /* Ocultar barra lateral inteira */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Ocultar cabeçalho, rodapé e barra de ferramentas nativos do Streamlit */
    header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Ocultar botões, menus interativos (Selectbox) e caixas de seleção (Checkbox) do Streamlit */
    .stSelectbox, .stCheckbox, .stButton, .stDownloadButton, [data-testid="stForm"] {
        display: none !important;
    }
    
    /* Ocultar componentes de script do botão de impressão e iframes de terceiros */
    iframe, div[data-testid="stHtml"] {
        display: none !important;
    }
    
    /* Expandir o conteúdo principal para ocupar a largura máxima do papel */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("IdaPlastEqRenata.csv", sep=",")

df=df.sort_values("Nome")

df["Colab"] = df["Nome"]
df["Compet"] = df["Competencia"]
df["Setor"] = df["Nível de Avaliação"]
df["Setorial"] = df["Nível de Avaliação"]
df["Comenta"] = df["Comentário"]
df["Avaliar"] = df["Avaliador"]

# Inicializar estado de impressão se não existir
if "printing" not in st.session_state:
    st.session_state.printing = False

# Sidebar sempre é renderizada para manter o seletor do colaborador
# (Mas o CSS oculta ela na impressão física ou no PDF)
st.sidebar.write("""
## Renata de Lima Rocha
""" )

Nome = st.sidebar.selectbox("Avaliados",df["Colab"].unique())

# Filtros e dados comuns
df_filtered = df[df["Colab"] == Nome]
df_Média = df_filtered.groupby("Compet")[["Autoavaliação","Gestor",]].mean().round(decimals=1).reset_index()
aval = ["Autoavaliação","Gestor"]


# -------------------------------------------------------------
# CASO 1: MODO DE IMPRESSÃO (Layout limpo apenas com o solicitado)
# -------------------------------------------------------------
if st.session_state.printing:
    
    if st.button("⬅️ Voltar ao Painel", key="back_to_dashboard", type="secondary"):
        st.session_state.printing = False
        st.rerun()
            
    # Título do Relatório com Nome do Avaliado
    st.write(f"# Relatório de Avaliação - Ida Plast")
    st.write(f"### Colaborador Avaliado: **{Nome}**")
    st.markdown("---")
    
    # 1. Gráfico: Competências
    st.write("## Competências")
    fig_comp = px.bar(df_Média, y=aval, x="Compet", barmode='group', color_discrete_map = {"Autoavaliação":"#62492E", "Gestor":"#E2DF82"})
    fig_comp.update_layout(xaxis_title="Competências", yaxis_title="Médias")
    
    plotly_config_comp = {
        'displaylogo': False,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'competencias_{Nome.replace(" ", "_")}',
            'height': 600,
            'width': 1000,
            'scale': 2
        }
    }
    st.plotly_chart(fig_comp, use_container_width=True, config=plotly_config_comp)
    
    st.markdown("---")
    
    # 3. Gráfico: Evolução Mensal do Avaliado (É o terceiro gráfico do dashboard)
    st.write("## Evolução Mensal do Avaliado")
    df_trend_row = df[df["Unnamed: 12"] == Nome]
    
    if not df_trend_row.empty:
        months = ["janeiro 2026", "fevereiro 2026", "março 2026", "abril 2026"]
        values = df_trend_row[months].values[0]
        
        df_individual_trend = pd.DataFrame({
            "Mês": ["Janeiro", "Fevereiro", "Março", "Abril"],
            "Pontuação": values
        })
        
        df_individual_trend["Label"] = df_individual_trend["Pontuação"].apply(
            lambda v: f"{int(v)}" if pd.notna(v) else ""
        )
        
        fig_trend = px.line(
            df_individual_trend, 
            x="Mês", 
            y="Pontuação", 
            markers=True,
            text="Label",
            height=400
        )
        
        fig_trend.update_traces(
            line=dict(color="#94380A", width=3),
            marker=dict(size=10, color="#EBD027", line=dict(color="#94380A", width=2)),
            textposition="top center"
        )
        
        fig_trend.update_layout(
            xaxis_title="Mês",
            yaxis_title="Pontuação",
            yaxis=dict(range=[0, 300]),
            showlegend=False
        )
        
        plotly_config_trend = {
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'evolucao_{Nome.replace(" ", "_")}',
                'height': 600,
                'width': 1000,
                'scale': 2
            }
        }
        st.plotly_chart(fig_trend, use_container_width=True, config=plotly_config_trend)
    else:
        st.info("Histórico de evolução mensal não disponível para este colaborador.")
        
    st.markdown("---")
    
    # 4. Sequência de 10 Linhas em Branco (linhas de escrita pontilhadas)
    st.write("### Anotações / Plano de Ação")
    for i in range(6):
        st.markdown('<div style="border-bottom: 1px dotted #888; height: 32px; margin-bottom: 2px; width: 100%;"></div>', unsafe_allow_html=True)
        
    # Acionar diálogo de impressão após 1 segundo (tempo dos gráficos renderizarem)
    components.html(
        """
        <script>
            setTimeout(function() {
                window.parent.print();
            }, 1000);
        </script>
        """,
        height=0
    )

# -------------------------------------------------------------
# CASO 2: MODO PAINEL NORMAL (Todos os elementos interativos)
# -------------------------------------------------------------
else:
    st.write("""
    # Ida Plast - Análise de Competências (Liderança)
    """ )
    
    if st.button("🖨️ IMPRIMIR", key="btn_imprimir_top", type="primary"):
        st.session_state.printing = True
        st.rerun()

    # 1. Primeiro Gráfico: Competências
    st.write("""
    ## Competências
    """ ), Nome

    fig_comp = px.bar(df_Média, y=aval, x="Compet", barmode='group', color_discrete_map = {"Autoavaliação":"#62492E", "Gestor":"#E2DF82"})
    fig_comp.update_layout(xaxis_title="Competências", yaxis_title="Médias")

    plotly_config_comp = {
        'displaylogo': False,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'competencias_{Nome.replace(" ", "_")}',
            'height': 600,
            'width': 1000,
            'scale': 2
        }
    }
    st.plotly_chart(fig_comp, use_container_width=True, config=plotly_config_comp)

    # -------------------------------------------------------------------------------------------
    # 2. Segundo Gráfico: Análise das Perguntas
    st.write("""
    ## Análise das Perguntas
    """ ), Nome

    aval1 = ["Gestor", "Autoavaliação"]

    df_CompetUniq = df_filtered["Competencia"].dropna().reset_index(drop = True)
    
    competencias_lista = df_CompetUniq.unique()
    default_index = 1 if len(competencias_lista) > 1 else 0
    unica_Competencia = st.selectbox("Escolha a Competência", competencias_lista, index=default_index)

    df_filtered2 = df_filtered[df["Compet"] == unica_Competencia].copy()
    df_filtered2["Pergunta"] = (df_filtered2["Pergunta"].str.replace(" - ", "<br>") .str.replace(" / ", "<br>"))

    fig_Perg = px.bar(df_filtered2, y="Pergunta", x=aval1, orientation="h", height=500, barmode="group",color_discrete_map={"Autoavaliação":"#62492E", "Gestor":"#E2DF82"})
    fig_Perg.update_layout(xaxis_title="Médias", yaxis_title="Perguntas")

    plotly_config_perg = {
        'displaylogo': False,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'perguntas_{Nome.replace(" ", "_")}_{unica_Competencia.replace(" ", "_")}',
            'height': 600,
            'width': 1000,
            'scale': 2
        }
    }
    st.plotly_chart(fig_Perg, use_container_width=True, config=plotly_config_perg)

    # Seção de Comentários
    coment = st.checkbox("Comentários")
    df_filteredy = df[df["Comenta"] == "Sim"]

    if coment:
        col1, col2 = st.columns([1, 3])

        with col1:
            df_filtered3 = df_filteredy[df["Nome"] == Nome]
            Coment = st.selectbox("Comentário de :",df_filtered3["Avaliador"].unique())
        
        with col2:
            df_filteredz = df_filtered3[df["Avaliador"] == Coment]
            texto = df_filteredz.iloc[0, 7]

            st.text_area(
                "Comentário",
                texto,
                height=150
            )

    # -------------------------------------------
    # 3. Terceiro Gráfico: Evolução Mensal do Avaliado
    st.write("""
    ## Evolução Mensal do Avaliado
    """ )

    df_trend_row = df[df["Unnamed: 12"] == Nome]

    if not df_trend_row.empty:
        months = ["janeiro 2026", "fevereiro 2026", "março 2026", "abril 2026"]
        values = df_trend_row[months].values[0]
        
        df_individual_trend = pd.DataFrame({
            "Mês": ["Janeiro", "Fevereiro", "Março", "Abril"],
            "Pontuação": values
        })
        
        df_individual_trend["Label"] = df_individual_trend["Pontuação"].apply(
            lambda v: f"{int(v)}" if pd.notna(v) else ""
        )
        
        fig_trend = px.line(
            df_individual_trend, 
            x="Mês", 
            y="Pontuação", 
            markers=True,
            text="Label",
            height=400
        )
        
        fig_trend.update_traces(
            line=dict(color="#94380A", width=3),
            marker=dict(size=10, color="#EBD027", line=dict(color="#94380A", width=2)),
            textposition="top center"
        )
        
        fig_trend.update_layout(
            xaxis_title="Mês",
            yaxis_title="Pontuação",
            yaxis=dict(range=[0, 300]),
            showlegend=False
        )
        
        plotly_config_trend = {
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'evolucao_{Nome.replace(" ", "_")}',
                'height': 600,
                'width': 1000,
                'scale': 2
            }
        }
        st.plotly_chart(fig_trend, use_container_width=True, config=plotly_config_trend)
    else:
        st.info("Histórico de evolução mensal não disponível para este colaborador.")

    # ---------------------------------------------------------------------------------
    # Seção da Equipe (Se selecionada)
    st.write("""
    ## Desempenho Geral dos Avaliados
    """ )

    AvalEquipe = st.checkbox("Exibir avaliação da Equipe")

    if AvalEquipe:
        df_filtered7 = df
        df_MédiaSetor = df_filtered7.groupby("Nome")[["Gestor","Autoavaliação"]].mean().round(decimals=1).reset_index()
        
        fig_Setor = px.bar(df_MédiaSetor, x=aval, y="Nome", orientation="h", height=500,barmode='group', color_discrete_map = {"Autoavaliação":"#62492E", "Gestor":"#E2DF82"})
        fig_Setor.update_layout(xaxis_title="Média", yaxis_title="Colaborador")
        
        plotly_config_setor = {
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'desempenho_geral_equipe',
                'height': 600,
                'width': 1000,
                'scale': 2
            }
        }
        st.plotly_chart(fig_Setor, use_container_width=True, config=plotly_config_setor)

        # ---------------------------------------------
        st.write("""
        ### Evolução Mensal da Equipe
        """)
        
        df_team_trend = df[['Unnamed: 12', 'janeiro 2026', 'fevereiro 2026', 'março 2026', 'abril 2026']].dropna(subset=['Unnamed: 12']).copy()
        df_team_trend = df_team_trend.rename(columns={
            'Unnamed: 12': 'Colaborador',
            'janeiro 2026': 'Janeiro',
            'fevereiro 2026': 'Fevereiro',
            'março 2026': 'Março',
            'abril 2026': 'Abril'
        })
        
        df_team_melted = df_team_trend.melt(
            id_vars=['Colaborador'],
            var_name='Mês',
            value_name='Pontuação'
        )
        
        df_team_melted['Label'] = df_team_melted['Pontuação'].apply(
            lambda v: f"{int(v)}" if pd.notna(v) else ""
        )
        
        fig_team_trend = px.line(
            df_team_melted,
            x='Mês',
            y='Pontuação',
            color='Colaborador',
            markers=True,
            text='Label',
            height=500
        )
        
        fig_team_trend.update_traces(
            line=dict(width=3),
            marker=dict(size=8),
            textposition="top center"
        )
        
        fig_team_trend.update_layout(
            xaxis_title="Mês",
            yaxis_title="Pontuação",
            yaxis=dict(range=[0, 300]),
            legend_title="Colaborador"
        )
        
        plotly_config_team_trend = {
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'evolucao_mensal_equipe',
                'height': 600,
                'width': 1000,
                'scale': 2
            }
        }
        st.plotly_chart(fig_team_trend, use_container_width=True, config=plotly_config_team_trend)