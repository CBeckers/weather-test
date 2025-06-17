import requests
import json
from datetime import datetime

# Define the endpoint URL
API_URL = "http://75.217.196.248:7070/add_weather_log"

def send_weather_data(weather_condition, temperature, wind_speed, log_date=None):
    """
    Sends weather data to the Flask API endpoint.

    Args:
        weather_condition (str): Description of the weather (e.g., "Sunny", "Rainy").
        temperature (float): Temperature in Celsius or Fahrenheit.
        wind_speed (float): Wind speed.
    """

    # list of data to ping the endpoint
    payload = {
        "weather_condition": weather_condition,
        "temperature": temperature,
        "wind_speed": wind_speed
    }

    # boilerplate stuff for sending a ping to and endpoint 
    headers = {'Content-Type': 'application/json'}

    # try this code and check for errors
    try:
        # send the ping
        response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
        # API_URL -> ip of the server 
        # data -> data being sent to the server
        # headers -> boilerplate headers for sending a ping
        response.raise_for_status()  # raise an HTTP error for bad responses (4xx or 5xx)

        # print the status of the ping (error or confirmation)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

    # errors caught here
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}. Is the server running at {API_URL}?")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON response: {json_err} - Response text: {response.text}")





if __name__ == "__main__":
    # Send data with current time (server generates log_date) ---
    print("--- Sending Weather Data (Current Time) ---")
    send_weather_data(
        weather_condition="Partly Cloudy",
        temperature=90,
        wind_speed=15
    )
    print("\n" + "="*50 + "\n")