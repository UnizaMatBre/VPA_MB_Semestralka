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

    let itemForm = document.getElementById("create-item-form");

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

document.getElementById("create-category-form").addEventListener("submit", createCategoryFormSubmit);
document.getElementById("create-item-form"    ).addEventListener("submit", createItemFormSubmit);


const draggables = document.querySelectorAll(".item-div");
const droppables = document.querySelectorAll(".category-items-section");

draggables.forEach((item) => {
    item.addEventListener("dragstart", () => {
        item.classList.add("is-being-dragged");
    });

    item.addEventListener("dragend", () => {
        item.classList.remove("is-being-dragged");
    });
});

droppables.forEach((category) => {
    category.addEventListener("dragover", (e) => {
        e.preventDefault()

        const beingDragged = document.querySelector(".is-being-dragged");

        category.appendChild(beingDragged);
    });

});