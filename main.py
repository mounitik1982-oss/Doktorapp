from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.add_widget(Label(text="Welcome to MedScan AI", font_size=24))
        scan_button = Button(text="Start Scan", size_hint=(1, None), height=50)
        self.add_widget(scan_button)

class MedScanApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MedScanApp().run()
