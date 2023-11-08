const createAccount = document.getElementById("createAccountLink");

createAccount.addEventListener("click", function(e) {
    e.preventDefault()

    const loginForm = document.getElementById("loginForm");
    loginForm.classList.add("noDisplay");

    const signUpForm = document.getElementById("signUpForm");
    signUpForm.classList.remove("noDisplay");

    const loginLink = document.getElementById("loginLink");
    loginLink.classList.remove("noDisplay");
});

loginLink.addEventListener("click", function(e) {
    e.preventDefault()

    const loginForm = document.getElementById("loginForm");
    loginForm.classList.remove("noDisplay");

    const signUpForm = document.getElementById("signUpForm");
    signUpForm.classList.add("noDisplay");
});