import os
import pandas as pd

excel_path = "database/BBDD_DIVAIN_NEW.xlsx"

excel_path = os.path.join(os.getcwd(), excel_path)

columns_search = [
    "EAN 1 Litro",
    "EAN 1/2 Litro",
    "EAN BOTES",
    "EAN MUESTRAS",
    "N DIVAIN",
]

def get_reference_data(idBotella):
    df = get_df()

    resp = {"data": None, "error": "Referencia no encontrada"}

    try:
        eanBotella = int(idBotella)
    except:
        resp["error"] = "Error: debe ingresar un número valido"
        return resp

    if type(df) == pd.DataFrame:
        for column in columns_search:
            if column != "N DIVAIN":
                row_reference = df.loc[df[column] == eanBotella]
            else:
                row_reference = df.loc[df[column] == idBotella]
                if row_reference.empty:
                    row_reference = df.loc[df[column] == eanBotella]
            if not row_reference.empty:
                resp["data"] = {
                    "numero_divain": row_reference["N DIVAIN"].values[0],
                    "sexo": row_reference["SEXO"].values[0].strip(),
                    "ean_botes": int(row_reference["EAN BOTES"].values[0]),
                    "ean_muestras": int(row_reference["EAN MUESTRAS"].values[0]),
                    "sku": row_reference["SKU DIVAIN"].values[0].strip(),
                    "categoria": row_reference["CATEGORIA"].values[0].strip(),
                    "caja": row_reference["CAJA"].values[0].strip(),
                    "tapon": row_reference["TAPON"].values[0].strip(),
                    "ingredientes": row_reference["INGREDIENTES"].values[0].strip(),
                }
                resp["error"] = None
                break
    else:
        resp["error"] = df

    return resp

def get_df():
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        return f"Error: {e}"

    return df
