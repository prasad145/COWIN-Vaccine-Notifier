import requests
import time
import json
from datetime import date, datetime, timedelta
from playsound import playsound
age  = int(input("Enter the age: "))
pincodes = [input("Enter the pincode: ")]

numOfDays = 2 #looking slots for next two days
okFlag = 'y'

print("-----Starting search for covid vaccine slots!-----")

todayDate = datetime.today()
# print(str(todayDate))

dates_list = [todayDate + timedelta(days=i) for i in range(numOfDays)]
formated_dates_list = [i.strftime("%d-%m-%Y") for i in dates_list]

# print(formated_dates_list)
while True:
    counter = 0
    for pincode in pincodes:
        for givenDate in formated_dates_list:
            print("looking slot for date : " + givenDate)
            print("---------------------------------------------------------------------------")
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, givenDate)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 

            result = requests.get(URL, headers=header)
            # print(result)
            if result.ok:
                response_json = result.json()
                # print(response_json)
                if response_json["centers"]:
                    for center in response_json["centers"]:
                        for session in center["sessions"]:
                            if(session["min_age_limit"] <= age and session["available_capacity"] > 0):
                                print("Pincode -> " + pincode)
                                print("\nAvailable on + {}".format(givenDate))
                                print("\t", center["name"])
                                print("\t", center["block_name"])
                                print("\t Price -> ",center["fee_type"])
                                print("\t Availability : ", session["available_capacity"])

                                if session["vaccine"] != '':
                                    print("\t Vaccine type: ", session["vaccine"])
                                counter += 1
            else:
                print("No Response\n")


    if counter == 0:
        print("No Vacination slot available!")
    else:
        playsound('Resources/notify.wav')
        print("---------------------------------------------------------------------------")
        print("search completed!") 

    timeGap = datetime.now() + timedelta(minutes=3)

    while datetime.now() < timeGap:
        time.sleep(1)
