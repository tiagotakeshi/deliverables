import pandas as pd
import streamlit as st
import pickle

st.set_page_config(layout='wide')


@st.cache(allow_output_mutation=True)


def get_pickle(name):
    result = pickle.load(open(name, 'rb'))

    return result


def zone(zona):
    n = s = se = e = o = c = 0
    if zona == "Norte":
        n = 1
    elif zona == "Sul":
        s = 1
    elif zona == "Sudeste":
        se = 1
    elif zona == "Leste":
        e = 1
    elif zona == "Oeste":
        o = 1
    else:
        c = 1

    return n, s, se, e, o, c


def calculate(reg, a, be, ba, g, cond, c, e, n, o, se, s):
    value = reg.predict([[a, be, ba, g, cond, c, e, n, o, se, s]])

    return value


if __name__ == '__main__':
    # Extraction
    reg_name = 'regressor.pkl'
    reg = get_pickle(reg_name)
    st.title("Rental Calculator")
    st.subheader("We help you calculating the recommended rental value for you!")
    st.subheader("Fill the information about the building and click oin the button 'Calculate'.")
    area = float(st.text_input("Área do imóvel (m²): ", 75))
    quarto = int(st.selectbox("Número de Quartos: ", (range(11))))
    banheiro = int(st.selectbox("Número de Banheiros: ", (range(7))))
    garagem = int(st.selectbox("Quantidade de vagas de Garagens: ",(range(11))))
    condo = float(st.text_input("Valor de condomínio (R$): ", 500))
    zona = st.selectbox("Região: ",("Norte","Sul","Sudeste","Leste","Oeste","Centro"))
    norte, sul, sudeste, leste, oeste, centro = zone(zona)
    find = st.button("Calculate")
    if find:
        valor = calculate(reg, area, quarto, banheiro, garagem, condo, centro, leste, norte, oeste, sudeste, sul)
        st.success("O valor recomendado é de: R${0} ".format(round(float(valor),2)))

