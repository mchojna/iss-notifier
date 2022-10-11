import time

import requests
import datetime as dt
import smtplib
import time

current_lat = 52.967969
current_lng = 18.723041
current_time = str(dt.datetime.now()).split(" ")[1]

my_email = input("Please, enter your e-mail: ")
my_password = input("Please, enter your password: ")

iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_data = iss_response.json()

parameters = {
    "lat": current_lat,
    "lng": current_lng,
    "formatted": 0,
}

sunset_sunrise_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters, verify=False)
sunset_sunrise_data = sunset_sunrise_response.json()["results"]

iss_lat = float(iss_data["iss_position"]["latitude"])
iss_lng = float(iss_data["iss_position"]["longitude"])

sunrise_time = sunset_sunrise_data["sunrise"].split("T")[1].split("+")[0]
sunset_time = sunset_sunrise_data["sunset"].split("T")[1].split("+")[0]

check = False

if current_lat - 0.5 <= iss_lat <= current_lat + 0.5 and current_lng - 0.5 <= iss_lng <= current_lng + 0.5:
    check = True
    print("Currently ISS is close to your localization!")
else:
    print("Currently ISS is too far from your localization!")

if sunrise_time > current_time > sunset_time:
    print("Currently is enough dark in your localization!")
else:
    check = False
    print("Currently is not enough dark in your localization!")

while check:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        print("Sending notification...")
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg="Subject:ISS\n\nCurrently ISS is in your location. Look up!")
        print("Notification sent!")
        time.sleep(60)


