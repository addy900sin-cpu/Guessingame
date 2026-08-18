import random

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


class GuessingGame(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            **kwargs
        )

        self.secret_number = 0
        self.max_number = 10
        self.chances = 5
        self.score = 0
        self.wins = 0
        self.losses = 0
        self.game_over = True

        # Title
        self.add_widget(Label(
            text="GUESSING GAME",
            font_size="28sp",
            bold=True,
            size_hint_y=None,
            height=dp(60)
        ))

        # Difficulty
        self.add_widget(Label(
            text="Select Difficulty",
            size_hint_y=None,
            height=dp(30)
        ))

        self.difficulty = Spinner(
            text="Easy",
            values=("Easy", "Medium", "Hard"),
            size_hint_y=None,
            height=dp(50)
        )
        self.add_widget(self.difficulty)

        # Message
        self.result = Label(
            text="Press NEW GAME to start",
            font_size="16sp"
        )
        self.add_widget(self.result)

        # Input
        self.guess_input = TextInput(
            hint_text="Enter your number",
            input_filter="int",
            multiline=False,
            font_size="22sp",
            halign="center",
            size_hint_y=None,
            height=dp(55)
        )
        self.add_widget(self.guess_input)

        # Guess
        self.guess_button = Button(
            text="GUESS",
            font_size="18sp",
            size_hint_y=None,
            height=dp(55),
            disabled=True
        )
        self.guess_button.bind(on_press=self.check_guess)
        self.add_widget(self.guess_button)

        # New game
        self.new_game_button = Button(
            text="NEW GAME",
            font_size="17sp",
            size_hint_y=None,
            height=dp(55)
        )
        self.new_game_button.bind(on_press=self.start_game)
        self.add_widget(self.new_game_button)

        # Info
        self.info = Label(
            text="Chances: 5    Score: 0",
            size_hint_y=None,
            height=dp(40)
        )
        self.add_widget(self.info)

        # Stats
        self.stats = Label(
            text="Wins: 0    Losses: 0    Win Rate: 0.0%",
            size_hint_y=None,
            height=dp(45)
        )
        self.add_widget(self.stats)

    def start_game(self, instance):
        difficulty = self.difficulty.text

        if difficulty == "Easy":
            self.max_number = 10
        elif difficulty == "Medium":
            self.max_number = 20
        else:
            self.max_number = 40

        self.secret_number = random.randint(1, self.max_number)
        self.chances = 5
        self.score = 0
        self.game_over = False

        self.guess_input.text = ""
        self.guess_input.disabled = False
        self.guess_button.disabled = False

        self.result.text = (
            "Guess a number between 1 and "
            + str(self.max_number)
        )

        self.update_info()

    def check_guess(self, instance):

        if self.game_over:
            return

        text = self.guess_input.text.strip()

        if not text:
            self.result.text = "Enter a number first!"
            return

        try:
            guess = int(text)
        except ValueError:
            self.result.text = "Enter a valid number!"
            return

        if guess < 1 or guess > self.max_number:
            self.result.text = (
                "Enter a number between 1 and "
                + str(self.max_number)
            )
            return

        self.chances -= 1

        if guess == self.secret_number:

            if self.chances == 4:
                self.score = 30
            else:
                self.score = 10

            self.wins += 1
            self.game_over = True

            self.result.text = (
                "CORRECT!\nThe number was "
                + str(self.secret_number)
            )

            self.end_game()

        elif guess < self.secret_number:

            self.result.text = "Too low! Try higher."

        else:

            self.result.text = "Too high! Try lower."

        if self.chances == 0 and not self.game_over:

            self.losses += 1
            self.game_over = True

            self.result.text = (
                "GAME OVER!\nThe number was "
                + str(self.secret_number)
            )

            self.end_game()

        self.guess_input.text = ""
        self.update_info()

    def end_game(self):
        self.guess_button.disabled = True
        self.guess_input.disabled = True
        self.update_stats()

    def update_info(self):
        self.info.text = (
            "Chances: "
            + str(self.chances)
            + "    Score: "
            + str(self.score)
        )

        self.update_stats()

    def update_stats(self):

        total = self.wins + self.losses

        if total > 0:
            win_rate = (self.wins / total) * 100
        else:
            win_rate = 0

        self.stats.text = (
            "Wins: "
            + str(self.wins)
            + "    Losses: "
            + str(self.losses)
            + "    Win Rate: "
            + str(round(win_rate, 1))
            + "%"
        )


class GuessingGameApp(App):

    def build(self):
        Window.clearcolor = (0.04, 0.05, 0.08, 1)
        return GuessingGame()


if __name__ == "__main__":
    GuessingGameApp().run()
