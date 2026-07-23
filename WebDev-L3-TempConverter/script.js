document.getElementById('convertBtn').addEventListener('click', function () {
    const rawInput = document.getElementById('tempInput').value.trim();
    const unit = document.getElementById('unitSelect').value;
    const errorMsg = document.getElementById('errorMsg');
    const resultsArea = document.getElementById('resultsArea');

    // Reset previous states
    errorMsg.classList.add('hidden');
    resultsArea.classList.add('hidden');

    // 1. Validation: Check if input is empty or non-numeric
    if (rawInput === "" || isNaN(rawInput)) {
        errorMsg.textContent = "Error: Please enter a valid numeric temperature value.";
        errorMsg.classList.remove('hidden');
        return;
    }

    const val = parseFloat(rawInput);
    let celsius, fahrenheit, kelvin;

    // 2. Conversion Calculations & Absolute Zero Checks
    if (unit === 'C') {
        if (val < -273.15) {
            errorMsg.textContent = "Error: Temperature cannot fall below Absolute Zero (-273.15°C).";
            errorMsg.classList.remove('hidden');
            return;
        }
        celsius = val;
        fahrenheit = (val * 9/5) + 32;
        kelvin = val + 273.15;
    } else if (unit === 'F') {
        if (val < -459.67) { // Absolute zero in Fahrenheit
            errorMsg.textContent = "Error: Temperature cannot fall below Absolute Zero (-459.67°F).";
            errorMsg.classList.remove('hidden');
            return;
        }
        celsius = (val - 32) * 5/9;
        fahrenheit = val;
        kelvin = celsius + 273.15;
    } else if (unit === 'K') {
        if (val < 0) { // Absolute zero in Kelvin
            errorMsg.textContent = "Error: Kelvin temperature cannot be negative.";
            errorMsg.classList.remove('hidden');
            return;
        }
        kelvin = val;
        celsius = val - 273.15;
        fahrenheit = (celsius * 9/5) + 32;
    }

    // 3. Display simultaneous outputs
    document.getElementById('celsiusResult').textContent = `Celsius: ${celsius.toFixed(2)} °C`;
    document.getElementById('fahrenheitResult').textContent = `Fahrenheit: ${fahrenheit.toFixed(2)} °F`;
    document.getElementById('kelvinResult').textContent = `Kelvin: ${kelvin.toFixed(2)} K`;

    resultsArea.classList.remove('hidden');
});
