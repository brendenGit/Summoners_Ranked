import requests

def get_summoner_data(api_key, username, region):
    api_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}"
    headers = {
        "X-Riot-Token": api_key
    }

    try:
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as error:
        return None