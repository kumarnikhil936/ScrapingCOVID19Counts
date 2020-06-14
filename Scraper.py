import smtplib
from datetime import datetime

import requests
from bs4 import BeautifulSoup

header = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}


def fetch_numbers():
    webpage = 'https://www.mygov.in/covid-19'
    # Fetch page contents
    r = requests.get(webpage)
    page_text = r.text
    soup = BeautifulSoup(page_text, 'html.parser')
    # Find required divs and spans
    divs = soup.find_all('div', attrs={'class': 'info_label'})
    spans = soup.find_all('span', attrs={'class': 'icount'})
    return divs, spans


def send_email():
    google_email = 'kumar.nikhil936@gmail.com'
    # google_email_2 = 'nikhilkumarjha94@gmail.com'
    gmail_smtp = 'smtp.gmail.com'
    gmail_port = 587

    # Create your own app password for the gmail account from 2-step authentication
    google_app_password = 'wsdxfsmcglvujoou'

    # SMTP is Simple Mail Transfer Protocol
    server = smtplib.SMTP(gmail_smtp, gmail_port)
    # EHLO is Extended SMTP command sent by email server to identify itself, when connecting with another email server
    server.ehlo()

    # Excrypt the connection
    server.starttls()
    server.ehlo()

    # Login
    server.login(google_email, google_app_password)

    today_date = datetime.date(datetime.now())
    divs, spans = fetch_numbers()

    # Draft the message to be sent
    subject = f"Daily update on the count of COVID cases in India :: {today_date}"
    body = f'{divs[0].text}: {spans[0].text} \n\n{divs[1].text}: {spans[1].text} \n\n{divs[2].text}: {spans[2].text} \n\n{divs[3].text}: {spans[3].text} \n\n'
    msg = f"Subject: {subject}\n\n\n{body}"
    print(msg)

    # Send the mail
    server.sendmail(google_email, google_email_2, msg)
    print("Sent email from {} to {}".format(google_email, google_email_2))

    # Quit server
    server.quit()


if __name__ == '__main__':
    send_email()
