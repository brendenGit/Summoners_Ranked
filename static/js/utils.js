// helper functions to update errors
//creates an error alert element and returns it to be appended
const addErrorAlert = (error) => {
    const errorAlert = document.createElement('blaze-alert');
    errorAlert.setAttribute('open', '');
    errorAlert.setAttribute('type', 'error');
    errorAlert.textContent = error.response.data.error;

    return errorAlert;
}

//creates a success alert element and returns it to be appended
const addSuccessAlert = (successData) => {
    const successAlert = document.createElement('blaze-alert');
    successAlert.setAttribute('open','');
    successAlert.setAttribute('dismissible','');
    successAlert.setAttribute('type','success');
    successAlert.textContent = successData.success;

    return successAlert;
}

//removes all alerts on the page
const removeAlerts = () => {
    const alerts = document.querySelectorAll('blaze-alert');
    
    alerts.forEach(alert => {
        alert.remove();
    });
};
