document.addEventListener('DOMContentLoaded', () => {
    const weatherTableBody = document.querySelector('#weatherTable tbody');
    const loadingMessage = document.getElementById('loading');
    const errorMessage = document.getElementById('error');
    const noDataMessage = document.getElementById('noDataMessage');
    const refreshButton = document.getElementById('refreshButton');

    const API_URL = "http://75.217.196.248:7070/get_weather_logs"

    async function fetchWeatherData() {
        weatherTableBody.innerHTML = '';
        loadingMessage.classList.remove('hidden');
        errorMessage.classList.add('hidden');
        noDataMessage.classList.add('hidden');

        try {
            const response = await fetch(API_URL);

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const data = await response.json();

            if (data.length === 0) {
                noDataMessage.classList.remove('hidden');
                return;
            }

            data.forEach(log => {
                const row = weatherTableBody.insertRow();
                row.insertCell().textContent = log.id;
                row.insertCell().textContent = log.log_date;
                row.insertCell().textContent = log.weather_condition;
                row.insertCell().textContent = log.temperature;
                row.insertCell().textContent = log.wind_speed;
            });

        } catch (error) {
            console.error("Error fetching weather data:", error);
            errorMessage.textContent = `Failed to load weather data: ${error.message}. Please check the server.`;
            errorMessage.classList.remove('hidden');
            weatherTableBody.innerHTML = '<tr><td colspan="5">Error loading data.</td></tr>';
        } finally {
            loadingMessage.classList.add('hidden');
        }
    }

    fetchWeatherData();

    refreshButton.addEventListener('click', fetchWeatherData);
});