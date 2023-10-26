# League-Companions-LoC
A web app, “League Companions". Users can connect their League of Legends account, add friends to their LoC friends list, and compare League metrics across their 
friends for some friendly competition and bragging rights.

## Riot API 
[https://developer.riotgames.com/](https://developer.riotgames.com/)
### Obtaining Summoner Account Information
We use the following endpoint to search for finding a summoner. We will need to specify the region and summoner name. We must include our API key in the header parameters.
We will use this endpoint for account creation as well as adding friends.

`/lol/summoner/v4/summoners/by-name/{summonerName}`

The endpoint returns information about the summoner's account. We will want to remember to keep and save the:
- PUUID
- Summoner Name
- ProfileIconId

####Example:

`https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Brendinoo`

###Obtaining Match Data
We use the following endpoints to search for match information. We first need to find match IDs. We must include our API key in the header parameters.
We use the endpoint: 

`/lol/match/v5/matches/by-puuid/{puuid}/ids`

The endpoint returns a list of match IDs which we will perform further action on.

####Example:

`https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/yu6FoYvV64VOPORPBF93HhaksnHMuYsfbGuqTe55DF2zK1C33KmCfDAraB5UzEbUgeWrYpFS-RBeOQ/ids`

We now need to find the individual match data. We will use the list of match IDs to find specific match data. We must include our API key in the header parameters. 
We use the endpoint: 

`/lol/match/v5/matches/{matchId}`

We are then returned an object of match data which we will manipulate based on user input.

####Example:

`https://americas.api.riotgames.com/lol/match/v5/matches/NA1_4810500600`
