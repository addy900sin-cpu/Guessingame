import random

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


# ---------- COLORS ----------
BG = (0.035, 0.045, 0.07, 1)
CARD = (0.075, 0.09, 0.13, 1)
CARD2 = (0.10, 0.12, 0.17, 1)
ACCENT = (0.20, 0.55, 1, 1)
GREEN = (0.20, 0.80, 0.45, 1)
RED = (1, 0.30, 0.30, 1)
WHITE = (0.95, 0.97, 1, 1)
GRAY = (0.60, 0.65, 0.72, 1)


class DarkButton(Button):
    background_normal = ""
    background_color = ACCENT
    color = WHITE
    bold = True
    font_size = "17sp"


class GuessingGame(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=[dp(20), dp(18), dp(20), dp(18)],
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

        # ---------- TITLE ----------
        title = Label(
            text="🎯 GUESSING GAME",
            font_size="29sp",
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=dp(55)
        )
        self.add_widget(title)

        subtitle = Label(
            text="Test your luck • Beat your high score",
            font_size="13sp",
            color=GRAY,
            size_hint_y=None,
            height=dp(25)
        )
        self.add_widget(subtitle)

        # ---------- DIFFICULTY ----------
        self.add_widget(Label(
            text="DIFFICULTY",
            font_size="12sp",
            bold=True,
            color=GRAY,
            size_hint_y=None,
            height=dp(28)
        ))

        self.difficulty = Spinner(
            text="Easy",
            values=("Easy", "Medium", "Hard"),
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=CARD2,
            color=WHITE,
            font_size="16sp"
        )
        self.add_widget(self.difficulty)

        # ---------- MESSAGE CARD ----------
        message_box = BoxLayout(
            padding=dp(10),
            size_hint_y=None,
            height=dp(75)
        )

        self.result = Label(
            text="Press NEW GAME to start!",
            font_size="16sp",
            color=WHITE,
            halign="center",
            valign="middle"
        )

        message_box.add_widget(self.result)
        self.add_widget(message_box)

        # ---------- INPUT ----------
        self.guess_input = TextInput(
            hint_text="Enter your number",
            multiline=False,
            input_filter="int",
            font_size="22sp",
            halign="center",
            padding=[dp(10), dp(12)],
            size_hint_y=None,
            height=dp(55),
            background_normal="",
            background_color=CARD2,
            foreground_color=WHITE,
            hint_text_color=GRAY
        )
        self.add_widget(self.guess_input)

        # ---------- GUESS BUTTON ----------
        self.guess_button = DarkButton(
            text="🎯  GUESS",
            size_hint_y=None,
            height=dp(55),
            disabled=True
        )
        self.guess_button.bind(on_press=self.check_guess)
        self.add_widget(self.guess_button)

        # ---------- NEW GAME ----------
        self.new_game_button = Button(
            text="🔄  NEW GAME",
            font_size="16sp",
            bold=True,
            color=WHITE,
            background_normal="",
            background_color=CARD2,
            size_hint_y=None,
            height=dp(50)
        )
        self.new_game_button.bind(on_press=self.start_game)
        self.add_widget(self.new_game_button)

        # ---------- INFO ----------
        self.info = Label(
            text="❤️  Chances: 5       ⭐ Score: 0",
            font_size="15sp",
            color=WHITE,
            size_hint_y=None,
            height=dp(35)
        )
        self.add_widget(self.info)

        # ---------- STATS ----------
        stats_box = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(65)
        )

        self.wins_label = self.create_stat("🏆\nWins: 0")
        self.losses_label = self.create_stat("❌\nLosses: 0")
        self.winrate_label = self.create_stat("📊\nWin Rate: 0%")

        stats_box.add_widget(self.wins_label)
        stats_box.add_widget(self.losses_label)
        stats_box.add_widget(self.winrate_label)

        self.add_widget(stats_box)

        # ---------- FOOTER ----------
        self.add_widget(Label(
            text="Good luck! 🔥",
            font_size="12sp",
            color=GRAY,
            size_hint_y=None,
            height=dp(25)
        ))

    def create_stat(self, text):
        return Label(
            text=text,
            font_size="13sp",
            color=WHITE,
            halign="center",
            valign="middle"
        )

    # ---------- START GAME ----------
    def start_game(self, instance):

        difficulty = self.difficulty.text

        if difficulty == "Easy":
            self.max_number = 10
        elif difficulty == "Medium":
            self.max_number = 20
        else:
            self.max_number = 30

        self.secret_number = random.randint(
            1, self.max_number
        )

        self.chances = 5
        self.score = 0
        self.game_over = False

        self.guess_input.text = ""
        self.guess_input.disabled = False
        self.guess_button.disabled = False

        self.result.color = WHITE
        self.result.text = (
            f"Guess between 1 and {self.max_number}"
        )

        self.update_info()

    # ---------- CHECK GUESS ----------
    def check_guess(self, instance):

        if self.game_over:
            return

        text = self.guess_input.text.strip()

        if not text:
            self.result.color = RED
            self.result.text = "⚠️ Enter a number first!"
            return

        guess = int(text)

        if guess < 1 or guess > self.max_number:
            self.result.color = RED
            self.result.text = (
                f"Enter 1 – {self.max_number}"
            )
            return

        self.chances -= 1

        if guess == self.secret_number:

            self.score = 30 if self.chances == 4 else 10

            self.wins += 1
            self.game_over = True

            self.result.color = GREEN
            self.result.text = (
                f"🎉  CORRECT!\n"
                f"The number was {self.secret_number}"
            )

            self.end_game()

        elif guess < self.secret_number:

            self.result.color = ACCENT
            self.result.text = "📈 Too low! Go higher."

        else:

            self.result.color = ACCENT
            self.result.text = "📉 Too high! Go lower."

        if self.chances == 0 and not self.game_over:

            self.losses += 1
            self.game_over = True

            self.result.color = RED
            self.result.text = (
                f"😢 GAME OVER\n"
                f"The number was {self.secret_number}"
            )

            self.end_game()

        self.guess_input.text = ""
        self.update_info()

    # ---------- END GAME ----------
    def end_game(self):
        self.guess_button.disabled = True
        self.guess_input.disabled = True
        self.update_stats()

    # ---------- UPDATE INFO ----------
    def update_info(self):

        self.info.text = (
            f"❤️  Chances: {self.chances}"
            f"       ⭐ Score: {self.score}"
        )

        self.update_stats()

    # ---------- UPDATE STATS ----------
    def update_stats(self):

        total = self.wins + self.losses

        if total:
            rate = (self.wins / total) * 100
        else:
            rate = 0

        self.wins_label.text = f"🏆\nWins: {self.wins}"
        self.losses_label.text = f"❌\nLosses: {self.losses}"
        self.winrate_label.text = (
            f"📊\nWin Rate: {rate:.1f}%"
        )


class GuessingGameApp(App):

    def build(self):
        Window.clearcolor = BG
        return GuessingGame()


if __name__ == "__main__":
    GuessingGameApp().run()
