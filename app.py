import streamlit as st

from utils.google import get_sheet_service, get_title, upload_drive
from utils.plot import format_plot_data, plot_data

USERS = {"admin": "web2023"}
CELLS = [
    "Grafico!P18:P66",
    "Grafico!Q18:P66",  # FASE MONTANTE
    "Grafico!T18:T66",
    "Grafico!U18:T66",  # NEUTRO MONTANTE
    "Grafico!X18:X66",
    "Grafico!Y18:X66",  # FASE JUSANTE
    "Grafico!AB18:AB66",
    "Grafico!AC18:AC66",  # NEUTRO JUSANTE
    "Grafico!B55:B56",
    "Grafico!C55:C56",  # I CARGA
    "Grafico!B60:B61",
    "Grafico!C60:C61",  # ANSI
    "Grafico!B65:B66",
    "Grafico!C65:C66",  # IMAG
    "Grafico!E55:E56",
    "Grafico!F55:F56",  # ICC3F
    "Grafico!E60:E61",
    "Grafico!F60:F61",  # ICC1F
    "Grafico!H55:H56",
    "Grafico!I55:I56",  # 51 GS MONTANTE
    "Grafico!H60:H61",
    "Grafico!I60:I61",  # 51 GS JUSANTE
    "Curvas_fusiveis!P59:P102",
    "Curvas_fusiveis!Q59:Q102",  # ELO
]

SPREADSHEET_ID = "1WnrHs_0bG33XNqnsYQIrMkNM3LK4-V6mVYP50CPehts"


def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "title" not in st.session_state:
        st.session_state["title"] = ""


def validate_login(username, password):
    return username in USERS and password == USERS[username]


def set_logged_in_state():
    st.session_state["logged_in"] = True


def set_title_in_state():
    sheet = get_sheet_service()
    title = get_title(sheet, SPREADSHEET_ID)
    st.session_state["title"] = title


def format_and_plot():
    sheet = get_sheet_service()
    data_values = format_plot_data(sheet, SPREADSHEET_ID, CELLS)
    fig = plot_data(data_values)

    return fig


def main():
    initialize_session_state()

    if not st.session_state["logged_in"]:
        st.title("Login | Coordenograma")

        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if validate_login(username, password):
                set_logged_in_state()
                set_title_in_state()
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")

    if st.session_state["logged_in"]:
        st.title("Dashboard | Coordenograma")
        st.write("Agora você pode gerar gráficos e fazer upload para o Google Drive.")

        if st.button("Gerar Gráfico"):
            with st.spinner("Gerando gráfico..."):
                img_buffer, fig = format_and_plot()
            st.pyplot(fig)
            st.success("Gráfico gerado com sucesso!")

        if st.button("Salvar no Google Drive"):
            with st.spinner("Salvando no Google Drive..."):
                img_buffer, _ = format_and_plot()
                file_name = f"{st.session_state['title']}_COORDENOGRAMA.jpeg"
                upload_drive(img_buffer, file_name)
            st.success(f"Arquivo {file_name} salvo com sucesso no Google Drive!")


if __name__ == "__main__":
    main()
