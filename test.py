import json

with open("piscine.json", "r") as file:
	users = json.load(file)

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

with open("piscine.csv", "w") as file:
	file.write(csv_content)