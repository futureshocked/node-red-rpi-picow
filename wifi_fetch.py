import network
import time
import usocket
import ussl
import ujson

# Initialize WiFi
wifi     = network.WLAN(network.STA_IF)
wifi.active(True)

# Set your WiFi credentials
SSID     = '<--WIFI-NETWORK-NAME-->'
PASSWORD = '<--WIFI-PASSWORD-->'

# Connect to WiFi
wifi.connect(SSID, PASSWORD)

# Wait for connection
while not wifi.isconnected():
    time.sleep(1)

print("Successfully connected to WiFi!")

# Fetch weather data from OpenWeather API over HTTPS
addr_info = usocket.getaddrinfo("api.openweathermap.org", 443)
addr      = addr_info[0][-1]

s         = usocket.socket()
s.connect(addr)

# Wrap socket with SSL
s         = ussl.wrap_socket(s)

# Construct and send the HTTPS GET request
api_key   = "<--YOUR-API-KEY-->"
city      = "<--YOUR-CITY-->"
request   = "GET /data/2.5/weather?q={}&appid={}&units=metric HTTP/1.1\r\nHost: api.openweathermap.org\r\n\r\n".format(city, api_key)
print("Getting weather information...")
s.write(request.encode('utf-8'))

# Receive and decode the response
response  = b""
print("Got data")
while True:
    data = s.read(1000)
    if data:
        response += data
    else:
        break

# Extract temperature from JSON response
response_str = str(response, 'utf-8')
start_idx    = response_str.find('{"temp":') + 8
end_idx      = response_str.find(',"feels_like"')
temperature  = response_str[start_idx:end_idx]

print(f"The current temperature in {city} is {temperature}°C.")
