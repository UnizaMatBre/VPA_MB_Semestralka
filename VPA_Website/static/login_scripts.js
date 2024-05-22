loginFormSubmit = function(e) {
    e.preventDefault();

	let loginForm = document.getElementById("login-form");

    // create optional part of fetch
    options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
		    "username": loginForm.elements["username"].value,
		    "password": loginForm.elements["password"].value
	    })
    };



    handleFetchPromise( fetch("/login", options),
        // handle correct result
        (jsonData) => {
            console.log("Login successfully");
            window.location.replace("/index");
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

    )
}


document.getElementById("login-form").addEventListener("submit", loginFormSubmit)