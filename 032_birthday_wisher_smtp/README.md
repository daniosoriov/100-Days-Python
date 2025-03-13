# Birthday Email Sender

This internal project is designed to send personalized birthday emails to contacts listed in a CSV file. The emails can
include jokes, facts, and quotes generated using either OpenAI's GPT-4 or Anthropic's Claude.

## Features

- Fetches contacts from a CSV file and checks for birthdays.
- Generates personalized birthday messages using OpenAI or Anthropic.
- Sends HTML formatted emails with personalized content.
- Logs activities and errors for monitoring.

## Requirements

- Python 3.8+
- The following Python packages (listed in `requirements.txt`):
    - `anthropic`
    - `pandas`
    - `python-dotenv`
    - `openai`
    - `google-auth`
    - `google-auth-httplib2`
    - `google-auth-oauthlib`
    - `google-api-python-client`

## Setup

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the root directory with the following environment variables:**
   ```env
   USER_EMAIL=<your-email>
   USER_BBC_EMAIL=<your-bcc-email>
   OPENAI_API_KEY=<your-openai-api-key>
   ANTHROPIC_API_KEY=<your-anthropic-api-key>
   ```

4. **Prepare the `contacts.csv` file in the root directory with the following columns:**
    - `First Name`
    - `Last Name`
    - `Birthday` (format: `YYYY-MM-DD` or ` --MM-DD`)
    - `E-mail 1 - Value`

This file is downloaded from Google Contacts, and it contains the required columns for the script to work.

## Usage

1. **Run the script:**
   ```sh
   python main.py
   ```

2. **The script will:**
    - Check the `contacts.csv` file for today's birthdays.
    - Generate a personalized birthday message using the specified source (`openai` or `anthropic`).
    - Email each birthday contact.

## Python Anywhere and Google Authentication

**UPDATE**: I removed the dependency, and instead I am using an App Password (less secure) to authenticate with Google
via SMTP.

Unfortunately, I was unable to automate the authentication process for Google Cloud and Python Anywhere, as it requires
OAuth2 verification. This means that the script will not work on Python Anywhere, as it requires manual intervention to
authenticate the app.

To run the script on Python Anywhere, you will need to run it locally and then upload the generated `token.json` file to
the Python Anywhere server.

In this way, the script will be able to authenticate with Google Cloud and send emails automatically.

Since the token expires after a certain period, you will need to re-authenticate the app every time the token expires.

## License

This project is for internal use only and is not publicly available.