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


createItemFormSubmit = function(e) {
    e.preventDefault();

    let itemForm = e.submitter.parentNode;

    // create optional part of fetch
    options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": getCookieValue("csrf_access_token"),
        },
        credentials: 'same-origin',
        body: JSON.stringify({
		    "name": itemForm.elements["item-name"].value
	    })
    };

    category_id = itemForm.elements["item-category-id"].value;

    endpoint = "/category/" + category_id + "/item"

    handleFetchPromise( fetch(endpoint, options),
        // handle correct result
        (jsonData) => {
            console.log("Item created successfully");
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


window.addEventListener("load", (event) => {

document.getElementById("create-category-form").addEventListener("submit", createCategoryFormSubmit);
document.querySelectorAll(".create-item-form").forEach((itemForm) => {
    itemForm.addEventListener("submit", createItemFormSubmit)
});






const draggables = document.querySelectorAll(".item-div");
const droppables = document.querySelectorAll(".category-items-section");

let item_id = 0;

draggables.forEach((item) => {
    item.addEventListener("dragstart", (e) => {
        item.classList.add("is-being-dragged");

        item_id = e.target.querySelector('input[type="hidden"]').value;
    });

    item.addEventListener("dragend", () => {
        item.classList.remove("is-being-dragged");
    });
});

droppables.forEach((category) => {
    category.addEventListener("dragover", (e) => {
        e.preventDefault();

        const beingDragged = document.querySelector(".is-being-dragged");

        category.appendChild(beingDragged);
    });

    category.addEventListener("dragenter", (e) => {
        e.preventDefault();
    })

    category.addEventListener("drop", (e) => {
        console.log("dropped");

        const category_id = e.target.querySelector('input[type="hidden"]').value;


        options = {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-TOKEN": getCookieValue("csrf_access_token"),
            },
            credentials: 'same-origin',
            body: JSON.stringify({
		        "category_id": category_id
	        })
        };


        endpoint = "/item/" + item_id;

        handleFetchPromise( fetch(endpoint, options),
            // handle correct result
            (jsonData) => {
                console.log("Item moved successfully");
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

    });

});

});