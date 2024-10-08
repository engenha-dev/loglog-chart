import streamlit as st

from utils.google import get_sheet_service, get_title, upload_drive
from utils.plot import format_plot_data, plot_data

users = {"admin": "web2023"}

phase_cells = [
    "Dados_Gráficos!C9:C58",
    "Dados_Gráficos!D9:D58",  # 51/50 - Concessionária
    "Dados_Gráficos!K9:K58",
    "Dados_Gráficos!L9:L58",  # 51/50 - Cabine Cliente
    "Dados_Gráficos!R9:R10",
    "Dados_Gráficos!S9:S10",  # Corrente de Curto Icc3F - Concessionária
    "Dados_Gráficos!U9:U10",
    "Dados_Gráficos!V9:V10",  # Corrente de Curto Icc2F - Concessionária
    "Dados_Gráficos!AG9:AG10",
    "Dados_Gráficos!AH9:AH10",  # Corrente de Carga - Cabine Cliente
    "Dados_Gráficos!AJ9:AJ10",
    "Dados_Gráficos!AK9:AK10",  # Corrente de Partida Fase - Cabine Cliente
    "Dados_Gráficos!AP9:AP10",
    "Dados_Gráficos!AQ9:AQ10",  # Corrente de Magnetização - Cabine Cliente
    "Dados_Gráficos!AY9:AY10",
    "Dados_Gráficos!AZ9:AZ10",  # Corrente de Magnetização do  Menor Trafo - Cliente
    "Dados_Gráficos!BE9:BE10",
    "Dados_Gráficos!BF9:BF10",  # ANSI Trafo 1 - Cliente
    "Dados_Gráficos!BH9:BH10",
    "Dados_Gráficos!BI9:BI10",  # ANSI Trafo 2 - Cliente
    "Dados_Gráficos!BK9:BK10",
    "Dados_Gráficos!BL9:BL10",  # ANSI Trafo 3 - Cliente
    "Dados_Gráficos!BN9:BN10",
    "Dados_Gráficos!BO9:BO10",  # ANSI Trafo 4 - Cliente
    "Dados_Gráficos!BQ9:BQ10",
    "Dados_Gráficos!BR9:BR10",  # ANSI Trafo 5 - Cliente
    "Dados_Gráficos!BT9:BT10",
    "Dados_Gráficos!BU9:BU10",  # ANSI Trafo 6 - Cliente
    "Dados_Gráficos!BW9:BW10",
    "Dados_Gráficos!BX9:BX10",  # ANSI Trafo 7 - Cliente
    "Dados_Gráficos!BZ9:BZ15",
    "Dados_Gráficos!CA9:CA15",  # Curva de Dado Trafo 1 - Cliente
    "Dados_Gráficos!CC9:CC15",
    "Dados_Gráficos!CD9:CD15",  # Curva de Dado Trafo 2 - Cliente
    "Dados_Gráficos!CF9:CF15",
    "Dados_Gráficos!CG9:CG15",  # Curva de Dado Trafo 3 - Cliente
    "Dados_Gráficos!CI9:CI15",
    "Dados_Gráficos!CJ9:CJ15",  # Curva de Dado Trafo 4 - Cliente
    "Dados_Gráficos!CL9:CL15",
    "Dados_Gráficos!CM9:CM15",  # Curva de Dado Trafo 5 - Cliente
    "Dados_Gráficos!CO9:CO15",
    "Dados_Gráficos!CP9:CP15",  # Curva de Dado Trafo 6 - Cliente
    "Dados_Gráficos!CR9:CR15",
    "Dados_Gráficos!CS9:CS15",  # Curva de Dado Trafo 7 - Cliente
    "Dados_Gráficos!DP9:DP52",
    "Dados_Gráficos!DQ9:DQ52",  # ELO FUSÍVEL - Cliente
]

neutral_cells = [
    "Dados_Gráficos!G9:G58",
    "Dados_Gráficos!H9:H58",  # 51N/50N - Concessionária
    "Dados_Gráficos!O9:O58",
    "Dados_Gráficos!P9:P58",  # 51N/50N - Cabine Cliente
    "Dados_Gráficos!X9:X10",
    "Dados_Gráficos!Y9:Y10",  # Corrente de Curto IccFT Máx - Concessionária
    "Dados_Gráficos!AA9:AA10",
    "Dados_Gráficos!AB9:AB10",  # Corrente de Curto IccFT Mín. - Concessionária
    "Dados_Gráficos!AD9:AD10",
    "Dados_Gráficos!AE9:AE10",  # Sobrecorrente Temporizada Sensível a Terra - Concessionária
    "Dados_Gráficos!AG9:AG10",
    "Dados_Gráficos!AH9:AH10",  # Corrente de Carga - Cabine Cliente
    "Dados_Gráficos!AM9:AM10",
    "Dados_Gráficos!AN9:AN10",  # Corrente de Partida Neutro - Cabine Cliente
    "Dados_Gráficos!AS9:AS10",
    "Dados_Gráficos!AT9:AT10",  # Corrente de Magnetização Residual - Cabine Cliente
    "Dados_Gráficos!AV9:AV10",
    "Dados_Gráficos!AW9:AW10",  # Sobrecorrente Temporizada Sensível a Terra - Cliente
    "Dados_Gráficos!CU9:CU10",
    "Dados_Gráficos!CV9:CV10",  # NANSI Trafo 1 - Cliente
    "Dados_Gráficos!CX9:CX10",
    "Dados_Gráficos!CY9:CY10",  # NANSI Trafo 2 - Cliente
    "Dados_Gráficos!DA9:DA10",
    "Dados_Gráficos!DB9:DB10",  # NANSI Trafo 3 - Cliente
    "Dados_Gráficos!DD9:DD10",
    "Dados_Gráficos!DE9:DE10",  # NANSI Trafo 4 - Cliente
    "Dados_Gráficos!DG9:DG10",
    "Dados_Gráficos!DH9:DH10",  # NANSI Trafo 5 - Cliente
    "Dados_Gráficos!DJ9:DJ10",
    "Dados_Gráficos!DK9:DK10",  # NANSI Trafo 6 - Cliente
    "Dados_Gráficos!DM9:DM10",
    "Dados_Gráficos!DN9:DN10",  # NANSI Trafo 7 - Cliente
]

SPREADSHEET_ID = "1996UCu8Zrlz6EKvT9lYdCSV37A1BsQ3jfF9YZgtNt4M"


def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "title" not in st.session_state:
        st.session_state["title"] = ""


def validate_login(username, password):
    return username in users and password == users[username]


def set_logged_in_state():
    st.session_state["logged_in"] = True


def set_title_in_state():
    sheet = get_sheet_service()
    title = get_title(sheet, SPREADSHEET_ID)
    st.session_state["title"] = title


def format_and_plot(cell_range, choice):
    sheet = get_sheet_service()
    data_values = format_plot_data(sheet, SPREADSHEET_ID, cell_range)
    fig = plot_data(data_values, choice)
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
        choice = st.radio("Escolha o tipo de coordenograma", ("Fase", "Neutro"))
        choice_translated = "phase" if choice == "Fase" else "neutral"

        if st.button("Gerar Gráfico"):
            with st.spinner("Gerando gráfico..."):
                cell_range = phase_cells if choice == "Fase" else neutral_cells
                img_buffer, fig = format_and_plot(cell_range, choice_translated)
            st.pyplot(fig)
            st.success("Gráfico gerado com sucesso!")

        if st.button("Salvar no Google Drive"):
            with st.spinner("Salvando no Google Drive..."):
                cell_range = phase_cells if choice == "Fase" else neutral_cells
                img_buffer, _ = format_and_plot(cell_range, choice_translated)
                file_name = (
                    f"{st.session_state['title']}_COORDENOGRAMA_{choice.upper()}.jpeg"
                )
                upload_drive(img_buffer, file_name)
            st.success(f"Arquivo {file_name} salvo com sucesso no Google Drive!")


if __name__ == "__main__":
    main()
