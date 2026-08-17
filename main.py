from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import random


class GuessingGame(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=20,
            spacing=12,
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
            text="🎯 GUESSING GAME",
            font_size="28sp",
            bold=True,
            size_hint_y=None,
            height=60
        ))

        # Difficulty
        self.add_widget(Label(
            text="Select Difficulty",
            font_size="16sp",
            size_hint_y=None,
            height=35
        ))

        self.difficulty = Spinner(
            text="Easy",
            values=("Easy", "Medium", "Hard"),
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.difficulty)

        # Result message
        self.result = Label(
            text="Press NEW GAME to start!",
            font_size="17sp",
            halign="center",
            valign="middle"
        )
        self.add_widget(self.result)

        # Guess input
        self.guess_input = TextInput(
            hint_text="Enter your guess",
            input_filter="int",
            multiline=False,
            font_size="22sp",
            halign="center",
            size_hint_y=None,
            height=55
        )
        self.add_widget(self.guess_input)

        # Guess button
        self.guess_button = Button(
            text="🎯 GUESS",
            font_size="18sp",
            bold=True,
            size_hint_y=None,
            height=55,
            disabled=True
        )
        self.guess_button.bind(on_press=self.check_guess)
        self.add_widget(self.guess_button)

        # New Game
        self.new_game_button = Button(
            text="🔄 NEW GAME",
            font_size="17sp",
            bold=True,
            size_hint_y=None,
            height=55
        )
        self.new_game_button.bind(on_press=self.start_game)
        self.add_widget(self.new_game_button)

        # Game information
        self.info = Label(
            text="Chances: 5    Score: 0",
            font_size="16sp",
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.info)

        # Statistics
        self.stats = Label(
            text="Wins: 0    Losses: 0    Win Rate: 0.0%",
            font_size="15sp",
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.stats)

    def start_game(self, instance):
        difficulty = self.difficulty.text

        if difficulty == "Easy":
            self.max_number = 10
        elif difficulty == "Medium":
            self.max_number = 50
        else:
            self.max_number = 100

        self.secret_number = random.randint(1, self.max_number)
        self.chances = 5
        self.score = 0
        self.game_over = False

        self.guess_input.text = ""
        self.guess_input.disabled = False
        self.guess_button.disabled = False

        self.result.text = (
            f"Guess a number between 1 and {self.max_number}"
        )

        self.update_info()

    def check_guess(self, instance):

        if self.game_over:
            return

        guess_text = self.guess_input.text.strip()

        if not guess_text:
            self.result.text = "⚠️ Enter a number first!"
            return

        guess = int(guess_text)

        if guess < 1 or guess > self.max_number:
            self.result.text = (
                f"⚠️ Enter a number between 1 and {self.max_number}"
            )
            return

        self.chances -= 1

        if guess == self.secret_number:

            # First try bonus
            if self.chances == 4:
                self.score = 30
            else:
                self.score = 10

            self.wins += 1
            self.game_over = True

            self.result.text = (
                f"🎉 CORRECT!\n"
                f"The number was {self.secret_number}"
            )

            self.end_game()

        elif guess < self.secret_number:

            self.result.text = "📈 Too low! Try a higher number."

        else:

            self.result.text = "📉 Too high! Try a lower number."

        if self.chances == 0 and not self.game_over:

            self.losses += 1
            self.game_over = True

            self.result.text = (
                f"😢 GAME OVER!\n"
                f"The number was {self.secret_number}"
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
            f"Chances: {self.chances}    Score: {self.score}"
        )
        self.update_stats()

    def update_stats(self):

        total_games = self.wins + self.losses

        if total_games > 0:
            win_rate = (self.wins / total_games) * 100
        else:
            win_rate = 0

        self.stats.text = (
            f"Wins: {self.wins}    "
            f"Losses: {self.losses}    "
            f"Win Rate: {win_rate:.1f}%"
        )


class GuessingGameApp(App):

    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.08, 1)
        return GuessingGame()


if __name__ == "__main__":
    GuessingGameApp().run()
