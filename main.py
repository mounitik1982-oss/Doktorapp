from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
import ocr_utils
import med_parser

class MedScanLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.image = Image(size_hint=(1, 0.5))
        self.add_widget(self.image)

        self.result_label = Label(text="Scan result will appear here", size_hint=(1, 0.2))
        self.add_widget(self.result_label)

        btn_layout = BoxLayout(size_hint=(1, 0.3))
        btn_layout.add_widget(Button(text="Choose Image", on_press=self.choose_image))
        self.add_widget(btn_layout)

    def choose_image(self, instance):
        chooser = FileChooserIconView(filters=["*.png", "*.jpg", "*.jpeg"], on_selection=self.on_file_selected)
        self.clear_widgets()
        self.add_widget(chooser)

    def on_file_selected(self, chooser, *args):
        if chooser.selection:
            image_path = chooser.selection[0]
            self.display_image(image_path)
            extracted_text = ocr_utils.extract_text(image_path)
            analysis = med_parser.analyze_text(extracted_text)
            self.result_label.text = analysis
            self.add_widget(self.result_label)

    def display_image(self, path):
        pil_image = PILImage.open(path)
        pil_image = pil_image.convert('RGB')
        pil_image = pil_image.resize((Window.width, int(Window.height * 0.5)))
        texture = Texture.create(size=pil_image.size)
        texture.blit_buffer(pil_image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.image.texture = texture
        self.add_widget(self.image)

class MedScanApp(App):
    def build(self):
        return MedScanLayout()

if __name__ == '__main__':
    MedScanApp().run()
