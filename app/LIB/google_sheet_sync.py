import urllib
import os
import pickle
import pandas as pd

# GOOGLE
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SECRET_FILE_NAME = "client_secret.json"
SECRET_FOLDER = "database"
SECRET_FILE_PATH = os.path.join(os.getcwd(), SECRET_FOLDER, SECRET_FILE_NAME)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1kZITqxBmjPXLcv7NPsmRfuMuzj-Ko5X3BZGFpKe4nqQ"
RANGE = "A1:M1000"

BBDD_FOLDER = "database"
BBDD_FILE_NAME = "BBDD_DIVAIN_NEW.xlsx"
BBDD_PATH = os.path.join(BBDD_FOLDER, BBDD_FILE_NAME)
BBDD_PATH = os.path.join(os.getcwd(), BBDD_FOLDER, BBDD_FILE_NAME)

# function to check if the internet connection is available
def check_internet_connection():
    try:
        urllib.request.urlopen("http://google.com", timeout=1)
        return True
    except urllib.request.URLError as err:
        return False


# get the credentials from the secret file
def get_credentials():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SECRET_FILE_PATH, SCOPES
            )  # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_datashhet(creds, sheet_id, range):
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
    values = result.get("values", [])
    return values


def from_list_to_xlsx(values, path):
    df = pd.DataFrame(values[1:], columns=values[0])
    # df = pd.DataFrame(values)
    df.to_excel(path, index=False)


def reload_database():
	try:
		if check_internet_connection():
			creds = get_credentials()
			values = get_datashhet(creds, SPREADSHEET_ID, RANGE)
			from_list_to_xlsx(values, BBDD_PATH)
			return True, "Base de datos actualizada correctamente"
		else:
			return False, "No hay conexión a internet, no se ha podido actualizar la base de datos"
	except Exception as e:
		return False, f"Error al actualizar la base de datos: {e}"


if __name__ == "__main__":
    if check_internet_connection():
        creds = get_credentials()
        values = get_datashhet(creds, SPREADSHEET_ID, RANGE)
        if values:
            from_list_to_xlsx(values, BBDD_PATH)
    else:
        print("No internet connection available.")
