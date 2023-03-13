import tkinter as tk

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
repetitions = 0
stay_alive = None


def reset_timer():
    """
    Reset the timer to start from 25:00 again
    :return: None
    """
    global stay_alive
    global repetitions
    repetitions = 0
    activity_label.config(text='Timer', fg=GREEN)
    checkmark_label.config(text='')
    C.itemconfig(timer_label, text='25:00')
    window.after_cancel(stay_alive)


def start_timer():
    """
    Start the timer and depending on if it is a work or break session, adapt some labels and timing.
    :return: None
    """
    global repetitions
    repetitions += 1
    if repetitions in (1, 3, 5, 7):
        if repetitions == 1:
            add_arrow(0)
        seconds = WORK_MIN * 60
        activity_label.config(text='Work', fg=GREEN)
    elif repetitions in (2, 4, 6):
        add_arrow(repetitions // 2)
        seconds = SHORT_BREAK_MIN * 60
        activity_label.config(text='Break', fg=PINK)
    elif repetitions == 8:
        add_arrow(4)
        seconds = LONG_BREAK_MIN * 60
        repetitions = 0
        activity_label.config(text='Break', fg=RED)
    countdown_clock(seconds)


def add_arrow(num):
    """
    Adds an arrow to the label on the bottom every time a work session finished.
    :param num: The number of the work session that just finished.
    :return: None
    """
    arrows = ' '.join('✔' for _ in range(num))
    checkmark_label.config(text=arrows)


def countdown_clock(countdown):
    """
    It makes the clock go down in time.
    :param countdown: The current second
    :return: None
    """
    if countdown > 0:
        global stay_alive
        minutes = str(countdown // 60).rjust(2, '0')
        seconds = str(round(countdown % 60)).rjust(2, '0')
        C.itemconfig(timer_label, text=f'{minutes}:{seconds}')
        stay_alive = window.after(1000, countdown_clock, countdown - 1)
    else:
        start_timer()


window = tk.Tk()
window.title('Pomodoro timer')
window.config(pady=80, padx=80, bg=YELLOW)

C = tk.Canvas(window, width=200, height=224, bg=YELLOW, bd=0, highlightthickness=0, relief='ridge')
filename = tk.PhotoImage(file="tomato.png")
C.create_image(100, 112, image=filename)
timer_label = C.create_text(100, 125, text='25:00', font=(FONT_NAME, 30, 'bold'), fill='white')
C.grid(column=1, row=1)

activity_label = tk.Label(window, text='Timer', bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50, 'normal'))
activity_label.grid(column=1, row=0)

start_button = tk.Button(text='Start', command=start_timer, font=(FONT_NAME, 18), highlightthickness=0, relief='ridge')
start_button.grid(column=0, row=3)

reset_button = tk.Button(text='Reset', command=reset_timer, font=(FONT_NAME, 18), highlightthickness=0, relief='ridge')
reset_button.grid(column=3, row=3)

checkmark_label = tk.Label(window, text='', fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, 'bold'))
checkmark_label.grid(column=1, row=4)

window.mainloop()
