import random
from tkinter import *
import pandas


# ___________________________CSV FILE STUFF______________________________

# using try to catch exception when the words_to_learn file is not present when running for first time
try:
    dataframe = pandas.read_csv("data/words_to_learn.csv")   # creating dataframe from words_to_learn.csv file
except FileNotFoundError:
    original_data = pandas.read_csv("data/japanese_words.csv")   # creating dataframe from japanese_words.csv 1st run
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = dataframe.to_dict(orient="records")  # list of dicts with Japanese words and english translation as keys


selected_dict = {}
# print(to_learn)  # printing the list of dictionaries with the words and their translation


# GENERATE A CANVAS WITH JAPANESE CARD
def change_text():
    global selected_dict, flip_timer

    window.after_cancel(flip_timer)   # cancel the card flipping because it has already been flipped

    selected_dict = random.choice(to_learn)
    current_word = selected_dict["Japanese"]

    canvas.itemconfig(word_text, text=current_word, fill="black")    
    canvas.itemconfig(language_title, text="日本語", fill="black")
    canvas.itemconfig(flashcard_image, image=flashcard_front)

    flip_timer = window.after(4000, translate_canvas)  # change card after


# TRANSLATE THE WORD AND SHOW IT IN A NEW CANVAS
def translate_canvas():
    canvas.itemconfig(flashcard_image, image=flashcard_back)   # change color of the card after flipping
    canvas.itemconfig(language_title, fill="white", text="English")    # change font of title of the card
    canvas.itemconfig(word_text, fill="white", text=selected_dict["English"])  # change the word to the eng translation

    # ____________________________DELETE____________________________________-__
    print(selected_dict["Japanese"])     # printing japanese word in console for testing purpose
    print(selected_dict["English"])      # printing japanese word in console for testing purpose
    # __________________________________________________________________________________________


# removing words that user knows from list & creating a new list where only the words that user doesn't know are present
def is_known():
    to_learn.remove(selected_dict)   # removing an item from list of dictionaries(to_learn) if the users knows
    data = pandas.DataFrame(to_learn)   # creating a new dataframe

    # ______________________________________DELETE____________________________________
    print(data)
    print(len(to_learn))  # printing list of dictionaries with translations
    # ________________________________________________________________________________

    data.to_csv("data/words_to_learn.csv", index=False)   # updates file & does not add row numbers and make file messy
    change_text()
 




BACKGROUND_COLOR = "#B1DDC6"


# ______________________UI SETUP__________________________


window = Tk()
window.title("Flashcards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# ____________________________________CANVAS________________________________

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard_front = PhotoImage(file="images/card_front.png")
flashcard_back = PhotoImage(file="images/card_back.png")
flashcard_image = canvas.create_image(400, 263, image=flashcard_front)


# the first two numbers are the x and y value for where the image should be in the canvas
language_title = canvas.create_text(400, 100, text="日本語", font=("Ariel", 30))
# we have word_text as variable because it's easier to change it later when the buttons are pressed and new words
# dont overwrite each other
word_text = canvas.create_text(400, 250, text="", font=("Ariel", 70, "bold"))


canvas.grid(column=1, row=0, columnspan=2)

# BUTTONS

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bd=0, command=change_text)
wrong_button.grid(column=1, row=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bd=0, command=is_known)
right_button.grid(column=2, row=1)

flip_timer = window.after(4000, translate_canvas)
# change text after flip timer cause flip timer is in change text boiiii
change_text()




window.mainloop()
