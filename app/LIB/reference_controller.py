#!/usr/bin/env python3
# coding: utf-8

import os
from pandas.core.frame import DataFrame
import xlrd
import pandas as pd

# excel_path = 'database\BBDD_DIVAIN.xlsx'
excel_path = "database/BBDD_DIVAIN_NEW.xlsx"

excel_path = os.path.join(os.getcwd(), excel_path)

columns_search = [
    "EAN 1 Litro",
    "EAN 1/2 Litro",
    "EAN BOTES",
    "EAN MUESTRAS",
    "N DIVAIN",
]

def get_str_value(obj, key):
    k = obj.get(key)
    if k is None:
        return ""

    value = k.values[0]

    if isinstance(value, str):
        return value.strip()
    return ""

def get_reference_data(idBotella):

    df = get_df()
    # if (isinstance(df, str)):
    #     print("#"*50)
    #     print(df)
    #     print("#"*50)

    resp = {"data": None, "error": "Referencia no encontrada"}

    # TODO: maneja la no conversión
    try:
        eanBotella = int(idBotella)

    except:
        resp["error"] = "Error: debe ingresar un número valido"
        return resp

    # prin ("#"*50)
    # print(columns_search)
    # # print(df.dtypes)
    # print("#"*50)
    if isinstance(df, DataFrame):
        for column in columns_search:

            if column != "N DIVAIN":
                row_reference = df.loc[df[column] == eanBotella]

            else:
                row_reference = df.loc[df[column] == idBotella]

                if row_reference.empty:
                    row_reference = df.loc[df[column] == eanBotella]

            if not row_reference.empty:
                # categoria = row_reference['CATEGORIA'].values[0]

                resp["data"] = {
                    "numero_divain": row_reference["N DIVAIN"].values[0],
                    "sexo": get_str_value(
                        row_reference, "SEXO"
                    ),  # row_reference['SEXO'].values[0].strip(),
                    "ean_botes": int(row_reference["EAN BOTES"].values[0]),
                    "ean_muestras": int(row_reference["EAN MUESTRAS"].values[0]),
                    "sku": get_str_value(row_reference, "SKU DIVAIN"),
                    "categoria": get_str_value(row_reference, "CATEGORIA"),
                    "caja": get_str_value(row_reference, "CAJA"),
                    "tapon": get_str_value(row_reference, "TAPON"),
                    "ingredientes": get_str_value(row_reference, "INGREDIENTES"),
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
