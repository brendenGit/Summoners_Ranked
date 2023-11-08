const numGamesValue = document.getElementById("number-of-games-value")
const number_of_games = document.getElementById("number_of_games")

number_of_games.addEventListener('input', function () {
    numGamesValue.textContent = this.value;
});