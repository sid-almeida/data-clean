import streamlit as st
import pandas as pd
import os


# configurei o streamlit para abrir em wide mode
st.set_page_config(layout="wide")

with st.sidebar:
    st.image("Brainize Tech(1).png", width=250)
    st.write('---')
    choice = st.radio("**Navegação:**", ("Limpeza Automatizada", "Sobre"))
    st.success("Esta aplicação tem como objetivo executar a **limpeza automatizada de dados** para a geração de **certificados**.")
    st.write('---')

if choice == "Limpeza Automatizada":
    st.subheader("Limpeza Automatizada de Dados")
    st.write("Selecione o augorítmo para ser utilizado.")
    # criei um uploader para fazer upload do arquivo .csv
    uploaded_file = st.file_uploader("Escolha um arquivo .csv", type="csv")
    if uploaded_file is not None:
        # salvei o nome do arquivo em uma variável
        filename = uploaded_file.name
        # transformei o arquivo em um dataframe com separador de ponto e vírgula
        data = pd.read_csv(uploaded_file, sep=";", encoding="latin1")
        st.subheader("Dataframe")
        st.write(data)
        # escrevi o típo de dado de cada coluna
        st.write("Tipos de dados:")
        st.write(data.dtypes)
        # criei um multi select para selecionar as colunas que serão utilizadas
        colunas = st.multiselect("Selecione as colunas que serão utilizadas", data.columns)
        # criei um botão para executar a limpeza
        if st.button("Executar Limpeza"):
            # excluí as colunas que não foram selecionadas
            data = data[colunas]
            # excluí linhas vaizas
            data = data.dropna(how="all")
            # convertí todas as colunas para o tipo string
            data = data.astype(str)
            # removí os espaços em branco no início e no fim de cada string
            data = data.apply(lambda x: x.str.strip())
            # removí os espaços em branco duplicados
            data = data.apply(lambda x: x.str.replace("  ", " "))
            # caso no título da coluna tenha a palavra "NOME", todos os valores devem começar com letra maiúscula no início de cada palavra
            data = data.apply(lambda x: x.str.title() if "NOME" in x.name else x)
            # caso no título da coluna tenha a palavra "CPF" e o valor seja menor que 11 caracteres, preenchi com zeros à esquerda
            data = data.apply(lambda x: x.str.zfill(11) if "CPF" in x.name and len(x) < 14 else x)
            # caso no título da coluna tenha a palavra "CPF" e o valor seja maior que 11 caracteres, verificar se existem "." e "-" duplicados e remover os duplicados
            data = data.apply(lambda x: x.str.replace("..", ".") if "CPF" in x.name and len(x) > 14 else x)
            data = data.apply(lambda x: x.str.replace("--", "-") if "CPF" in x.name and len(x) > 14 else x)

            # Mostrando o resultado da limpeza
            st.subheader("Dataframe Limpo")
            st.write(data)
            st.success("Limpeza executada com sucesso!")
            # Criei um botão para fazer o download do arquivo .csv limpo com o nome do arquivo original + "limpo" deletando a coluna index
            if st.download_button("Download do Arquivo Limpo", data.to_csv(index=False), file_name=f"{filename}_limpo.csv", mime="text/csv"):
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
