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

    labels_and_styles_phase = [
        ("Fase Concessionária NEOENERGIA SUDESTE", "-", "red"),
        ("Fase DISJUNTOR GERAL", "-", "black"),
        ("Corrente de Curto (Icc3F)", "-", "darkgreen"),
        ("Corrente de Curto (Icc2F)", "-", "orange"),
        ("Corrente de Carga (I Carga)", "--", "purple"),
        ("Corrente de Partida Fase (I Partida F)", "--", "dodgerblue"),
        ("Corrente de Magnetização (I mag)", "-", "deeppink"),
        ("Corrente de Magnetização do menor Trafo (I mag menor Trafo)", "-", "olive"),
        ("ANSI TRAFO 500", "--", "cyan"),
        ("ANSI TRAFO 500", "--", "lime"),
        ("ANSI TRAFO 500", "--", "khaki"),
        ("ANSI TRAFO 500", "--", "lightpink"),
        ("ANSI TRAFO 500", "--", "darksalmon"),
        ("ANSI TRAFO 500", "--", "chocolate"),
        ("ANSI TRAFO 500", "--", "bisque"),
        ("Curva de dano TRAFO 500", "--", "cyan"),
        ("Curva de dano TRAFO 500", "--", "lime"),
        ("Curva de dano TRAFO 500", "--", "khaki"),
        ("Curva de dano TRAFO 500", "--", "lightpink"),
        ("Curva de dano TRAFO 500", "--", "darksalmon"),
        ("Curva de dano TRAFO 500", "--", "chocolate"),
        ("Curva de dano TRAFO 500", "--", "bisque"),
        ("ELO 65K", "-", "seagreen"),
    ]

    labels_and_styles_neutral = [
        ("Neutro Concessionária NEOENERGIA SUDESTE", "-", "dodgerblue"),
        ("Neutro DISJUNTOR GERAL", "-", "lightgreen"),
        ("Corrente de Curto (IccFT -Máx.)", "-", "darkgreen"),
        ("Corrente de Curto (IccFT -Mín.)", "-", "orange"),
        ("51GS Concessionária NEOENERGIA SUDESTE", "-", "darkred"),
        ("Corrente de Carga (I Carga)", "--", "purple"),
        ("Corrente de Partida Neutro (I Partida N)", "--", "red"),
        ("Corrente de Magnetização Residual (I mag res.)", "-", "deeppink"),
        ("51GS DISJUNTOR GERAL", "-", "gold"),
        (
            "Corrente de Magnetização Residual do menor Trafo (I mag res. menor Trafo)",
            "-",
            "olive",
        ),
        ("NANSI TRAFO 500", "--", "cyan"),
        ("NANSI TRAFO 500", "--", "lime"),
        ("NANSI TRAFO 500", "--", "khaki"),
        ("NANSI TRAFO 500", "--", "lightpink"),
        ("NANSI TRAFO 500", "--", "darksalmon"),
        ("NANSI TRAFO 500", "--", "chocolate"),
        ("NANSI TRAFO 500", "--", "bisque"),
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
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    ax.grid(which="both", axis="both", linestyle="-")

    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="jpeg")
    img_buffer.seek(0)

    return img_buffer, fig
