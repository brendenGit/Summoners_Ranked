//////////////////////////////////////////////////////////////////////////////////////////////////////
//Add friend form funcs

const addFriendForm = document.getElementById("addFriendForm");
const friendsSelection = document.getElementById("friendsSelection");

function createFriendElement(friend) {
    const label = document.createElement('label');
    label.textContent = friend.friend_summoner_name;

    const input = document.createElement('input');
    input.type = 'checkbox';
    input.value = friend.friend_puuid;
    input.name = 'selected_friends';

    label.appendChild(input);
    friendsSelection.appendChild(label);
}


const addFriend = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target)
    console.log(formData)

    axios.post('/add_friend', formData)
        .then(response => {
            const addedFriend = response.data;

            if (addedFriend.hasOwnProperty('success')) {
                console.log('success');
                createFriendElement(addedFriend);
            }


        })
        .catch(error => {
            // Handle errors
            console.error('Error:', error);
        });
};

addFriendForm.addEventListener("submit", addFriend);



//////////////////////////////////////////////////////////////////////////////////////////////////////
//Leaderboard Funcs

//Leaderboard creation form funcs
const numGamesValue = document.getElementById("number-of-games-value")
const number_of_games = document.getElementById("number_of_games")

number_of_games.addEventListener('input', function () {
    numGamesValue.textContent = this.value;
});


const createLeaderboardForm = document.getElementById("create_leaderboard_form");
const leaderboardBody = document.getElementById("leaderboardBody");

//Create a row and fill that row with cells. Then append the row to the table to build the leaderboard
function createLeaderboard(performance) {

    const row = document.createElement('tr');
    row.classList.add('c-table__row');

    for (const key in performance) {
        const cell = document.createElement('td');
        cell.classList.add('c-table__cell');
        cell.textContent = performance[key];
        row.appendChild(cell);
    }

    leaderboardBody.appendChild(row);
}

//Get data for leaderboard
const getLeaderboardData = async (e) => {
    e.preventDefault();

    const rowsToRemove = leaderboardTable.querySelectorAll('tr:not(thead tr)');
    rowsToRemove.forEach(row => row.remove());

    const formData = new FormData(e.target)

    axios.post('/create_leaderboard', formData)
        .then(response => {
            performances = response.data;

            const ogOrder = ['summoner_name', 'kills', 'deaths', 'wins', 'losses', 'total_damage_dealt', 'total_damage_taken', 'kda'];
            const sortedData = performances.map(performance => {
                const sortedObject = {};
                ogOrder.forEach(key => {
                    sortedObject[key] = performance[key];
                });
                return sortedObject;
            });

            sortedData.sort((a, b) => b.kills - a.kills); // Sorting by kills, adjust as needed

            sortedData.forEach(createLeaderboard);
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

createLeaderboardForm.addEventListener("submit", getLeaderboardData);