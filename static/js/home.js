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

    axios.post('/add_friend', formData)
        .then(response => {
            removeAlerts();
            const addedFriend = response.data;
            console.log(addedFriend);

            if (addedFriend.hasOwnProperty('success')) {
                const successAlert = addSuccessAlert(addedFriend);
                addFriendForm.appendChild(successAlert);
                createFriendElement(addedFriend);
                addFriendForm.reset();
                setTimeout(removeAlerts, 3000);
            }
        })
        .catch(error => {
            console.log(error);
            removeAlerts();
            const errorAlert = addError(error);
            addFriendForm.appendChild(errorAlert);
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

const loader = document.getElementById("loader");
//Get data for leaderboard
const getLeaderboardData = async (e) => {
    e.preventDefault();

    const subButton = createLeaderboardForm.querySelector('button[type="submit"]');
    subButton.disabled = true;
    subButton.innerText = '. . .';

    const rowsToRemove = leaderboardTable.querySelectorAll('tr:not(thead tr)');
    rowsToRemove.forEach(row => row.remove());

    loader.classList.remove("noDisplay");

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

            sortedData.sort((a, b) => b.kills - a.kills);
            loader.classList.add("noDisplay");
            sortedData.forEach(createLeaderboard);
            const sortByColumn = document.getElementById("sortStart");
            sortByColumn.classList.add('sorted');
            subButton.disabled = false;
            subButton.innerText = 'Create Leaderboard';
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

createLeaderboardForm.addEventListener("submit", getLeaderboardData);

//sort table by index
function sortTable(columnIndex, column) {

    const currSort = document.querySelector('.sorted');
    if (currSort) {
        currSort.classList.remove('sorted');
    }
    column.classList.add('sorted')

    let leaderboardTable, rows, switching, i, x, y, shouldSwitch;
    leaderboardTable = document.getElementById("leaderboardTable");
    switching = true;

    while (switching) {
        switching = false;
        rows = leaderboardTable.rows;
        console.log(rows);

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[columnIndex];
            console.log(x.innerHTML);
            y = rows[i + 1].getElementsByTagName("td")[columnIndex];
            console.log(y.innerHTML);

            if (parseFloat(x.innerText) < parseFloat(y.innerText)) {
                shouldSwitch = true;
                break;
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

const headers = document.querySelectorAll('.sortable');
//add event listeners to headers
headers.forEach(header => {
    header.addEventListener('click', function () {
        const columnIndex = this.getAttribute('data-index');
        sortTable(columnIndex, this);
    });
});