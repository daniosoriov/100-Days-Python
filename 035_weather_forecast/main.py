import requests
import os
import datetime
import smtplib
import logging
import logging.handlers
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# The package name is python-dotenv
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('weather-log')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler('weather-emails.log', maxBytes=5 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_weather_data() -> dict:
    """
    Get the weather data from Open Weather Map
    :return: a dictionary with the response
    """
    params = {
        'lat': os.environ['MY_LAT'],
        'lon': os.environ['MY_LNG'],
        'exclude': 'minutely,hourly,daily',
        'units': 'metric',
        'appid': os.environ['OPEN_WEATHER_MAP_API_KEY'],
    }
    response = requests.get('https://api.openweathermap.org/data/3.0/onecall', params=params)
    response.raise_for_status()
    return response.json()


def from_unix_time(unix_timestamp: float, time_format='%Y-%m-%d %H:%M:%S') -> str:
    """
    Formats a unix timestamp and returns a string with time_format format
    :param unix_timestamp: the unix timestamp
    :param time_format: the desired format for the output
    :return: the string with the date
    """
    datetime_obj = datetime.datetime.fromtimestamp(unix_timestamp)
    return datetime_obj.strftime(time_format)


def format_data(data: dict, hourly=False) -> list:
    """
    Formats the data from the API to a readable set of lines of text
    :param data: the dictionary with the data
    :param hourly: True if checking the hourly data, False otherwise
    :return: a list with messages with the formatted data
    """
    messages = []
    if not hourly:
        messages.append(f"Current time: {from_unix_time(data['dt'])}")
        messages.append(f"Sunrise: {from_unix_time(data['sunrise'], '%H:%M')}")
        messages.append(f"Sunset: {from_unix_time(data['sunset'], '%H:%M')}")
    else:
        messages.append('')
        messages.append(from_unix_time(data['dt']))
    messages.append(f"Temperature: {data['temp']}°C feels like {data['feels_like']}°C")
    messages.append(f"Clouds: {data['clouds']}%")
    messages.append(f"Precipitation: {round(data.get('pop', 0) * 100)}%")
    for weather in data['weather']:
        messages.append(f"Weather: {weather['main']} / {weather['description']}")
    return messages


def send_email(message: list) -> None:
    """
    Sends an email message
    :param message: The lines of the message
    :return: None
    """
    sender_email = os.environ['SENDER_EMAIL']
    receiver_email = os.environ['RECIPIENT_EMAIL']
    password = os.environ['SENDER_PASSWORD']
    today = datetime.datetime.today()
    today_formatted = today.strftime("%A, %B %d")
    subject = f"Alert on weather today, {today_formatted}"
    message = '\n'.join(message)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        logger.info(f'Alerts found! Email sent to {receiver_email}')


def main() -> None:
    """
    The main functionality, calling the API, formatting the data, and sending emails in case of alert.
    :return: None
    """
    weather_data = get_weather_data()
    lines = []
    lines += format_data(weather_data['current'])

    if 'hourly' in weather_data:
        for hour in weather_data['hourly'][:13]:
            lines += format_data(hour, True)

    for event in weather_data.get('alerts', []):
        lines.append('')
        lines.append('Alert message')
        lines.append(event['event'])
        lines.append(f"From {from_unix_time(event['start'])} until {from_unix_time(event['end'])}")
        lines.append(event['description'])

    if 'alerts' in weather_data:
        send_email(lines)
    else:
        logger.info('No alerts, no email sent.')


if __name__ == '__main__':
    main()
