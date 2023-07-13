import yfinance as yf
import os
import smtplib
import datetime
import logging.handlers
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# The package name is python-dotenv
from dotenv import load_dotenv

load_dotenv()
TICKERS = os.environ['TICKERS']
TICKERS_LIST = TICKERS.split(',')
GREEN = '#5d921c'
RED = '#ff4411'
recommendations = {'': '', 'hold': '', 'none': '', 'buy': GREEN, 'sell': RED}
today = datetime.datetime.today()
today_formatted = today.strftime("%A, %B %d")

logger = logging.getLogger('stocks-log')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler('stocks-emails.log', maxBytes=5 * 1024 * 1024, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_yahoo_values() -> dict:
    """
    Gets the stock values from Yahoo finance
    :return: a dictionary with the needed values for the email
    """
    tickers = yf.download(TICKERS_LIST, period='5d', interval='1d', progress=False)
    tickers_info = yf.Tickers(TICKERS)
    values = {}
    for tick in TICKERS_LIST:
        # print(dir(tickers_info.tickers[tick]))
        # for key, val in tickers_info.tickers[tick].info.items():
        #     print(key, val)
        # TODO: The recommendation stopped working, so I am commenting it out for now.
        # recommendation = tickers_info.tickers[tick].info.get('recommendationKey', '-')
        before_yesterday_close = tickers['Close'][tick][3]
        yesterday_close = tickers['Adj Close'][tick][4]
        change = yesterday_close - before_yesterday_close
        change_percentage = f"{change / before_yesterday_close:.2%}"
        values[tick] = {
            'by_close': f"{before_yesterday_close:.2f}",
            'ye_close': f"{yesterday_close:.2f}",
            'change': f"{change:.2f}",
            'change_p': change_percentage,
            # 'guidance': recommendation,
        }
    return values


def format_values(values: dict) -> list:
    """
    Formats the values taken from Yahoo and formats them for the email.
    :param values: the data from Yahoo, already filtered.
    :return: a list of lines for the email.
    """
    max_ticker = len(max(TICKERS_LIST + ['stock'], key=len))
    keys = [key for key in [val for val in values.values()][0].keys()]
    max_lengths = {}
    for key in keys:
        max_lengths[key] = len(max([val[key] for val in values.values()] + [key], key=len))
    header = ['stock'] + keys
    guidance = keys.pop()

    lines = [
        "&nbsp;",
        f"Your stocks today {today_formatted}",
        f"<span>{' | '.join(header)}</span>",
    ]
    for stock, val in values.items():
        color = GREEN if float(val['change']) > 0 else RED
        for key in keys:
            val[key] = val[key].rjust(max_lengths[key], '@').replace('@', '&nbsp;')
        val[guidance] = f"<span style=\"color:{recommendations.get(val[guidance], '')};\">" \
                        f"{val[guidance]}</span>"

        lines.append(f"<span style=\"color:{color};\"><strong>"
                     f"{stock.ljust(max_ticker, '@').replace('@', '&nbsp;')}</strong></span> | "
                     f"{' | '.join(val.values())}")
    return lines


def send_email(message: list) -> None:
    """
    Sends an email message
    :param message: The lines of the message
    :return: None
    """
    sender_name = os.environ['SENDER_NAME'].replace('-', ' ')
    sender_email = os.environ['SENDER_EMAIL']
    sender_email_complete = f"{sender_name} <{sender_email}>"
    receiver_name = os.environ['RECIPIENT_NAME'].replace('-', ' ')
    receiver_email = f"{receiver_name} <{os.environ['RECIPIENT_EMAIL']}>"
    password = os.environ['SENDER_PASSWORD']
    subject = f"Your stocks today, {today_formatted}"
    message = '\n'.join(message)

    msg = MIMEMultipart()
    msg['From'] = sender_email_complete
    msg['To'] = receiver_email
    msg['Subject'] = subject

    body = f"""
        <html>
        <body>
        <pre style="font-family:monospace,monospace;font-size:15px;white-space:pre-line;margin:0;">
        <div>
        {message}
        </div>
        </pre>
        </body>
        </html>
        """

    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        logger.info(f'Email sent to {receiver_email}')


def main():
    yahoo_values = get_yahoo_values()
    lines = format_values(yahoo_values)
    send_email(lines)


if __name__ == '__main__':
    main()
