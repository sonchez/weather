import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
import datetime
#majority of code logic

def welcome_message():
    print('''
    Welcome to the Office Closure Program.
    We will now check if any offices are required to close,
    as per policy. Any office that meets the requirements
    will automatically be sent an email to close the office.
    ''')

def yaml_pull(path):
    with open(path, "r") as file:
        info = yaml.load(file)
    return info

##Yaml push to file
def yaml_push(path):
    with open(path, "w") as file:
        yaml.dump(info, file)

#SMTP Method
def closure_email(email_list):
    manager_emails = []
    with open(email_list, mode='r', encoding='utf-16') as each_office_emails:
        for email in each_office_emails:
            print(email)

def send_email(my_email, to_email, office):
    my_subject = "IMPORTANT: Office Closure"
    message = "Good Morning, due to inclement weather conditions, the {} office is closed. Please inform all staff.".format(office)
    final_message = MIMEMultipart()
    final_message['From'] = my_email
    final_message['To'] = to_email
    final_message['Subject'] = my_subject
    final_message.attach(MIMEText(message,))
    
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("chris.test.enmu1@gmail.com", "Bassetbond1988!")
    final_message = final_message.as_string()
    server.sendmail(my_email, to_email, final_message)
    server.quit

def string_creater(city, temp, weather_details):
    return ("The {} office is currently closed due to incelement weather."
       "The temperature is {}\n"
       "The weather is: {} \n".format(city, temp, weather_type))

def weather_record(text):           
    file = open("weather_record", 'w')
    file.write(text)
    file.close

def weather_report_output(city,fehrenheit, weather_type):
    return('''---------------------------------
    current temp in  {} is:
    {} fehrenheit.
    The weather is currently: 
    {}
---------------------------------'''.format(city, fehrenheit, weather_type))
    
# top-level variables for use throughout program.
zipcode_list = [87102, 88101, 87301, 88241, 87701, 88001, 88202, 87004, 87501, 88061, 87571]
closure_list = []
report_text_holder = [] 
time = datetime.datetime.now()
formatted_time = time.strftime("%c")
text = ("Managers are responsible for informing staff."
        "Additionally, A copy of this must be reviewed and approved by the E.D."
        "Due to inclememt weather, on {} the following offices were closed:"
        "Details of weather conditions is included:".format(formatted_time))

#Code decision pathing and method/logic calls begins here.
welcome_message

#loop to run through zipcodess
for zipcode in zipcode_list:

    base_url = "http://api.openweathermap.org/data/2.5/weather?zip=%s,us&APPID=20ff885bfd4ee6c9872889da9cf3acc7&units=imperial" %zipcode

    response = requests.get(base_url)   
    weather_report = response.json()

    main_info = weather_report['main']
    city = weather_report['name']
    fehrenheit = main_info['temp']
    weather_macro = weather_report['weather']
    
    for weather_micro in weather_macro:
        weather_type = weather_micro['main']

    
#simple output of temps and offices
    print(weather_report_output(city, fehrenheit, weather_type))
    text = text + weather_report_output(city, fehrenheit, weather_type)
    if fehrenheit <= 32.00:
        closure_list.append(city)

weather_record(text)

# boolean check for office closure
if(len(closure_list)) != 0:
    ##Output for me to review
    print("The following offices need to be closed")
    for office in closure_list:
        print(office)
        
        #yaml pull and format for email distribution that happens automatically.
        path = "office_managers.yaml"
        office_info = yaml_pull(path)

        office_dictionary = office_info.get("offices")
        for office_location, manager_email in office_dictionary.items():
            if office_location in closure_list:
                send_email("chris.test.enmu1@gmail.com", manager_email, office_location)
                break

print('''Thanks for using the weather closure program.
        all processes are now complete.''')
       
