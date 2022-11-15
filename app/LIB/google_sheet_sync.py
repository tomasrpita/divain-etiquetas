
import urllib

# function to check if the internet connection is available
def check_internet_connection():
	try:
		urllib.request.urlopen('http://google.com', timeout=1)
		return True
	except urllib.request.URLError as err:
		return False


# get
