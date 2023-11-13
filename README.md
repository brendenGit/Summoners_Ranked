# Summoner's Ranked 
[https://sr-web-service.onrender.com/](https://sr-web-service.onrender.com/)
A web app, Summoner's Ranked (SR). Users can connect their League of Legends account, add friends to their SR friends list, and compare League metrics across their 
friends for some friendly competition and bragging rights.

## Key Features
### Account Creation
We spent time on this feature to ensure the user created an account that would in turn show meaningful information.
By ensuring account creation was linked to League of Legends account we are able to provide accurate analytics.

### Adding Friends
A critical feature that supports our leaderboards. Allowing users to be able to add friends by summoner name. This feature is core to building out the leaderboards. This allows users to select which friends they
would like to view analytics on.

### Leaderboards
The main product of SR is to create a leaderboard of aggregated data across a certain number of games in a specific game type. We build a leaderboard based on this information
and initially sort it by total kills. 

The leaderboard can be sorted by any column allowing users to see who is performing the best in which categories.

## A Flow Through Summoner's Ranked
1. Visit SR and be prompted to sign in or create an account.
2. Create an account and log in
3. Add friends to your account by their summoner name
4. Create a leaderboard for the last 20 ARAM games to see who's been doing the best in which categories!
5. And that's it - a really simple but fun way to view some league data.
6. If you're feeling crazy make another leaderboard!

## Tech Stack
- **Python Packages:**
  - Bcrypt
  - Flask
  - Flask-Bcrypt
  - Flask-WTF
  - Jinja2
  - Requests (`requests==2.31.0`)
 
- **Web Technologies:**
  - HTML
  - CSS
  - JavaScript

- **ORM:**
  - SQLAlchemy (used by Flask by default, not explicitly mentioned in requirements.txt)
  - Torch (`torch==2.0.1`)

- **Deployed with:**
  - ElephantSQL
  - Render

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

#### Example:

`https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Brendinoo`

### Obtaining Match Data
We use the following endpoints to search for match information. We first need to find match IDs. We must include our API key in the header parameters.
We use the endpoint: 

`/lol/match/v5/matches/by-puuid/{puuid}/ids`

The endpoint returns a list of match IDs which we will perform further action on.

#### Example:

`https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/yu6FoYvV64VOPORPBF93HhaksnHMuYsfbGuqTe55DF2zK1C33KmCfDAraB5UzEbUgeWrYpFS-RBeOQ/ids`

We now need to find the individual match data. We will use the list of match IDs to find specific match data. We must include our API key in the header parameters. 
We use the endpoint: 

`/lol/match/v5/matches/{matchId}`

We are then returned an object of match data which we will manipulate based on user input.

#### Example:

`https://americas.api.riotgames.com/lol/match/v5/matches/NA1_4810500600`
