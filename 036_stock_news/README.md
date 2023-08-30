# Stock Analysis with Yahoo Finance

## Overview

This script provides functionalities to fetch stock values from Yahoo Finance, process the retrieved data, and possibly
send out email notifications based on the stock's performance.

## Features

- **Data Retrieval**: Uses the `yfinance` library to download stock values for a list of tickers.
- **Data Processing**: Processes the downloaded data to obtain relevant metrics, such as:
    - Before yesterday's closing price
    - Yesterday's closing price
    - Change in price
    - Percentage change in price

- **Email Notifications**: (As inferred) The script contains imports suggesting that it might send out email
  notifications based on certain criteria.
- **Logging**: Uses a rotating log handler to log relevant events and activities.
- **Environment Management**: Manages environment variables and configurations using `dotenv`.

## Dependencies

To run the script, ensure you have the following dependencies installed:

- `yfinance`
- `os`
- `smtplib`
- `datetime`
- `logging`
- `dotenv`

You can also check `requirements.txt` for the full list of dependencies.

## Environment Variables

The script uses the following environment variables:

- `TICKERS`: A comma-separated list of tickers to fetch data for.
- `RECIPIENT_NAME`: The name of the recipient.
- `RECIPIENT_EMAIL`: The email address of the recipient.
- `SENDER_NAME`: The name of the sender.
- `SENDER_EMAIL`: The email address of the sender.
- `SENDER_PASSWORD`: The password of the sender's email address.

## How to Run

1. Ensure all dependencies are installed.
2. Set up environment variables using a file `.env`.
3. Run the command:

    ```bash
    python main.py
    ```

## Logging

The script uses a rotating log handler to log relevant events and activities. The logs are stored in
the `stocks-emails.log` file.

## Example Output

```text
Your stocks today Wednesday, August 30
stock | by_close | ye_close | change | change_p
ABCD  |   180.19 |   184.12 |   3.93 | 2.18%
EFGH  |    41.08 |    43.31 |   2.23 | 5.43%
IJKL  |    11.98 |    12.11 |   0.13 | 1.09%
MNOP  |    71.26 |    72.20 |   0.94 | 1.32%
QRST  |    97.41 |    98.91 |   1.50 | 1.54%
UVWX  |     7.06 |     7.28 |   0.22 | 3.12%
```

## License

This project is licensed under the terms of the [MIT](https://choosealicense.com/licenses/mit/) license.
