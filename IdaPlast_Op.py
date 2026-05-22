import streamlit as st 
import pandas as pd 
import plotly_express as px 
#import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

#color = st.color_picker("Pick A Color", "#00f900")
#st.write("The current color is", color)

df = pd.read_csv("IdaPlastEqRenata.csv", sep=",")


df=df.sort_values("Nome")

df["Colab"] = df["Nome"]
df["Compet"] = df["Competencia"]
df["Setor"] = df["Nível de Avaliação"]
df["Setorial"] = df["Nível de Avaliação"]
df["Comenta"] = df["Comentário"]
df["Avaliar"] = df["Avaliador"]


st.write("""
# Ida Plast - Análise de Competências (Operação)
""" )

st.sidebar.write("""
## Renata de Lima Rocha
""" )

aval = ["Autoavaliação","Gestor"]

Nome = st.sidebar.selectbox("Avaliados",df["Colab"].unique())

df_filtered = df[df["Colab"] == Nome]
#df_filtered

df_Média = df_filtered.groupby("Compet")[["Autoavaliação","Gestor",]].mean().round(decimals=1).reset_index()
#df_Média

aval = ["Autoavaliação","Gestor"]
#----------------------------------------------------------------------

#Avaliado = str(Nome)
st.write("""
## Competências
""" ), Nome

fig_comp = px.bar(df_Média, y=aval, x="Compet", barmode='group', color_discrete_map = {"Autoavaliação":"#94380A", "Gestor":"#EBD027"})
fig_comp.update_layout(xaxis_title="Competências", yaxis_title="Médias")

fig_comp

#df_filtered

#-------------------------------------------------------------------------------------------

st.write("""
## Análise das Perguntas
""" ), Nome

aval1 = ["Gestor", "Autoavaliação"]

#df["CompetUniqx"] = df_filtered["Competencia"]
#df["CompetUniqx"]
df_CompetUniq = df_filtered["Competencia"].dropna().reset_index(drop = True)

unica_Competencia = st.selectbox("Escolha a Competência",df_CompetUniq.unique(),index=1)

df_filtered2 = df_filtered[df["Compet"] == unica_Competencia]

#fig_Perg = px.bar(df_filtered2, y="Pergunta", x=aval1, orientation="h",height=300, barmode='group', color_discrete_map = {"Autoavaliação":"#094E86", "Gestor":"#EC6227"})
#fig_Perg.update_layout(xaxis_title="Médias", yaxis_title="Perguntas")
#fig_Perg.update_layout(xaxis_title="Médias", yaxis_title="Perguntas", height=500)
#fig_Perg
###

#df_filtered2 = df_filtered[df["Compet"] == unica_Competencia].copy()

df_filtered2["Pergunta"] = (df_filtered2["Pergunta"].str.replace(" - ", "<br>") .str.replace(" / ", "<br>"))

fig_Perg = px.bar(df_filtered2, y="Pergunta", x=aval1, orientation="h", height=500, barmode="group",color_discrete_map={"Autoavaliação":"#94380A", "Gestor":"#EBD027"})

fig_Perg.update_layout(xaxis_title="Médias", yaxis_title="Perguntas")

fig_Perg

#-------------------------------------------------------------------------------------------
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
        yaxis=dict(range=[0, 105]),
        showlegend=False
    )
    
    fig_trend
else:
    st.info("Histórico de evolução mensal não disponível para este colaborador.")

#coment = st.checkbox("Comentários")
#df_filteredy = df[df["Comenta"] == "Sim"]
##df_filteredy
#
#if coment:
#
#    col1, col2 = st.columns([1, 3])
#
#    with col1:
#        df_filtered3 = df_filteredy[df["Nome"] == Nome]
#       # df_filtered3
#        Coment = st.selectbox("Comentário de :",df_filtered3["Avaliador"].unique())
#    
#    with col2:
#        df_filteredz = df_filtered3[df["Avaliador"] == Coment]
#        texto = df_filteredz.iloc[0, 7]
#
#        st.text_area(
#            "Comentário",
#            texto,
#            height=150
#        )
#    with col2:
#        df_filteredz = df_filtered3[df["Avaliador"] == Coment]
#        df_coment = df_filteredz.iloc[:,7]
#        df_coment
        

#-----------------------------------------------------------------------------------------
#st.write("""
### Desempenho Geral por Competência
#""" )
#
#Compet_Desemp = st.selectbox("Defina a Competência",df["Compet"].dropna().unique(),index=1)
#
#aval1 = ["Autoavaliação","Gestor"]
#
#df_filtered5 = df[df["Compet"] == Compet_Desemp]
#
#df_MédiaGeral = df_filtered5.groupby("Nome")[["Autoavaliação","Gestor"]].mean().round(decimals=1).reset_index()
##df_MédiaGeral
#
#fig_DesenvGeral = px.bar(df_MédiaGeral, y=aval1, x="Nome", barmode='group',color_discrete_map = {"Autoavaliação":"#94380A", "Gestor":"#EBD027"})
#fig_DesenvGeral.update_layout(xaxis_title="Colaboradores do Setor", yaxis_title="Médias")
#fig_DesenvGeral
#
#---------------------------------------------------------------------------------

st.write("""
## Desempenho Geral dos Avaliados
""" )

AvalEquipe = st.checkbox("Exibir avaliação da Equipe")

if AvalEquipe:
   

    #df_filtered3 = df[df["Competencia"] == Compet_Desemp]
    #df_filtered3

    #df_MédiaSetor = df_filtered5.groupby("Setor")[["Auto Avaliação","Avaliador"]].mean().reset_index()
    #df_MédiaSetor

    #fig_Setor = px.bar(df_MédiaSetor, y=aval, x="Setor", barmode='group', color_discrete_map = {"Auto Avaliação":"Brown", "Avaliador":"Yellow"})
    #fig_Setor.update_layout(xaxis_title="Setores", yaxis_title="Médias")
    #fig_Setor



    df_filtered7 = df
    #df_filtered3

    #df_MédiaSetor = df_filtered7.groupby("Nome")[["Autoavaliação","Gestor","Pares","Liderados"]].mean().round(decimals=1).reset_index()
    df_MédiaSetor = df_filtered7.groupby("Nome")[["Gestor","Autoavaliação"]].mean().round(decimals=1).reset_index()
    #df_MédiaSetor

    #fig_Setor = px.bar(df_MédiaSetor, x=aval, y="Nome", orientation="h", barmode='group', color_discrete_map = {"Autoavaliação":"Blue", "Gestor":"#00F900","Pares":"#F9AF00", "Liderados":"#F900D2"})
    
    fig_Setor = px.bar(df_MédiaSetor, x=aval, y="Nome", orientation="h", height=500,barmode='group', color_discrete_map = {"Autoavaliação":"#94380A", "Gestor":"#EBD027"})
    fig_Setor.update_layout(xaxis_title="Média", yaxis_title="Colaborador")
    fig_Setor

    #---------------------------------------------
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
        yaxis=dict(range=[0, 105]),
        legend_title="Colaborador"
    )
    
    fig_team_trend
#---------------------------------------------
    