import streamlit as st
import pandas as pd
import os
import re

# configurei o streamlit para abrir em wide mode
st.set_page_config(layout="wide")

# funçao para formatar cpf
def format_cpf_column(data):
    # Remove dígitos especiais e espaços
    data["CPF_PARTICIPANTE"] = data["CPF_PARTICIPANTE"].str.replace(r'[.-]', '', regex=True)
    # Adiciona um "0" no início dos valores que não começam com "0"
    data["CPF_PARTICIPANTE"] = data["CPF_PARTICIPANTE"].apply(lambda x: '0' + x if not x.startswith('0') else x)
    # Formata os valores para o formato "000.000.000-00"
    data["CPF_PARTICIPANTE"] = data["CPF_PARTICIPANTE"].str.replace(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', regex=True)
    return data

# função linhas vazias
def remover_ultimas_linhas_vazias(df):
    linhas_vazias = df[df.isna().all(axis=1)].index
    df = df.drop(linhas_vazias)
    return df

with st.sidebar:
    st.image("Brainize Tech(1).png", width=250)
    st.write('---')
    choice = st.radio("**Navegação:**", ("Limpeza Automatizada", "Sobre"))
    st.success("Esta aplicação tem como objetivo executar a **limpeza automatizada de dados** para a geração de **certificados**.")
    st.write('---')

if choice == "Limpeza Automatizada":
    st.subheader("Limpeza Automatizada de Dados")
    # criei um uploader para fazer upload do arquivo .csv
    uploaded_file = st.file_uploader("Escolha um arquivo .csv", type="csv")
    if uploaded_file is not None:
        # criei selectboxes para selecionar o separador do arquivo .csv
        sep = st.radio("Selecione o separador do arquivo .csv", (",", ";","|"))
        # salvei o nome do arquivo em uma variável
        filename = uploaded_file.name
        # transformei o arquivo em um dataframe com separador de ponto e vírgula
        data = pd.read_csv(uploaded_file, sep=sep, encoding="latin1")
        # removi linhas vazias
        remover_ultimas_linhas_vazias(data)
        st.subheader("Dataframe")
        st.write(data)
        # converti todas as colunas para string
        data = data.astype(str)
        # escrevi o típo de dado de cada coluna
        st.write("Tipos de dados:")
        st.write(data.dtypes)
        # criei um multi select para selecionar as colunas que serão utilizadas
        colunas = st.multiselect("Selecione as colunas que serão utilizadas", data.columns)
        # criei um botão para executar a limpeza
        if st.button("Executar Limpeza"):
            # excluí as colunas que não foram selecionadas
            data = data[colunas].astype(str)
            # excluí linhas vaizas
            data = data.dropna(how="all")
            # removí linhas com valores None Nan ou Na
            data = data.dropna()
            # removí os espaços em branco no início e no fim de cada string
            data = data.apply(lambda x: x.str.strip())
            # removí os espaços em branco duplicados
            data = data.apply(lambda x: x.str.replace("  ", " "))
            # caso no título da coluna tenha a palavra "NOME", todos os valores devem começar com letra maiúscula no início de cada palavra
            data = data.apply(lambda x: x.str.title() if "NOME" in x.name else x)
            data = data.apply(lambda x: x.str.zfill(11) if "CPF" in x.name and len(x) < 14 else x)
            # caso o título da coluna tenha a palavra "EMAIL", todos os valores devem estar em letras minúsculas
            data = data.apply(lambda x: x.str.lower() if "EMAIL" in x.name else x)
            # Aplicando a função format_cpf_column
            data = format_cpf_column(data)
            # Mostrando o resultado da limpeza
            st.subheader("Dataframe Limpo")
            st.write(data)
            st.success("Limpeza executada com sucesso!")
            # Criei um botão para fazer o download do arquivo .csv limpo com o nome do arquivo original + "limpo" deletando a coluna index com todas as colunas convertidas para string
            if st.download_button("Download do Arquivo Limpo", data.to_csv(index=False, encoding="latin1"), file_name=filename.replace(".csv", "") + "_limpo.csv"):
                pass
    else:
        st.warning("Faça o upload de um arquivo .csv para executar a **limpeza**.")


if choice == "Sobre":
    st.subheader("Sobre o Projeto")
    st.write('---')
    st.write("**Sobre o App**:\nEste aplicativo é um Software criado com o objetivo de automatizar a limpeza de dados para a geração de certificados no **IFRS - Campus Caxias do Sul**.")
    st.write("**Tenologia**:\nEle utiliza **Python** em conjunto com a biblioteca **Pandas** para executar a limpeza dos dados de forma automática.")
    st.write("**Implementação**:\nA implementação foi feita em forma de **WebApp** na plataforma **Streamlit** para facilitar o acesso.")
    st.write('---')
st.write('Made with ❤️ by [Sidnei Almeida](https://www.linkedin.com/in/saaelmeida93/)')
