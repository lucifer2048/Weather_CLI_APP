# Weather CLI Application

## Overview
A Python-based command-line interface (CLI) application that interacts with the OpenWeatherMap API to fetch real-time weather data and manage user search history using MySQL. The app allows users to register, log in, search for current weather and a 5-day forecast, and manage their search history.

## Features
- **User Registration & Login**: Users can create accounts, log in securely using hashed passwords, and manage profiles.
- **Weather Search**: Search for current weather conditions (temperature, humidity, weather description, wind speed) for any city.
- **5-Day Forecast**: Retrieve and display a detailed 5-day forecast for any city.
- **Search History Management**: View, delete, and store weather search history linked to each user.
- **Profile Management**: Users can update their username and password.

## Technologies Used
- **Python**: Core programming language for the CLI app.
- **MySQL**: For persistent data storage (user information and search history).
- **OpenWeatherMap API**: To fetch real-time weather and forecast data.
- **bcrypt**: For securely hashing passwords.

## Prerequisites
- Python 3.x installed
- MySQL installed and running
- OpenWeatherMap API key (register at [OpenWeatherMap](https://openweathermap.org/))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather-cli-app.git
   cd weather-cli-app
