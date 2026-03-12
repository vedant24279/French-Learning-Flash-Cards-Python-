from tkinter import Tk, Canvas, PhotoImage,Button

import pandas
import pandas as pd
import random
current_card = {}
BACKGROUND_COLOR = "#B1DDC6"
TEXT_WHITE = "#ffffff"
TEXT_BLACK = "#000000"
to_learn = {}
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    french_word = current_card["French"]
    canvas.itemconfig(flash_card,image=front_card_image)
    canvas.itemconfig(card_title,text="French",fill=TEXT_BLACK)
    canvas.itemconfig(card_word,text=french_word,fill= TEXT_BLACK)
    flip_timer = window.after(ms=3000, func=answer_card)
def answer_card():
    global current_card
    english_word = current_card["English"]
    canvas.itemconfig(flash_card,image=back_card_image)
    canvas.itemconfig(card_title,text="English",fill=TEXT_WHITE)
    canvas.itemconfig(card_word,text=english_word,fill=TEXT_WHITE)
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)

    next_card()

window = Tk()
window.title("Flask Cards")
window.config(pady=50,padx=50,bg=BACKGROUND_COLOR)
window.minsize(height=576,width=850)

canvas = Canvas(width=800,height=526,bg=BACKGROUND_COLOR,highlightthickness=0)
front_card_image = PhotoImage(file="images/card_front.png")
back_card_image = PhotoImage(file="images/card_back.png")
flash_card = canvas.create_image(400,263,image = front_card_image)
canvas.grid(row=0,column=1,columnspan=2)
card_title = canvas.create_text(400,150,text="",font=("Ariel",40))
card_word = canvas.create_text(400,300,text="",font=("Ariel",60,"bold"))

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image,command=next_card)
unknown_button.config(highlightthickness=0)
unknown_button.grid(row=1,column=1)

right_image = PhotoImage(file="images/right.png")
known_button = Button(image=right_image,command=is_known)
known_button.config(highlightthickness=0)
known_button.grid(row=1,column=2)
flip_timer = window.after(ms=3000, func=answer_card)
next_card()








window.mainloop()
