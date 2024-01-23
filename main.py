import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from random import choice, shuffle

class ColorMatchingApp(App):
    def build(self):
        self.colors = self.generate_colors()
        self.target_color = choice(self.colors)
        self.score = 0  # Inicializace skóre
        self.is_game_over = False
        return self.create_ui()

    def generate_colors(self):
        # Definice různých barev v RGBA formátu
        colors = [
            (1, 0, 0, 1),  # Red
            (0, 1, 0, 1),  # Green
            (0, 0, 1, 1),  # Blue
            (1, 1, 0, 1),  # Yellow
            (1, 0, 1, 1),  # Magenta
            (0, 1, 1, 1),  # Cyan
            (0.5, 0, 0, 1),  # Maroon
            (1, 1, 0.5, 1),  # Light Yellow
            (0.5, 1, 0, 1),  # Lime Green
            (0, 0.5, 0, 1),  # Dark Green
            (0, 1, 0.5, 1),  # Sea Green
            (0, 0.5, 1, 1),  # Sky Blue
            (0.5, 0, 1, 1),  # Purple
            (1, 0, 0.5, 1),  # Salmon
        ]
        return colors

    def create_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=10)
        label = Label(text="Match the color:", font_size=20)
        layout.add_widget(label)

        target_color_button = Button(background_color=self.target_color, size_hint=(None, None), height=80, width=80, pos_hint={'center_x': 0.5})
        layout.add_widget(target_color_button)

        # Zobrazení skóre
        score_label = Label(text=f"Skóre: {self.score}", font_size=16)
        layout.add_widget(score_label)

        option_buttons_layout = BoxLayout(spacing=10)
        options = self.colors.copy()
        shuffle(options)

        for color in options:
            button = Button(background_color=color, size_hint=(None, None), height=50, width=50)
            button.bind(on_press=self.on_button_press)
            option_buttons_layout.add_widget(button)

        layout.add_widget(option_buttons_layout)

        #End button
        end_button = Button(text="End Game", on_press=self.end_game)
        layout.add_widget(end_button)

        return layout

    def on_button_press(self, button):
        if not self.is_game_over:
            target_color = self.target_color
            selected_color = button.background_color
            '''ověření zda jsou barvy shodné v toleranci, 
            převede target_color a selected_color do jednoho listu,
            abs ověřuje že je absolutní rozdíl mezi nimi menší než tolerance'''
            tolerance = 0.01
            match = all(abs(target - selected) < tolerance for target, selected in zip(target_color, selected_color))

            diff = [abs(target - selected) for target, selected in zip(target_color, selected_color)]
            if match:
                self.score += 1  # Inkrementace skóre
            else:
                self.show_popup("Konec hry", "Špatná barva.")
                self.score = 0  # Reset skóre

            # Aktualizace zobrazení skóre
            self.root.children[0].text = f"Skóre: {self.score}"

            # Resetování hry, pokud není konec
            if not self.is_game_over:
                self.reset_game()

    def end_game(self, instance):
        self.is_game_over = True
        self.show_popup("Konec hry", f"Hra skončila. Tvé konečné skóre: {self.score}")

    def show_popup(self, title, content):
        box_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box_layout.add_widget(Label(text=content, font_size=16))
        popup = Popup(title=title, content=box_layout, size_hint=(None, None), size=(260, 150), auto_dismiss=True)
        popup.open()

    def reset_game(self):
        self.target_color = choice(self.colors)
        self.root.clear_widgets()
        self.root.add_widget(self.create_ui())

if __name__ == '__main__':
    ColorMatchingApp().run()
