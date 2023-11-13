def get_perf_data(performances):
    """builds a data structure for performances of a specific leaderboard"""

    performances_data = []

    for performance in performances:
        
        performance_data = {
            "summoner_name": performance.summoner_name,
            "kills": performance.kills,
            "deaths": performance.deaths,
            "wins": performance.wins,
            "losses": performance.losses,
            "total_damage_dealt": performance.total_damage_dealt,
            "total_damage_taken": performance.total_damage_taken,
            "kda": performance.kda
            }
        
        performances_data.append(performance_data)

    return performances_data