createCategoryFormSubmit = function(e) {
    e.preventDefault();

    let categoryForm = document.getElementById("create-category-form");

    // create optional part of fetch
    options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": getCookieValue("csrf_access_token"),
        },
        credentials: 'same-origin',
        body: JSON.stringify({
		    "name": categoryForm.elements["category-name"].value
	    })
    };

    project_id = categoryForm.elements["category-project-id"].value;

    endpoint = "/project/" + project_id + "/category"

    handleFetchPromise( fetch(endpoint, options),
        // handle correct result
        (jsonData) => {
            console.log("Category created successfully");
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

document.getElementById("create-category-form").addEventListener("submit", createCategoryFormSubmit)