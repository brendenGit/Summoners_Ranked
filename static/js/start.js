const createAccount = document.getElementById("createAccountLink");
//Listen for a click on our sign up link to show the proper forms. 
createAccount.addEventListener("click", function (e) {
    e.preventDefault()

    const loginForm = document.getElementById("loginForm");
    loginForm.classList.add("noDisplay");

    const signUpForm = document.getElementById("signUpForm");
    signUpForm.classList.remove("noDisplay");

    const loginLink = document.getElementById("loginLink");
    loginLink.classList.remove("noDisplay");
});

//Listen for a click on our login link to show the proper forms. 
loginLink.addEventListener("click", function (e) {
    e.preventDefault()

    const loginForm = document.getElementById("loginForm");
    loginForm.classList.remove("noDisplay");

    const signUpForm = document.getElementById("signUpForm");
    signUpForm.classList.add("noDisplay");
});


const signUpForm = document.getElementById("signUpForm");
// Make sign up request
const signUp = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    try {
        const response = await axios.post('/sign_up', formData);

        if (response.status === 200) {
            // Assuming the server sends the user to the home page after successful login
            window.location.href = response.request.responseURL;
        }
    } catch (error) {
        console.log(error);
        removeAlerts();
        const errorAlert = addErrorAlert(error);
        signUpForm.appendChild(errorAlert);
    }
};
signUpForm.addEventListener("submit", signUp);



const loginForm = document.getElementById("loginForm");
// Make login request
const login = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    try {
        const response = await axios.post('/login', formData);

        if (response.status === 200) {
            // Assuming the server sends the user to the home page after successful login
            window.location.href = response.request.responseURL;
        }
    } catch (error) {
        console.log(error);
        removeAlerts();
        const errorAlert = addErrorAlert(error);
        loginForm.appendChild(errorAlert);
    }
};
loginForm.addEventListener("submit", login);