import json
import re
import smtplib
import os
import requests
import pandas as pd
import logging.config
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
import birthday_variables as bv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

THIS_FOLDER = Path(__file__).parent.resolve()
CONTACTS_FILE = THIS_FOLDER / 'contacts.csv'
LOGGING_CONF_FILE = THIS_FOLDER / 'logging_conf.json'

with open(LOGGING_CONF_FILE) as conf_file:
    dict_conf = json.load(conf_file)

logging.config.dictConfig(dict_conf)
logger = logging.getLogger(__name__)


class Birthday:

    def __init__(self, source: str = 'openai') -> None:
        """
        Initializes the class.
        :param source: either 'openai' or 'ninja'
        """
        self.gmail_user = os.environ.get('USER')
        self.gmail_password = os.environ.get('PASSWORD')
        self.source = source
        if source == 'openai':
            self.api_key = os.environ.get('OPENAI_KEY')
        else:
            self.api_key = os.environ.get('NINJA_API_KEY')
        self.random_text = ''
        self.recipients = {}

    def get_openai_random(self) -> None:
        """
        Gets a text from OpenAI ChatGPT for the birthday wish
        :return: None
        """
        openai.api_key = self.api_key
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=bv.prompt,
            temperature=0.6,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
        )
        openai_text = response['choices'][0]['text'].replace('[YOUR NAME]', '')
        self.random_text = openai_text.lstrip().replace('\n\n', '<br /><br />').replace('\n', '<br />')

    def get_ninja_random(self, what: str) -> None:
        """
        Gets random texts from the Ninja API.
        :param what: a string for the type of text to get from Ninja
        :return: None
        """
        if what == 'quotes':
            api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format('love')
        else:
            api_url = f'https://api.api-ninjas.com/v1/{what}'
        response = requests.get(api_url, headers={'X-Api-Key': self.api_key})
        if response.status_code == requests.codes.ok:
            if what == 'quotes':
                res = json.loads(response.text)
                self.random_text = f"{res[0]['quote']}\nby {res[0]['author']}"
            elif what == 'riddles':
                res = json.loads(response.text)
                self.random_text = f"{res[0]['title']}\nQ: {res[0]['question']}\nA: {res[0]['answer']}"
            else:
                mapping = {'dadjokes': 'joke', 'jokes': 'joke', 'facts': 'fact'}
                self.random_text = json.loads(response.text)[0][mapping[what]].strip()
        else:
            logger.error(f'Ninja API problem: {response.status_code} {response.text}')
            self.random_text = f'No {what} for now'

    def get_recipients(self, contacts_filepath: Path) -> None:
        """
        Check the contacts.csv file and fetch who has their birthday today.
        :param contacts_filepath: the filepath to the csv.
        :return: None
        """
        df = pd.read_csv(contacts_filepath)
        today = date.today()
        df = df[['Given Name', 'Family Name', 'Birthday', 'E-mail 1 - Value']]
        for index, row in df.iterrows():
            (_, month, day) = row['Birthday'].strip().replace('--', 'None-').split('-')
            if today.strftime('%m-%d') == f'{month}-{day}':
                self.recipients[index] = {
                    'full_name': f"{row['Given Name']} {row['Family Name']}",
                    'name': row['Given Name'],
                    'email': row['E-mail 1 - Value']
                }

    def send_email(self, html_email: str, recipient_email: str, subject_email: str) -> None:
        """
        Send the email to the birthday person(s)
        :param html_email: The html of the letter
        :param recipient_email: The recipient in the form Name Lastname <email>
        :param subject_email: The subject of the email
        :return: None
        """
        msg = MIMEMultipart('alternative')
        from_email = f'Dani Oshi <{self.gmail_user}>'

        msg['From'] = from_email
        msg['To'] = recipient_email
        msg['Bcc'] = os.environ.get('BCC_USER')
        msg['Subject'] = subject_email
        msg.add_header('Content-Type', 'text/html')

        body = re.sub(re.compile('<.*?>'), '', html_email).replace('&nbsp;', '').strip()
        body = '\n'.join([line.strip() for line in body.split('\n')])
        msg.attach(MIMEText(body, 'plain'))
        msg.attach(MIMEText(html_email, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(self.gmail_user, recipient_email, msg.as_string())
            logger.info(f'Email sent to {recipient_email}')


if __name__ == '__main__':
    birthday = Birthday('openai')
    birthday.get_recipients(CONTACTS_FILE)
    if not birthday.recipients:
        logger.info('Nobody has a birthday today!')
    else:
        for _, person in birthday.recipients.items():
            recipient = f"{person['full_name']} <{person['email']}>"
            subject = f"Happy birthday {person['name']}!"
            html = ''
            if birthday.source == 'openai':
                birthday.get_openai_random()
                html = bv.html_openai.replace('[OPENAI_TEXT]', birthday.random_text)
            elif birthday.source == 'ninja':
                birthday.get_ninja_random('dadjokes')
                html = bv.html_ninja.replace('[DAD_JOKE]', birthday.random_text)
                birthday.get_ninja_random('jokes')
                html = html.replace('[JOKE]', birthday.random_text)
                birthday.get_ninja_random('facts')
                html = html.replace('[FACT]', birthday.random_text)
                birthday.get_ninja_random('quotes')
                html = html.replace('[QUOTE]', birthday.random_text)
            html = html.replace('[NAME]', person['name'])
            birthday.send_email(html, recipient, subject)
