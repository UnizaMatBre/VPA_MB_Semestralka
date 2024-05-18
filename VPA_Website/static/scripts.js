/**
* Function that simplifies handling of fetch promises
*
* \fetchPromise : promise returned by fetch call
* \correctHandler    : handler for response without errors. Accepts body of response in json
* \apiErrorHandler   : handler for response with error from api. Accepts response itself
* \fetchErrorHandler : handler for errors from fetch (like network error). Accepts response itself
*/
handleFetchPromise = function(fetchPromise, correctHandler, apiErrorHandler, fetchErrorHandler) {
    fetchPromise
        .then((response) => {
            // handle error response
	        if(!response.ok) {
	            return Promise.reject(response);
	        }

            // turn ok response into json
	        return response.json();

        })
        .then(correctHandler)
        .catch((error) => {
            if(typeof error.json === "function") {
                apiErrorHandler(error);
            }
            else {
                fetchErrorHandler(error);
            }
        });
}



showErrorMessage = function(messageText) {
    const messageSection = document.getElementById("message-section");

    messageSection.style.display = "flex";
    messageSection.style.background = "red";

    const messageTextSection = document.getElementById("message-section-text");

    messageTextSection.innerText = messageText;
}

hideMessage = function() {
    document.getElementById("message-section-text").innerText = "";

    document.getElementById("message-section").style.display = "none";
}