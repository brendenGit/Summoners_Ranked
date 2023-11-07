import requests
from models import *

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
    

def get_summoner_friend_data(api_key, friend_summoner_name, friend_region):
    api_url = f"https://{friend_region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{friend_summoner_name}"
    headers = {
        "X-Riot-Token": api_key
    }

    try:
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as error:
        return None
    

def friends_performance(api_key, puuid, queue, num_games, ranked_by):
    friend = Friends.query.filter_by(friend_puuid=puuid).first()

    friend_region = 'americas' if friend.friend_region == 'NA1' else 'error'
    
    api_url = f"https://{friend_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&start=0&count={num_games}"
    headers = {
        "X-Riot-Token": api_key
    }

    try:
        response = requests.get(api_url, headers=headers)
        match_ids = response.json()
    except requests.exceptions.RequestException as error:
        return None
    score = 0
    for match_id in match_ids:
        api_url = f"https://{friend_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        try:
            response = requests.get(api_url, headers=headers)
            match_data = response.json()
            for player in match_data['info']['participants']:
                if player['puuid'] == puuid:
                    player_data = player
                    break

            if player_data is not None:
                value = player_data[ranked_by]
            else:
                print("Participant with the given puuid not found.")
            
            if ranked_by != 'win':
                score = score + value
            elif value == True:
                score += 1

        except requests.exceptions.RequestException as error:
            return None
    return score


def per_performance(api_key, puuid, queue, num_games, ranked_by):
    user = User.query.filter_by(puuid=puuid).first()

    region = 'americas' if user.region == 'NA1' else 'error'
    
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&start=0&count={num_games}"
    headers = {
        "X-Riot-Token": api_key
    }

    try:
        response = requests.get(api_url, headers=headers)
        match_ids = response.json()
    except requests.exceptions.RequestException as error:
        return None
    score = 0
    for match_id in match_ids:
        api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        try:
            response = requests.get(api_url, headers=headers)
            match_data = response.json()
            for player in match_data['info']['participants']:
                if player['puuid'] == puuid:
                    player_data = player
                    break

            if player_data is not None:
                value = player_data[ranked_by]
            else:
                print("Participant with the given puuid not found.")
            
            if ranked_by != 'win':
                score = score + value
            elif value == True:
                score += 1

        except requests.exceptions.RequestException as error:
            return None
    return score

    

# def match_result(api_key, match_id, ranked_by):

#     friend_region = 'americas' if friend.friend_region == 'NA1' else 'error'
    
#     api_url = f"https://{friend_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&start=0&count={num_games}"

#     headers = {
#         "X-Riot-Token": api_key
#     }

#     try:
#         response = requests.get(api_url, headers=headers)
#         response_data = response.json()
#         return response_data
#     except requests.exceptions.RequestException as error:
#         return None