registerFormSubmit = function(e) {
    e.preventDefault();

    let registerForm = document.getElementById("register-form");


    let username = registerForm.elements["username"].value;
    let password = registerForm.elements["password"].value;
    let confirm = registerForm.elements["password-repeat"].value;

    // not matching? Error
    if(password != confirm) {
        showErrorMessage("400: Password and Repeated Password don't match");
        return;
    }

    // create optional part of fetch
    options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
		    "username": username,
		    "password": password
	    })
    };


    handleFetchPromise( fetch("/user", options),
        // handle correct result
        (jsonData) => {
            console.log("Registered successfully");
            window.location.replace("/login");
        },

        // handle api error
        (apiError) => {
            // get status number
            // TODO: this is garbage, fix it
            let messageText = "";
            messageText += apiError.status;
            messageText += " ";
            messageText += apiError.statusText;
            messageText += ": ";

            apiError.json().then((apiErrorJson) => {
                messageText += apiErrorJson["msg"];

                showErrorMessage(messageText);
            });
        },

        // handle fetch error
        (fetchError) => {
            let messageText = "";
            messageText += fetchError.status;
            messageText += " ";
            messageText += fetchError.statusText;

            showErrorMessage(messageText);
        }

    );
}

document.getElementById("register-form").addEventListener("submit", registerFormSubmit)