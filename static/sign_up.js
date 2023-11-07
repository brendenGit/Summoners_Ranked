const signUpForm = document.getElementById("signUpForm")
const numberOfGamesValue = document.getElementById("number-of-games-value")
const number_of_games = document.getElementById("number_of_games")


number_of_games.addEventListener('input', function () {
    numberOfGamesValue.textContent = this.value;
});

// async function findPUUID(username) {
//     try {
//         const response = await axios.get(
//             `https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/${username}`,
//             {
//                 headers: {
//                     "X-Riot-Token": apiKey
//                 }
//             }
//         );
//         console.log(response.data);
//     } catch (error) {
//         // Handle errors here
//         console.error(error);
//     }
// }

// signUpForm.addEventListener("submit", async function (event) {
//     event.preventDefault(); // Prevent the default form submission

//     const usernameInput = document.getElementById("username");
//     const username = usernameInput.value;

//     if (username) {
//         findPUUID(username);
//     } else {
//         console.log("Username is empty");
//     }
// });
// signUpForm.addEventListener("submit", )