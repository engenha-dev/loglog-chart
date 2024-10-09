def get_ids(idType):
    rowChosen = 1 if idType == "sheets" else 2
    try:
        with open("urls.txt", "r", encoding="UTF-8") as file:
            rows = file.readlines()
            row = rows[rowChosen - 1].strip()
            url = row.split("=")[1]
            fileId = get_sheet_id(url) if idType == "sheets" else get_drive_id(url)
            return fileId
    except FileNotFoundError:
        return "Arquivo não encontrado."


def get_sheet_id(url):
    parts = url.split("/")
    range_d = parts.index("d")
    return parts[range_d + 1]


def get_drive_id(url):
    clean_url = url.split("?")[0]
    parts = clean_url.split("/")
    return parts[-1]
