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