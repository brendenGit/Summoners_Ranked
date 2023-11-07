



def get_perf_data(performances):
    """builds a data structure for performances of a specific leaderboard"""

    performances_data = []

    for performance in performances:
        performance_data = {
            "summoner_name": performance.summoner_name,
            "perf_metric": performance.perf_metric,
            "score": performance.score,
            }
        performances_data.append(performance_data)

    return performances_data