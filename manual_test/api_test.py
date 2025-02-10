import requests

ss = requests.Session()

url = "http://127.0.0.1:8000"

# pl_profile = "eyJzIjogIld6SXNNekU0TlRnMU9ESmQ6MXRhTVZhOlZJVHBVaWZUX20zYUNkT0V6QTNsR1JQQXdhLVRLakhVYnk0ZEphR0VVZ3ciLCAidSI6IHsiaWQiOiAzMTg1ODU4MiwgImZuIjogIlNhbSIsICJsbiI6ICJIYW5yYWhhbiIsICJmYyI6IDQzfX0="
# datadome = "mcm0HxDxR4YbQSbC5zmgLGNCJp0WXnTB_4IXvsizc8ZYnPNtzon2w35ZvA_d2dlQqnMLkG_6723DPzRb978zqSUSx9ej1V8t5BY4KAzQEiaSDLb0h8nVI8u~uieeEGhg"

# data = {
#     "email": "samhanrahan16@gmail.com",
#     "password": "mypassword",
#     "manager_id": 6171224,
#     "fpl_cookie": pl_profile,
#     "datadome_cookie": datadome,
# }
# r = ss.post(f"{url}/create_account", json=data)
# print(r.text)

data = {
    "fpl_account": {
        "fpl_email": "samhanrahan16@gmail.com",
        "fpl_password": "Imperial16!1969",
    }
}

r = ss.get(f"{url}/my_team/fixture_difficulty", json=data)
print(r.text)
# url = "https://users.premierleague.com/accounts/login/"
# payload = {
#     "password": "Imperial16!1969",
#     "login": "samhanrahan16@gmail.com",
#     "redirect_uri": "https://fantasy.premierleague.com/a/login",
#     "app": "plfpl-web",
# }
# r = ss.post(url, data=payload)
# print(r.text)

# r = ss.get("https://fantasy.premierleague.com/api/entry/6171224/event/22/picks/")
# print(r.text)


# async def my_team(user_id):
#     async with aiohttp.ClientSession() as session:
#         fpl = FPL(session)
#         await fpl.login(
#             email="samhanrahan16@gmail.com", password="Imperial16!1969", cookie=cookie
#         )
#         user = await fpl.get_user(user_id)
#         print(user)
#         team = await user.get_team()
#     print(team)


# asyncio.run(my_team(6171224))

# print("Now trying the API")
# r = ss.get("https://fantasy.premierleague.com/api/my-team/6171224/")
# print(r.text)

# r = ss.post(url, data=data, headers=headers)
# print(r.text)
# data = {"email": "samhanrahan16@gmail.com", "password": "mypassword"}
# r = ss.post(f"{url}/user_login", json=data)
# print(r.text)

# data = {"names": ["Manchester City"]}
# r = ss.get(f"{url}/teams/rating", json=data)
# print(r.json())

# data_put = {
#     "teams": [
#         {"name": "Chelsea", "home_rating": 7, "away_rating": 4},
#         {"name": "Man City", "home_rating": 9, "away_rating": 7},
#     ]
# }
# r = ss.put(f"{url}/teams/rating", json=data_put)
# print(r.json())

# data_post = {
#     "teams": [
#         {"name": "Chelsea", "home_rating": 9, "away_rating": 4},
#         {"name": "Newcastle United", "home_rating": 7, "away_rating": 3},
#     ]
# }
# r = ss.post(f"{url}/teams/rating", json=data_post)
# print(r.json())

# r = ss.post(f"{url}/fpl/fixtures")
# r = ss.get(f"{url}/fixtures/table")
# r = ss.post(f"{url}/update/static")
# r = ss.post(
#     f"{url}/login",
#     json={"email": "samhanrahan16@gmail.com", "password": "Imperial16!1968"},
# )
# print(r.text)
