import json
import smtplib
import time
from datetime import date
from email.mime.text import MIMEText
import cloudscraper


#These variables must be set before running
##################################################
sender_address = 'sample_sender⚠@gmail.com'
sender_pass = 'samplepassword'
receiver_address = ['sample_receiver⚠@gmail.com',\
                    'sample_receiver2⚠@gmail.com']  # multiple emails can be added (seperated by commas)
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)   # change if not using gmail smpt 
pin_code = "100001"                                 # pincode of your area
###################################################


scraper = cloudscraper.create_scraper()
par_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?"
selected_date = date.today().strftime("%d-%m-%Y")
userdata = {"data": []}
name_added = False
tmp_body = ''


def pause(x):
    time.sleep(x)
    main()


def sendmail(body):
    global tmp_body

    if tmp_body == body:
        pause(60)
    else:
        print(body)
        msg = MIMEText(body)
        msg['From'] = sender_address
        msg['To'] = "You"
        msg['Subject'] = 'Vaccine slot alert'
        smtp_ssn = smtp_server
        smtp_ssn.starttls()
        smtp_ssn.login(sender_address, sender_pass)
        smtp_ssn.send_message(msg, sender_address, receiver_address)
        smtp_ssn.quit()
        tmp_body = body
        print('Mail Sent')
    pause(60)


def main():
    message = []
    uri = par_url + "pincode=" + pin_code + "&date=" + selected_date
    data = json.loads(scraper.get(uri).text)
    center_count = len(data['centers'])
    tmp = 0
    global tmp_body
    global name_added
    while tmp < center_count:
        for count in data['centers']:
            name_added = False
            for session in data['centers'][tmp]['sessions']:
                if session['min_age_limit'] == 18 and session['available_capacity_dose1'] > 0:
                    if not name_added:
                        message.append(count['name'] + ', Available slots:\n')
                        name_added = True
                    message.append(str(session['available_capacity_dose1']) + ' ')
                    message.append(session['vaccine'] + ' ')
                    message.append('For: ' + session['date']+'\n')
            tmp += 1
        sendmail(''.join(message))


main()