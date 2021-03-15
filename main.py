from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

# Get words
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
current_card = random.choice(to_learn)

def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_img, image=back_card_img)

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Francais", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_img, image=front_card_img)
    flip_timer = window.after(3000, flip_card)

def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

window = Tk()
window.title("En Francais, S'il Vous Plait")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

# Flash card
front_card_img = PhotoImage(file="images/card_front.png")
back_card_img = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_img = canvas.create_image(400, 263, image=front_card_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 260, text="Word", font=("Arial", 60, "bold"))
canvas.grid(column=0,row=0, columnspan=2)

# Buttons
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, command=is_known, highlightthickness=0)
right_button.grid(column=0, row=1)
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, command=next_card, highlightthickness=0)
wrong_button.grid(column=1, row=1)

next_card()

window.mainloop()