import io

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter

from utils.google import get_batch_values, get_sheet_service
from utils.ids import get_ids


def format_plot_data(sheet, spreadsheet_id, cells):
    result = (
        sheet.values().batchGet(spreadsheetId=spreadsheet_id, ranges=cells).execute()
    )
    value_ranges = result.get("valueRanges", [])

    plot_data = []
    for value_range in value_ranges:
        values = value_range.get("values", [])

        float_values = []
        for value in values:
            if value and value[0] not in ["", "#DIV/0!"]:
                str_value = str(value[0]).replace(",", ".")

                if str_value.count(".") > 1:
                    parts = str_value.split(".")
                    str_value = "".join(parts[:-1]) + "." + parts[-1]

                try:
                    float_values.append(float(str_value))
                except ValueError:
                    float_values.append(0)
            else:
                float_values.append(0)

        plot_data.append(np.array(float_values, dtype=np.float64))

    return plot_data


def plot_data(data, plot_type):
    fig, ax = plt.subplots(figsize=(10, 15))

    def contains_zero(x, y):
        return np.any(x == 0) or np.any(y == 0)

    phase_ranges = [
        "Dados_Gráficos!B3",
        "Dados_Gráficos!J3",
        "Dados_Gráficos!R3",
        "Dados_Gráficos!U3",
        "Dados_Gráficos!AG3",
        "Dados_Gráficos!AJ3",
        "Dados_Gráficos!AP3",
        "Dados_Gráficos!AY3",
        "Dados_Gráficos!BE3",
        "Dados_Gráficos!BH3",
        "Dados_Gráficos!BK3",
        "Dados_Gráficos!BN3",
        "Dados_Gráficos!BQ3",
        "Dados_Gráficos!BT3",
        "Dados_Gráficos!BW3",
        "Dados_Gráficos!BZ3",
        "Dados_Gráficos!CC3",
        "Dados_Gráficos!CF3",
        "Dados_Gráficos!CI3",
        "Dados_Gráficos!CL3",
        "Dados_Gráficos!CO3",
        "Dados_Gráficos!CR3",
        "Dados_Gráficos!DP3",
    ]

    neutral_ranges = [
        "Dados_Gráficos!F3",
        "Dados_Gráficos!N3",
        "Dados_Gráficos!X3",
        "Dados_Gráficos!AA3",
        "Dados_Gráficos!AD3",
        "Dados_Gráficos!AG3",
        "Dados_Gráficos!AM3",
        "Dados_Gráficos!AS3",
        "Dados_Gráficos!AV3",
        "Dados_Gráficos!BB3",
        "Dados_Gráficos!CU3",
        "Dados_Gráficos!CX3",
        "Dados_Gráficos!DA3",
        "Dados_Gráficos!DD3",
        "Dados_Gráficos!DG3",
        "Dados_Gráficos!DJ3",
        "Dados_Gráficos!DM3",
    ]

    SPREADSHEET_ID = get_ids("sheets")
    sheet = get_sheet_service()
    phase_values = get_batch_values(sheet, SPREADSHEET_ID, phase_ranges)
    neutral_values = get_batch_values(sheet, SPREADSHEET_ID, neutral_ranges)

    labels_and_styles_phase = [
        (label, linestyle, color)
        for label, linestyle, color in zip(
            phase_values,
            [
                "-",
                "-",
                "-",
                "-",
                "--",
                "--",
                "-",
                "-",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "-",
            ],
            [
                "red",
                "black",
                "darkgreen",
                "orange",
                "purple",
                "dodgerblue",
                "deeppink",
                "olive",
                "cyan",
                "lime",
                "khaki",
                "lightpink",
                "darksalmon",
                "chocolate",
                "bisque",
                "cyan",
                "lime",
                "khaki",
                "lightpink",
                "darksalmon",
                "chocolate",
                "bisque",
                "seagreen",
            ],
        )
    ]

    labels_and_styles_neutral = [
        (label, linestyle, color)
        for label, linestyle, color in zip(
            neutral_values,
            [
                "-",
                "-",
                "-",
                "-",
                "-",
                "--",
                "--",
                "-",
                "-",
                "-",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
                "--",
            ],
            [
                "dodgerblue",
                "lightgreen",
                "darkgreen",
                "orange",
                "darkred",
                "purple",
                "red",
                "deeppink",
                "gold",
                "olive",
                "cyan",
                "lime",
                "khaki",
                "lightpink",
                "darksalmon",
                "chocolate",
                "bisque",
            ],
        )
    ]

    labels_and_styles = (
        labels_and_styles_phase if plot_type == "phase" else labels_and_styles_neutral
    )
    title = (
        "COORDENOGRAMA DE FASE" if plot_type == "phase" else "COORDENOGRAMA DE NEUTRO"
    )

    for i in range(0, len(data), 2):
        if (
            i + 1 < len(data)
            and len(data[i]) > 0
            and not contains_zero(data[i], data[i + 1])
        ):
            label, linestyle, color = labels_and_styles[i // 2]
            ax.loglog(
                data[i], data[i + 1], label=label, linestyle=linestyle, color=color
            )

    ax.set(
        xlabel="Corrente (A)",
        ylabel="Tempo (s)",
        xlim=(0.1, 10000),
        ylim=(0.01, 1000),
        title=title,
    )

    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.6, box.height])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=1, fontsize="small")

    ax.grid(which="both", axis="both", linestyle="-")

    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="jpeg")
    img_buffer.seek(0)

    return img_buffer, fig
