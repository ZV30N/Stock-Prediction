// Range of year visibility
document.addEventListener('DOMContentLoaded', function() {
    const selectYearRadio = document.getElementById('select');
    const noneRadio = document.getElementById('none');
    const yearRangeBox = document.getElementById('yearRangeBox');

    // Listen for changes in the radio buttons    
    selectYearRadio.addEventListener('change', function() {
        if (selectYearRadio.checked) {
            yearRangeBox.style.display = 'block'; // Show the range slider
        }
    });

    noneRadio.addEventListener('change', function() {
        if (noneRadio.checked) {
            yearRangeBox.style.display = 'none'; // Hide the range slider
        }
    });

    if (!selectYearRadio.checked) {
        yearRangeBox.style.display = 'none'; // Ensure it's hidden if "None" is checked on page load
    }
});

// Slider
const inputRange = document.getElementById("yearrange");

inputRange.addEventListener("input", function() {
    const activeColor = "#a5c8e5";
    const inactiveColor = "#cccccc";
    const ratio = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = `linear-gradient(90deg, ${activeColor} ${ratio}%, ${inactiveColor} ${ratio}%)`;

    document.getElementById('value').innerText = this.value;
});

// Stock Ticker Predict
document.getElementById('stockForm').addEventListener("submit", function(event){
    event.preventDefault(); // Prevent default form submission

    const userInput = document.getElementById('ticker').value;
    const selectedRadio = document.querySelector('input[name="yearPredict"]:checked');
    const yearsPredict = selectedRadio && selectedRadio.value === 'SelectYear' 
                     ? document.getElementById('yearrange').value 
                     : 0; // Set to 0 if "None" is selected or no radio button is selected

    fetch('/stock', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stock_ticker: userInput, years_of_prediction: yearsPredict }), // Include years
    })
    .then(response => response.json())
    .then(data => {
        console.log("API Response:", data);
        if (data.message === 'Success') {
            document.getElementById('responseText').innerText = '';
            document.getElementById('stockChart').src = 'data:image/png;base64,' + data.plot_url;
            document.getElementById('stockChart').style.display = 'block';
        } else {
            document.getElementById('responseText').innerText = data.message;
            document.getElementById('stockChart').style.display = 'none';
        }
    })
    .catch(error => {
        document.getElementById('responseText').innerText = 'An error occurred: ' + error;
    });
});