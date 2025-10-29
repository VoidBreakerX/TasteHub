function submitFeedback() {
    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let rating = document.getElementById("rating").value;
    let message = document.getElementById("message").value.trim();
    let response = document.getElementById("responseMsg");

    // Basic validation
    if (name === "" || email === "" || rating === "" || message === "") {
        response.innerHTML = "All fields are required";
        response.style.color = "red";
        return;
    }

    // Email format check
    let emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
    if (!email.match(emailPattern)) {
        response.innerHTML = "Please enter a valid email address";
        response.style.color = "red";
        return;
    }

    // Submit success
    response.innerHTML = "Thank you for your valuable feedback";
    response.style.color = "green";

    // Clear form after successful submission
    document.getElementById("feedbackForm").reset();
}
