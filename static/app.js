const createAccount = document.getElementById("createAccountLink");

createAccount.addEventListener("click", function(e) {
    e.preventDefault()

    const loginFormDiv = document.getElementById("loginFormDiv");
    loginFormDiv.classList.add("noDisplay");

    const signUpFormDiv = document.getElementById("signUpFormDiv");
    signUpFormDiv.classList.remove("noDisplay");

    const loginLink = document.getElementById("loginLink");
    loginLink.classList.remove("noDisplay");
});

loginLink.addEventListener("click", function(e) {
    e.preventDefault()

    const loginFormDiv = document.getElementById("loginFormDiv");
    loginFormDiv.classList.remove("noDisplay");

    const signUpFormDiv = document.getElementById("signUpFormDiv");
    signUpFormDiv.classList.add("noDisplay");
});