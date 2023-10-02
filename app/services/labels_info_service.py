from flask import current_app
import requests
from logging import getLogger

log = getLogger(__name__)

URL = current_app.config.get("LABELS_INFO_URL")

def get_data():
    
    error = None
    data = {}

    try:
        response = requests.get(URL)

        # check if response is ok
        response.raise_for_status()
        
        data = response.json()

    except requests.exceptions.RequestException as e:
        error = f"Error mientras se hacia la petición a la URL: {e}"

    except Exception as e:
        error = f"Error desconocido: {e}"

    return data, error



def get_labels_info(on_production):

    error = None

    if on_production:
        # TODO: to implement
        log.info("get_labels_info: on_production")
        data, error = get_data()
        
    else:
        log.info("get_labels_info: on_development")
        # load data from file 
        import json
        import os
        filepath = os.path.join(os.getcwd(), "tests/fixtures", "fake_labels_info.json")

        
        with open(filepath, "r") as f:
            data = json.load(f)

    labels_info = data.get("items", [])
        
    return labels_info, error
