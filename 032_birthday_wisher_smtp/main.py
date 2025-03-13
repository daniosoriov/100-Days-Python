import base64
import json
import os
from typing import Literal

import pandas as pd
import random
import logging.config
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import anthropic
from openai import OpenAI

import birthday_variables as bv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client_openai = OpenAI()
client_anthropic = anthropic.Anthropic()

USER_EMAIL = os.getenv("USER_EMAIL")
USER_BBC_EMAIL = os.getenv("USER_BBC_EMAIL")

THIS_FOLDER = Path(__file__).parent.resolve()
CONTACTS_FILE = THIS_FOLDER / 'contacts.csv'
LOGGING_CONF_FILE = THIS_FOLDER / 'logging_conf.json'
CREDENTIALS_FILE = THIS_FOLDER / 'credentials.json'
TOKEN_FILE = THIS_FOLDER / 'token.json'

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

with open(LOGGING_CONF_FILE) as conf_file:
    dict_conf = json.load(conf_file)

logging.config.dictConfig(dict_conf)
logger = logging.getLogger(__name__)


def authenticate() -> Credentials:
    """
    Authenticate the user with Google's API.
    :return: The credentials.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds


class Birthday:

    def __init__(self) -> None:
        """
        Initializes the class.
        """
        self.gmail_user = USER_EMAIL
        self.llm_text = ''
        self.recipients = {}
        self.system_instruction = ''
        self.user_message = ''
        self.person_name = ''
        self.creds = authenticate()

    def prepare_prompt(self) -> None:
        """
        Creates the prompt for the AI.
        :return: None
        """
        joke = random.choice(bv.variables['jokes'])
        fact = random.choice(bv.variables['facts'])
        quote = random.choice(bv.variables['quotes'])
        variables = f'{joke}, {fact} and {quote}'
        self.system_instruction = bv.SYSTEM_INSTRUCTION.replace('[variables]', variables)

    def prepare_user_message(self) -> None:
        """
        Prepares the user message for the AI.
        :return: None
        """
        self.user_message = bv.USER_MESSAGE.replace('[NAME]', self.person_name)

    def get_openai_random(self) -> None:
        """
        Gets a text from OpenAI ChatGPT for the birthday wish
        :return: None
        """
        self.prepare_prompt()
        self.prepare_user_message()
        response = client_openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_instruction},
                {"role": "user", "content": self.user_message},
            ],
            temperature=0.6,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2
        )
        self.llm_text = response.choices[0].message.content

    def get_anthropic_random(self) -> None:
        """
        Gets a text from the Anthropic API.
        :return: None
        """
        self.prepare_prompt()
        self.prepare_user_message()
        message = client_anthropic.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=500,
            temperature=0.6,
            system=self.system_instruction,
            messages=[{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": self.user_message
                }]
            }]
        )
        self.llm_text = message.content[0].text

    def get_recipients(self, contacts_filepath: Path) -> None:
        """
        Check the contacts.csv file and fetch who has their birthday today.
        :param contacts_filepath: The filepath to the csv.
        :return: None
        """
        df = pd.read_csv(contacts_filepath)
        today = date.today()
        df = df[['First Name', 'Last Name', 'Birthday', 'E-mail 1 - Value']]
        for index, row in df.iterrows():
            (_, month, day) = row['Birthday'].strip().replace('--', 'None-').split('-')
            if today.strftime('%m-%d') == f'{month}-{day}':
                self.recipients[index] = {
                    'full_name': f"{row['First Name']} {row['Last Name']}",
                    'name': row['First Name'],
                    'email': row['E-mail 1 - Value']
                }

    def send_email(self, html_email: str, recipient_email: str, subject_email: str,
                   llm_used: Literal['openai', 'anthropic']) -> None:
        """
        Send the email to the birthday person(s)
        :param html_email: The HTML of the letter
        :param recipient_email: The recipient in the form Name Lastname <email>
        :param subject_email: The subject of the email
        :param llm_used: The LLM to use
        :return: None
        """
        service = build('gmail', 'v1', credentials=self.creds)
        message = MIMEMultipart('alternative')

        message['From'] = self.gmail_user
        message['To'] = recipient_email
        message['Bcc'] = USER_BBC_EMAIL
        message['Subject'] = subject_email

        message.attach(MIMEText(html_email, 'html'))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        data = {'raw': raw_message}

        try:
            service.users().messages().send(userId='me', body=data).execute()
            logger.info(f'Email sent to {recipient_email} using {llm_used}.')
        except Exception as e:
            logger.error(f'An error occurred: {e}')


if __name__ == '__main__':
    birthday = Birthday()
    birthday.get_recipients(CONTACTS_FILE)
    if not birthday.recipients:
        logger.info('Nobody has a birthday today!')
    else:
        for _, person in birthday.recipients.items():
            llm: Literal['openai', 'anthropic'] = random.choice(['openai', 'anthropic'])
            birthday.person_name = person['name']
            recipient = f"{person['full_name']} <{person['email']}>"
            subject = f"Happy birthday {person['name']}!"
            html = ''
            if llm == 'openai':
                birthday.get_openai_random()
                html = bv.HTML_TEMPLATE.replace('[LLM_TEXT]', birthday.llm_text)
            elif llm == 'anthropic':
                birthday.get_anthropic_random()
                html = bv.HTML_TEMPLATE.replace('[LLM_TEXT]', birthday.llm_text)
            birthday.send_email(html, recipient, subject, llm)
