







# if you dont have pip installed install that first, then run this
# pip install Flask mysql-connector-python flask-cors









from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
from flask_cors import CORS


# create an instance of the app with the cors middleware
app = Flask(__name__)#
CORS(app)

# database configuration
DB_CONFIG = {
    'host': '', #your home ipv4 (example 90.100.110.120)
    'user': '',  # database username
    'password': '',  # database password
    'database': ''  # database name
}

def get_db_connection():
    # establishes a connection to the MySQL database.
    return mysql.connector.connect(**DB_CONFIG)

# create the endpoint that your weather station can ping and send data to the main server
# endpoint is called "add_weather_log"
@app.route('/add_weather_log', methods=['POST']) # POST is the type of request made to the server
def add_weather_log():
    """
    API endpoint to add a new weather log.
    Expects JSON data: {
        "weather_condition": "string",
        "temperature": float,
        "wind_speed": float
    }
    """
    data = request.get_json()

    # no data provided
    if not data:
        return jsonify({'error': 'No data provided'}), 400 # 400 is error code given

    log_date = datetime.now() # grabs the current time

    # get each individual field and set them as variables
    weather_condition = data.get('weather_condition')
    temperature = data.get('temperature')
    wind_speed = data.get('wind_speed')

    # check for missing data
    if weather_condition is None or temperature is None or wind_speed is None:
        return jsonify({'error': 'Missing required fields: weather_condition, temperature, wind_speed'}), 400 # 400 is error code given

    # try this code and be ready to catch errors that arrise
    try:
        conn = get_db_connection() # connect to database
        cursor = conn.cursor() # from the connection grab a cursor connection (a way to execute database commands)

        # build the statement to insert the data to the database
        insert_query = """
        INSERT INTO weather_logs (log_date, weather_condition, temperature, wind_speed)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (log_date, weather_condition, temperature, wind_speed)) # execute the command
        conn.commit() # commit the changes to make the persist

        # when use use the cursor.execute changes happen but they are not permanent unless you commit them

        log_id = cursor.lastrowid # if you want to grab the new entry

        # close db connections
        cursor.close()
        conn.close()

        # return a JSON message saying that the data was added successfully
        return jsonify({'message': 'Weather log added successfully', 'id': log_id}), 201

    # start errors
    except mysql.connector.Error as err:
        return jsonify({'error': f"Database error: {err}"}), 500 # 500 error code, error for issues with the db
    except ValueError as err:
        return jsonify({'error': f"Invalid date format: {err}. Expected YYYY-MM-DD HH:MM:SS"}), 400 # 400 error code, invalid date format
    except Exception as e: 
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500 # 500 error code, other error catcher
    
# retrieve all weather logs
@app.route('/get_weather_logs', methods=['GET'])
def get_weather_logs():
    """
    API endpoint to fetch all weather logs.
    """
    try:
        # connect to database
        conn = get_db_connection() # connect to database

        # from the connection grab a cursor connection (a way to execute database commands)
        cursor = conn.cursor(dictionary=True) # Use dictionary=True to get rows as dictionaries

        # build the statement to insert the data to the database
        select_query = "SELECT id, log_date, weather_condition, temperature, wind_speed FROM weather_logs ORDER BY log_date DESC"
        cursor.execute(select_query) # execute the command
        records = cursor.fetchall() # get the records as a local variable from the command just executed

        # convert datetime to string for JSON conversion
        for record in records:
            if isinstance(record['log_date'], datetime):
                record['log_date'] = record['log_date'].strftime('%Y-%m-%d %H:%M:%S')

        # close connections
        cursor.close()
        conn.close()

        # return the requested data
        return jsonify(records), 200

    # errors here
    except mysql.connector.Error as err:
        return jsonify({'error': f"Database error: {err}"}), 500
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    # change host to your local ip for the server and change port for the port you opened on your network
    app.run(host='', debug=True, port=) # run the app and scan for pings on network port 7070