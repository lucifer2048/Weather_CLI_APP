import mysql.connector
import bcrypt
import requests
from datetime import datetime
from collections import defaultdict


# Database connection with error handling
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Change to your MySQL server address if different
            user="sss_assignment_sep24",
            password="doitnow",
            database="weather_cli"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Hash password for storage
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify password
def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# User registration with error handling
def register_user():
    connection = connect_to_db()
    if connection is None:
        return
    cursor = connection.cursor()
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    hashed_pw = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        connection.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Update user profile (username or password)
def update_user_profile(user_id):
    connection = connect_to_db()
    if connection is None:
        return
    cursor = connection.cursor()
    print("\n1. Update Username\n2. Update Password")
    choice = input("Select an option: ")

    if choice == '1':
        new_username = input("Enter new username: ")
        try:
            cursor.execute("UPDATE users SET username = %s WHERE id = %s", (new_username, user_id))
            connection.commit()
            print("Username updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    elif choice == '2':
        new_password = input("Enter new password: ")
        hashed_pw = hash_password(new_password)
        try:
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_pw, user_id))
            connection.commit()
            print("Password updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    else:
        print("Invalid option.")
    
    cursor.close()
    connection.close()

# User login with error handling
def login_user():
    connection = connect_to_db()
    if connection is None:
        return None
    cursor = connection.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        stored_hashed_pw = result[1].encode('utf-8')  # Convert to bytes
        if check_password(stored_hashed_pw, password):
            print("Login successful!")
            cursor.close()
            connection.close()
            return result[0]  # Return user ID
        else:
            print("Login failed! Invalid credentials.")
    else:
        print("User not found.")
    
    cursor.close()
    connection.close()
    return None

# Get weather data from OpenWeatherMap API with error handling (current weather)
def get_weather(location, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }
            return weather_info
        elif response.status_code == 404:
            print(f"Location '{location}' not found. Please try again.")
        elif response.status_code == 429:
            print("API rate limit exceeded. Please wait and try again later.")
        else:
            print(f"Error fetching weather data. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"API connection error: {e}")
    
    return None

# Get 5-day weather forecast from OpenWeatherMap API
def get_forecast(location, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"\n--- 5-Day Weather Forecast for {location.capitalize()} ---\n")
            
            # Group forecasts by date
            forecasts_by_date = defaultdict(list)
            for forecast in data['list']:
                date = datetime.utcfromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
                time = datetime.utcfromtimestamp(forecast['dt']).strftime('%H:%M')
                temp = forecast['main']['temp']
                desc = forecast['weather'][0]['description']
                wind_speed = forecast['wind']['speed']
                
                forecasts_by_date[date].append({
                    'time': time,
                    'temp': temp,
                    'desc': desc.capitalize(),
                    'wind_speed': wind_speed
                })
            
            # Display the forecast
            for date, forecasts in forecasts_by_date.items():
                print(f"\n=== {date} ===")
                for forecast in forecasts:
                    print(f"Time: {forecast['time']}, Temp: {forecast['temp']}°C, Condition: {forecast['desc']}, Wind Speed: {forecast['wind_speed']} m/s")
                print("-" * 40)  # Divider between days
            
        elif response.status_code == 404:
            print(f"Location '{location}' not found. Please try again.")
        elif response.status_code == 429:
            print("API rate limit exceeded. Please wait and try again later.")
        else:
            print(f"Error fetching weather data. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"API connection error: {e}")

    return None

# Save search history to the database with error handling
def save_search_history(user_id, location, weather_data):
    connection = connect_to_db()
    if connection is None:
        return
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO search_history (user_id, location, weather_data) VALUES (%s, %s, %s)",
            (user_id, location, str(weather_data))
        )
        connection.commit()
        print("Search history saved.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# View search history with error handling
def view_search_history(user_id):
    connection = connect_to_db()
    if connection is None:
        return
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id, location, weather_data, search_time FROM search_history WHERE user_id = %s", (user_id,))
        history = cursor.fetchall()

        if history:
            print("\nYour Search History:")
            for entry in history:
                print(f"ID: {entry[0]}, Location: {entry[1]}, Weather: {entry[2]}, Searched at: {entry[3]}")
        else:
            print("No search history found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Delete specific entry from search history with confirmation and go back option
def delete_search_history(user_id):
    connection = connect_to_db()
    if connection is None:
        return
    cursor = connection.cursor()

    try:
        # Display user's search history before deletion
        cursor.execute("SELECT id, location, search_time FROM search_history WHERE user_id = %s", (user_id,))
        history = cursor.fetchall()

        if not history:
            print("No search history found.")
            return

        print("\nYour Search History:")
        for entry in history:
            print(f"ID: {entry[0]}, Location: {entry[1]}, Searched at: {entry[2]}")

        # Provide an option to go back
        print("\nEnter the ID of the search entry to delete or type 'b' to go back:")
        entry_id = input("Delete Entry ID: ")

        if entry_id.lower() == 'b':
            print("Going back to the previous menu.")
            return

        # Validate if the entered ID is numeric
        if not entry_id.isdigit():
            print("Invalid ID. Please enter a numeric value.")
            return

        # Confirm before deleting
        confirm = input(f"Are you sure you want to delete entry ID {entry_id}? (y/n): ").lower()
        if confirm != 'y':
            print("Deletion cancelled. Going back to the previous menu.")
            return

        # Proceed to delete
        cursor.execute("DELETE FROM search_history WHERE id = %s AND user_id = %s", (entry_id, user_id))
        connection.commit()

        if cursor.rowcount > 0:
            print("Search entry deleted successfully.")
        else:
            print("No matching entry found for the provided ID.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# CLI interface for user actions
def main():
    API_KEY = "e3190c35cd148de695f94471866e5af6"  # Replace with your OpenWeatherMap API key

    print("Welcome to the Weather CLI Application!")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Quit")
        choice = input("Select an option: ")

        if choice == '1':
            register_user()
        elif choice == '2':
            user_id = login_user()
            if user_id:
                while True:
                    print("\n1. Search Weather")
                    print("2. View Search History")
                    print("3. Delete Search History")
                    print("4. Update Profile")
                    print("5. 5-day Weather Forecast")
                    print("6. Logout")
                    user_choice = input("Select an option: ")

                    if user_choice == '1':
                        location = input("Enter the city name: ")
                        weather_data = get_weather(location, API_KEY)
                        if weather_data:
                            print(f"\nWeather in {location}:")
                            print(f"Temperature: {weather_data['temperature']}°C")
                            print(f"Humidity: {weather_data['humidity']}%")
                            print(f"Condition: {weather_data['weather']}")
                            print(f"Wind Speed: {weather_data['wind_speed']} m/s")
                            save_search_history(user_id, location, weather_data)

                    elif user_choice == '2':
                        view_search_history(user_id)

                    elif user_choice == '3':
                        delete_search_history(user_id)

                    elif user_choice == '4':
                        update_user_profile(user_id)

                    elif user_choice == '5':
                        location = input("Enter the city name for the 5-day forecast: ")
                        get_forecast(location, API_KEY)

                    elif user_choice == '6':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Try again.")
        elif choice == '3':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
