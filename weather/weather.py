import argparse
import pyfiglet
from simple_chalk import chalk
import requests
from azure.storage.blob import BlobServiceClient


# Api key for
API_KEY='0ada6884f38cdc6a61b2ef1d69cea80e'

# base url for openweather api
BASE_URL='https://api.openweathermap.org/data/2.5/weather'

# map weather codes to weather icons
WEATHER_ICONS = {
    "01d": "☀️",  # Clear sky (day)
    "01n": "🌙",  # Clear sky (night)
    "02d": "⛅️",  # Few clouds (day)
    "02n": "☁️🌙",  # Few clouds (night)
    "03d": "☁️",  # Scattered clouds
    "03n": "☁️🌙",  # Scattered clouds (night)
    "04d": "☁️☁️",  # Broken clouds
    "04n": "☁️☁️🌙",  # Broken clouds (night)
    "09d": "🌧️",  # Shower rain
    "09n": "🌧️🌙",  # Shower rain (night)
    "10d": "🌦️",  # Rain
    "10n": "🌧️🌙",  # Rain (night)
    "11d": "⛈️",  # Thunderstorm
    "11n": "⛈️🌙",  # Thunderstorm (night)
    "13d": "❄️",  # Snow
    "13n": "❄️🌙",  # Snow (night)
    "50d": "🌫️",  # Mist
    "50n": "🌫️🌙",  # Mist (night)
}


# construct api url 
parser=argparse.ArgumentParser(description='Check the waether for certain location')
# parser.add_argument('country',help='The country/city to check the weather for')
parser.add_argument('country', help='The country/city to check the weather for')
args=parser.parse_args()
url=f'{BASE_URL}?q={args.country}&appid={API_KEY}&units=metric'

# make api request and parse response
response=requests.get(url)
if response.status_code !=200:
    print(chalk.red('Error:Unable to retrive information'))
    exit()
# parsing json response from api
data=response.json()

temperature=data['main']['temp']
feels_like=data['main']['feels_like']
description=data['weather'][0]['description']
icon=data['weather'][0]['icon']
city=data['name']
country=data['sys']['country']


# construct output with icons
weather_icon=WEATHER_ICONS.get(icon,'')
output=f"{pyfiglet.figlet_format(city)},{country}"
output+=f'{weather_icon}{description}\n'
output+=f'{temperature:{temperature}}^C\n'
output+=f'{feels_like:{feels_like}}^C\n'


# print output
print(chalk.green(output))

# Replace <connection_string> with your Azure Blob Storage connection string
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=acblob;AccountKey=zCWSkShrLIHTpQ+Y2Qqdwi63+guqT0wbjtuddI5d+zLiNN/vtXRyiTn1oT7hCvVFcS4i5aRAoUyy+AStpUcS4Q==;EndpointSuffix=core.windows.net")

# Replace <container_name> with the name of your container
container_name = "weatherapp"


def upload_to_blob_storage(data):
    # Replace <blob_name> with the desired name for your blob file
    blob_name = "ablob.txt"
    
    data_bytes = data.encode("utf-8")

    # Get a reference to the container
    container_client = blob_service_client.get_container_client('weatherapp')

    # Upload the data to the container
    container_client.upload_blob(name='ablob', data=data_bytes)

upload_to_blob_storage(output)


