#Weather CLI Application (README)

##Overview
This Python-based command-line application allows users to:
- Register and log in with credentials.
- Search for the current weather and 5-day weather forecast for any location using the OpenWeatherMap API.
- Store weather search history in a MySQL database.
- View, delete, and manage the search history.
- Update user profiles (username or password).

##Features
1.   User Authentication  
   - Register a new account with a username and password (hashed using bcrypt).
   - Log in with your credentials to access weather search and history features.
   
2.   Weather Search  
   - Search for the current weather in any city.
   - Get temperature, humidity, weather condition, and wind speed.
   
3.   5-Day Weather Forecast  
   - View the 5-day forecast for a city with detailed weather for each day.
   
4.   Search History Management  
   - View the history of all weather searches made by a user.
   - Delete individual search entries by ID.

5.   Profile Management  
   - Update your username or password.

##Requirements
1.   Python 3.x  
2.   MySQL Database  
3.   OpenWeatherMap API Key  
4.   Python Libraries   (install using `pip`):
   - `mysql-connector-python`
   - `bcrypt`
   - `requests`

##Setup Instructions
1.   Clone the Source Code  :
  	SSSAssignment.py file

2. Install the dependencies:
	pip install -r requirements.txt

3. Set up MySQL database:
    -  Run the SQL commands below to create the database and tables.

CREATE DATABASE weather_cli;

USE weather_cli;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE search_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    weather_data TEXT NOT NULL,
    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

4. Run the Application:
    python SSSAssignment.py


##API Key Setup
- Register at OpenWeatherMap to obtain an API key.
- Replace "your_openweathermap_api_key" in the main.py with your actual API key.

##Usage
- Register or log in.
- Search for weather by city name.
- View, update, or delete search history.
- Update profile information.
- 5-day forecast.


