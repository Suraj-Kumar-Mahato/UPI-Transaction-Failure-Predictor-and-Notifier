// Function to handle form submission
document.getElementById("transaction-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission (default action)

    // Get input values from the form
    const amount = document.getElementById("amount").value;
    const networkStatus = document.getElementById("network").value;
    const time = document.getElementById("time").value;

    // Basic Validation: Check if all inputs are provided
    if (amount === "" || networkStatus === "" || time === "") {
        alert("Please fill in all the details!");
        return;
    }

    // Create a JSON object with the form data
    const formData = {
        amount: amount,
        network_status: networkStatus,
        time: time
    };

    // Make a POST request to the Flask backend
    fetch('http://127.0.0.1:5000/predict', { // Update the URL if needed
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        // Display prediction result
        document.getElementById("prediction-status").innerHTML = `<p>${data.prediction}</p>`;
        
        // Display alert message
        document.getElementById("alert-box").innerHTML = `<p>${data.alert}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Error communicating with the backend.");
    });
});
