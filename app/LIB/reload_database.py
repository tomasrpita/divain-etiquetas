
from flask import current_app
from app.LIB import google_sheet_sync

def run() -> None:
	log = current_app.logger
	reload, message = google_sheet_sync.reload_database()
	if reload:
		log.info(message)
	else:
		log.error(message)
