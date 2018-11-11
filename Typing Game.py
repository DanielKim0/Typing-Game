import random
import sys
import tkinter as ttk
from tkinter import messagebox

class Question:
    def __init__(self, player, word):
        self.word = word.strip()
        self.player = player

    def calculate_points(self):
        total = 0
        char_points = {"a":1, "b":3, "c":3, "d":2, "e":1, "f":4, "g":2, "h":4, "i":1, "j":8, "k":5, "l":1, "m":3,
                       "n":1, "o":1, "p":3, "q":10, "r":1, "s":1, "t":1, "u":1, "v":4, "w":4, "x":8, "y":4, "z":10}
        letters = list(self.word)
        for char in letters:
            total += char_points[char]
        return total

    def query_answer(self, typed):
        if typed == self.word:
            self.player.points.set(self.player.points.get() + self.calculate_points())
            self.player.result.set("Success!")
        else:
            self.player.lives.set(self.player.lives.get() - 1)
            self.player.result.set("Failure!")

    def full_query(self):
        typed = self.player.word_entry.get()
        self.query_answer(typed)

class Interface:
    def __init__(self):
        self.words = list(open("words.txt", "r"))
        self.name = ""
        self.started = False

        self.root = ttk.Tk()
        self.root.title = "Typing Game"
        self.file = open("highscore.txt", "r")
        self.scores = list(self.file)
        self.file.close()

        self.word_entry = ttk.Entry(self.root, font=36)
        self.word_button = ttk.Button(self.root, text="Enter word", font=36)
        self.question = ttk.Label(self.root, text="Please type your name in the box.", font=36)
        self.word_label = ttk.Label(self.root, font=36)
        self.time_label = ttk.Label(self.root, text="Time:", font=36)
        self.score_label = ttk.Label(self.root, text="Score:", font=36)
        self.time_value = ttk.Label(self.root, font=36)
        self.score_value = ttk.Label(self.root, font=36)
        self.life_label = ttk.Label(self.root, text="Lives:", font=36)
        self.life_value = ttk.Label(self.root, font=36)
        self.result_label = ttk.Label(self.root, font=36)
        self.high_score_label = ttk.Label(self.root, font=36, text="High Score:")
        self.high_score_value = ttk.Label(self.root, font=36, text=(str(self.scores[0]) + self.scores[1]))

        self.question.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.word_label.grid(row=1, column=0, columnspan=2, sticky="NSEW")
        self.word_entry.grid(row=2, column=0, columnspan=2, sticky="NSEW")
        self.word_button.grid(row=3, column=0, columnspan=2, sticky="NSEW")
        self.time_label.grid(row=4, column=0, sticky="NSEW")
        self.time_value.grid(row=4, column=1, sticky="NSEW")
        self.score_label.grid(row=5, column=0, sticky="NSEW")
        self.score_value.grid(row=5, column=1, sticky="NSEW")
        self.life_label.grid(row=6, column=0, sticky="NSEW")
        self.life_value.grid(row=6, column=1, sticky="NSEW")
        self.result_label.grid(row=7, column=0, columnspan=2, sticky="NSEW")
        self.high_score_label.grid(row=8, column=0, sticky="NSEW")
        self.high_score_value.grid(row=8, column=1, sticky="NSEW")

        self.lives = ttk.IntVar()
        def lives_alter(*args):
            self.life_value.config(text=self.lives.get())
        self.lives.trace("w", lives_alter)
        self.lives.set(3)

        self.points = ttk.IntVar()
        def score_alter(*args):
            self.score_value.config(text=self.points.get())
        self.points.trace("w", score_alter)
        self.points.set(0)

        self.word = ttk.StringVar()
        def word_alter(*args):
            self.word_label.config(text=self.word.get())
        self.word.trace("w", word_alter)
        self.word.set("")

        self.result = ttk.StringVar()
        def result_alter(*args):
            self.result_label.config(text=self.result.get())
        self.result.trace("w", result_alter)
        self.result.set("Type in your name and press Enter!")

        self.time = ttk.IntVar()
        def time_alter(*args):
            self.time_value.config(text=self.time.get())
        self.time.trace("w", time_alter)
        self.time.set(60)

        self.root.geometry("500x500")
        for x in range(9):
            self.root.rowconfigure(x, weight=1)
        for x in range(2):
            self.root.columnconfigure(x, weight=1)

    def high_score(self):
        if int(self.scores[0]) < self.points.get():
            messagebox.showinfo("Game Over!", "You got a high score!")
            file = open("highscore.txt", "w")
            file.write(str(self.points.get()))
            file.write("\n" + self.name)
            file.close()
        else:
            messagebox.showinfo("Game Over!", "Game Over!")

    def game_over_check(self):
        if self.lives.get() == 0:
            self.high_score()
            sys.exit()
        else:
            return False

    def timer(self):
        if self.time.get() > 0 and self.lives.get() > 0:
            self.time.set(self.time.get()-1)
            self.root.after(1000, self.timer)
        elif self.lives.get() > 0:
            self.lives.set(0)
            self.game_over_check()

    def type_game(self):
        chosen = random.choice(self.words)
        self.word.set(chosen)

    def check_game(self, *args):
        if not self.started:
            self.name = self.word_entry.get()
            self.result.set("Type in the word!")
            self.question.config(text="Type in the word below!")
            self.word_entry.delete(0, ttk.END)
            player.type_game()
            player.timer()
            self.started = True
        else:
            question = Question(self, self.word.get())
            question.full_query()
            self.game_over_check()
            player.type_game()
            self.word_entry.delete(0, ttk.END)

player = Interface()
player.word_button.config(command=player.check_game)
player.root.bind("<Return>", player.check_game)
player.root.mainloop()