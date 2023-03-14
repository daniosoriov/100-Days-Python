import tkinter as tk
import pandas as pd
import os
import string
import random
import pyperclip
from tkinter import messagebox

MIN_PASSWORD_LENGTH = 20
MAX_PASSWORD_LENGTH = 25
CSV_FILE = 'passwords.csv'


def create_password() -> None:
    """
    Creates a random password between MIN_PASSWORD_LENGTH and MAX_PASSWORD_LENGTH characters.
    :return: None
    """
    size = random.randint(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
    population = string.ascii_letters + string.punctuation.replace(',', '')
    pwd_field.delete(0, tk.END)
    password = ''.join([random.choice(population) for _ in range(size)])
    pyperclip.copy(password)
    pwd_field.insert(0, password)


def save_password() -> None:
    """
    Saves a password to the file passwords.csv.
    :return: None
    """
    website = website_field.get().strip()
    user = email_field.get().strip()
    password = pwd_field.get().strip()

    if not website or not user or not password:
        messagebox.showerror(title='Invalid input', message='Please fill out all the fields')
        return

    message = f'Are you sure you want to save this password?\n' \
              f'Website: {website}\n' \
              f'User/Email: {user}\n' \
              f'Password: {password}'
    if not messagebox.askokcancel(title=f'Saving password to {website}', message=message):
        return

    df = pd.DataFrame([{'website': website, 'user': user, 'password': password}])
    df = df.set_index('website')
    if os.path.exists(CSV_FILE):
        old_df = pd.read_csv(CSV_FILE, index_col=['website'])
        df = df.combine_first(old_df)

    df.to_csv(CSV_FILE)

    website_field.delete(0, tk.END)
    pwd_field.delete(0, tk.END)


window = tk.Tk()
window.title('Password Manager')
window.config(pady=50, padx=50)

canvas = tk.Canvas(window, width=200, height=200, highlightthickness=0)
photo = tk.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=photo)
canvas.grid(column=1, row=0)

website_label = tk.Label(text='Website:')
website_label.grid(column=0, row=1)
website_field = tk.Entry(width=37)
website_field.grid(column=1, row=1, columnspan=2)
website_field.focus()

email_label = tk.Label(text='Email/Username:')
email_label.grid(column=0, row=2)
email_field = tk.Entry(width=37)
email_field.grid(column=1, row=2, columnspan=2)
email_field.insert(0, 'danioshi@gmail.com')

pwd_label = tk.Label(text='Password:')
pwd_label.grid(column=0, row=3)
pwd_field = tk.Entry(width=20)
pwd_field.grid(column=1, row=3)
pwd_gen_button = tk.Button(text='Generate Password', command=create_password)
pwd_gen_button.grid(column=2, row=3)

add_button = tk.Button(text='Add', width=35, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
