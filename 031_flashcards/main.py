import tkinter as tk
import csv
import random as r
import json

BACKGROUND_COLOR = "#B1DDC6"
FONT = 'Arial'
MEMORY_FILE = 'data/memory.json'
LIMIT_YES = 10
current_lang = 'French'


def show_info() -> None:
    """
    Shows the opposite information for the flashcard
    :return: None
    """
    global current_lang
    current_word = canvas.itemcget(word_label, 'text')
    if current_lang == 'French':
        fr_en_word = translations[current_word]
    else:
        fr_en_word = [k for k, v in translations.items() if v == current_word][0]
    canvas.itemconfig(word_label, text=fr_en_word)
    switch_languages()


def switch_languages() -> None:
    """
    Switches the language from French to English or vice versa
    :return: None
    """
    global current_lang
    canvas.itemconfig(img, image=back_img if current_lang == 'French' else front_img)
    show_info_button.config(text='Hide' if current_lang == 'French' else 'Show')
    current_lang = 'English' if current_lang == 'French' else 'French'
    color = 'white' if current_lang == 'English' else 'black'
    canvas.itemconfig(lang_label, text=current_lang, fill=color)
    canvas.itemconfig(word_label, fill=color)


def change_word() -> None:
    """
    Changes the current word for a new one to check
    :return: None
    """
    global current_lang
    with open(MEMORY_FILE) as file:
        data = json.load(file)
    possible_words = [w for w, n in data.items() if n < LIMIT_YES]
    if len(possible_words):
        new_word = r.choice(possible_words)
    else:
        new_word = f'Done! You know {len(data)} words'
        yes_button.config(state='disabled')
        no_button.config(state='disabled')
    canvas.itemconfig(word_label, text=new_word)

    if current_lang == 'English':
        switch_languages()


def no_remember() -> None:
    """
    When the user hits the X button
    :return: None
    """
    remember(False)


def yes_remember() -> None:
    """
    When the user hits the check button
    :return: None
    """
    remember(True)


def remember(yes: bool) -> None:
    """
    Perform the actions after the usr either knows the word or doesn't
    :param yes: True if the user remembers, False otherwise
    :return: None
    """
    rem = 1 if yes else -1
    current_word = canvas.itemcget(word_label, 'text')
    try:
        with open(MEMORY_FILE) as file:
            data = json.load(file)
    except FileNotFoundError:
        with open(MEMORY_FILE, 'w') as file:
            new_data = {current_word: rem}
            json.dump(new_data, file, indent=4)
    else:
        data[current_word] = data.get(current_word, 0) + rem
        with open(MEMORY_FILE, 'w') as file:
            json.dump(data, file, indent=4)
    change_word()


translations, french_words = {}, {}
try:
    with open('data/french_words.csv') as csv_file:
        data_words = csv.reader(csv_file)
        translations = {row[0]: row[1] for n, row in enumerate(data_words) if n > 0}
except FileNotFoundError as error:
    print(error)
    quit()
else:
    french_words = translations.keys()

try:
    with open(MEMORY_FILE) as json_file:
        data_memory = json.load(json_file)
except FileNotFoundError:
    with open(MEMORY_FILE, 'w') as json_file:
        new_memory = {w: 0 for w in french_words}
        json.dump(new_memory, json_file, indent=4)
else:
    for w in french_words:
        if w not in data_memory:
            data_memory[w] = 0
    with open(MEMORY_FILE, 'w') as json_file:
        json.dump(data_memory, json_file, indent=4)

window = tk.Tk()
window.title('Flashcards')
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(window, width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = tk.PhotoImage(file='images/card_front.png')
back_img = tk.PhotoImage(file='images/card_back.png')
img = canvas.create_image(400, 263, image=front_img)
canvas.grid(column=0, row=0, columnspan=4)

lang_label = canvas.create_text(400, 150, font=(FONT, 40, 'italic'), text='French', fill='black')
word_label = canvas.create_text(400, 263, font=(FONT, 60, 'bold'), text='', fill='black')
change_word()

show_info_button = tk.Button(text='Show', highlightthickness=0, command=show_info, font=('Verdana', 15))
show_info_button.grid(column=0, row=1)

no_img = tk.PhotoImage(file='images/wrong.png')
no_button = tk.Button(image=no_img, highlightthickness=0, command=no_remember)
no_button.grid(column=1, row=1)

yes_img = tk.PhotoImage(file='images/right.png')
yes_button = tk.Button(image=yes_img, highlightthickness=0, command=yes_remember)
yes_button.grid(column=2, row=1)

placeholder = tk.Label(text='Show', fg=BACKGROUND_COLOR, bg=BACKGROUND_COLOR)
placeholder.grid(column=3, row=1)

window.mainloop()
