import requests
import os
from dotenv import load_dotenv
import json
import datetime
from time import sleep

load_dotenv()
creds = None
BASE_URL = "https://api.intra.42.fr"
UID = os.getenv("42_APP_UID")
SECRET = os.getenv("42_APP_SECRET")

def get_access_token():
	url = f"{BASE_URL}/oauth/token?grant_type=client_credentials&client_id={UID}&client_secret={SECRET}"
	req = requests.post(
		url
	)
	data = req.json()
	return (data)

def GET(url):
	headers = {
		"Authorization": f"Bearer {creds.get("access_token")}"
	}
	req = requests.get(url, headers=headers)
	data = req.json()
	return data

def get_cursus():
	url = f"{BASE_URL}/v2/cursus?page=1"
	return GET(url)

def get_user(username: str):
	url = f"{BASE_URL}/v2/users/{username}"
	return GET(url)

def get_cursus_users(cursus_id: int, begin_at: str, page: int):
	url = f"{BASE_URL}/v2/cursus/{str(cursus_id)}/cursus_users?page[number]={str(page)}&page[size]=100&filter[campus_id]=1&filter[begin_at]={begin_at}"
	return GET(url)

# get creds
creds = get_access_token()

if creds.get("access_token") == None:
	print(f"Error, couldnt get an access token, \n{creds}")
	exit(1)

# Fetch user
username = input("Enter your username > ")
user_data = get_user(username)
if user_data.get("login") == None:
	print("bad username")
	exit(1)

# Get piscine
piscine = [elem for elem in user_data.get("cursus_users") if elem.get("grade") == "Pisciner"][0]
piscine_begin_at = piscine.get("begin_at")

# Fetch piscine cursus begin_at attr
users = []
page = 1
while (True):
	piscine_data = get_cursus_users(9, piscine_begin_at, page)
	if len(piscine_data) == 0:
		break
	users += piscine_data
	print(f"Fetched {len(piscine_data)} users (total: {len(users)}) (page n{page})")
	page += 1
	sleep(1)

print(f"Sucessfully fetched {len(users)} users")
# with open("piscine.json", "w") as file:
	# json.dump(users, file, indent=4)

# creating csv file
csv_content = "id;first_name;last_name;login;level;profile_url;profile_picture_url\n"
for user in users:
	csv_content += f"{user.get("id")};"
	user_obj = user.get("user")
	if user_obj:
		csv_content += f"{user_obj.get("first_name")};"
		csv_content += f"{user_obj.get("last_name")};"
		csv_content += f"{user_obj.get("login")};"
		csv_content += f"{user.get("level")};"
		csv_content += f"https://profile.intra.42.fr/users/{user_obj.get("login")};"
		csv_content += f"{user_obj.get("image").get("link")}"
	csv_content += "\n"
with open(f"{username}_piscine_users.csv", "w") as file:
	file.write(csv_content)