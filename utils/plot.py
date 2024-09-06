import io

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter


def format_plot_data(sheet, spreadsheet_id, cells):
    result = (
        sheet.values().batchGet(spreadsheetId=spreadsheet_id, ranges=cells).execute()
    )
    value_ranges = result.get("valueRanges", [])

    plot_data = []
    for value_range in value_ranges:
        values = value_range.get("values", [])
        float_values = np.array(
            [str(value[0]).replace(",", ".") for value in values if value],
            dtype=np.float64,
        )
        plot_data.append(float_values)

    return plot_data


def plot_data(data):
    fig, ax = plt.subplots(figsize=(10, 15))

    ax.loglog(
        data[0],
        data[1],
        label="FASE MONTANTE",
        linestyle="-",
        color="red",
    )
    ax.loglog(
        data[2],
        data[3],
        label="NEUTRO MONTANTE",
        linestyle="--",
        color="dodgerblue",
    )
    ax.loglog(
        data[4],
        data[5],
        label="FASE JUSANTE",
        linestyle="-",
        color="black",
    )
    ax.loglog(
        data[6],
        data[7],
        label="NEUTRO JUSANTE",
        linestyle="--",
        color="limegreen",
    )
    ax.loglog(
        data[8],
        data[9],
        marker=".",
        label="I CARGA",
        linestyle=":",
        color="orchid",
    )
    ax.loglog(
        data[10],
        data[11],
        marker=".",
        label="ANSI",
        linestyle=":",
        color="royalblue",
    )
    ax.loglog(
        data[12],
        data[13],
        marker=".",
        label="IMAG",
        linestyle=":",
        color="fuchsia",
    )
    ax.loglog(
        data[14],
        data[15],
        marker=".",
        label="ICC3F",
        linestyle=":",
        color="darkgreen",
    )
    ax.loglog(
        data[16],
        data[17],
        marker=".",
        label="ICC1F",
        linestyle=":",
        color="darkorange",
    )
    ax.loglog(
        data[18],
        data[19],
        label="51 GS MONTANTE",
        linestyle=":",
        color="darkred",
    )
    ax.loglog(
        data[20],
        data[21],
        label="51 GS JUSANTE",
        linestyle=":",
        color="orange",
    )
    ax.loglog(data[22], data[23], label="ELO", linestyle="-", color="brown")

    ax.set(
        xlabel="Corrente (A)",
        ylabel="Tempo (s)",
        xlim=(0.1, 10000),
        ylim=(0.01, 1000),
        title="COORDENOGRAMA FASES E NEUTRO\nDISJUNTOR GERAL DA CABINE X CONCESSIONÁRIA",
    )

    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    ax.grid(which="both", axis="both", linestyle="-")

    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="jpeg")
    img_buffer.seek(0)

    return img_buffer, fig
