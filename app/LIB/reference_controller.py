#!/usr/bin/env python3
# coding: utf-8

import os

from pandas.core.frame import DataFrame
import xlrd
import pandas as pd

excel_path = './database/BBDD_DIVAIN.xlsx'
columns_search = [' Prady 1 litro', 'Natur 1/2', 'Natur 1 litro']



def get_reference_data(eanBotella):

    df = get_df()
    resp = {
        'data': None,
        'error': "Referencia no encontrada"
    }

    # TODO: maneja la no conversión
    try: 
        eanBotella = int(eanBotella)
    except: 
        resp['error'] = "Error: debe ingresar un número valido"
        return resp


    if isinstance(df, DataFrame):
        for column in columns_search:
            row_reference = df.loc[df[column] == eanBotella]
            if not row_reference.empty:
                resp['data'] = {
                    'numero_divain': int(row_reference['DIVAIN'].values[0]), 
                    'sexo': row_reference['SEXO'].values[0],
                    'ean_13': int(row_reference['EAN 13'].values[0]),
                    'sku': row_reference['SKU'].values[0]
                    }
                resp['error'] = None
                break
    else:
        resp['error'] = df

    return resp

def get_df():

    try:
        df = pd.read_excel(excel_path)
    
    except Exception as e:
        return f'Error: {e}'

    return df

