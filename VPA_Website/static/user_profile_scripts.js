createProjectFormSubmit = function(e) {
    e.preventDefault();

    let projectForm = document.getElementById("create-project-form");

    cookies = document.cookie;

    // create optional part of fetch
    options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": "L",
        },
        credentials: 'same-origin',
        body: JSON.stringify({
		    "name": projectForm.elements["project-name"].value,
		    "desc": projectForm.elements["project-desc"].value
	    })
    };


    handleFetchPromise( fetch("/project", options),
        // handle correct result
        (jsonData) => {
            console.log("Project created successfully");
            window.location.reload();
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

document.getElementById("create-project-form").addEventListener("submit", createProjectFormSubmit)