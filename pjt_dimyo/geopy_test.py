import geopy.geocoders
from geopy.geocoders import GoogleV3
import certifi
import ssl

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

with open('google_develop.key', 'r') as file:
    api_key = file.read().strip()

geocoder = GoogleV3(api_key=api_key)
coord = geocoder.geocode('전북 전주시 덕진구 정여립로 1115, 415호 414호, 415호')

print(f'{coord.latitude}, {coord.longitude}')