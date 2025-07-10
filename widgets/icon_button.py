from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, PushMatrix, PopMatrix, Scale
from kivy.properties import NumericProperty


class IconButton(ButtonBehavior, BoxLayout):
    icon = StringProperty("")
    text = StringProperty("Botão")
    scale = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=5, **kwargs)

        with self.canvas.before:
            PushMatrix()
            self.scale_matrix = Scale(1.0, 1.0, 1.0)
            self.scale_matrix.origin = self.center
            self.bind(
                pos=self._update_scale_origin,
                size=self._update_scale_origin,
                scale=self._update_scale  
            )

            Color(rgba=(0.4, 0.7, 0.65, 1))  # Fundo verde escuro
            self.bg = RoundedRectangle(radius=[16])

        with self.canvas.after:
            PopMatrix()
        
        self.image = Image(source=self.icon, size_hint=(None, None), size=(100, 100), allow_stretch=True, pos_hint={"center_x": 0.5})
        self.label = Label(text=self.text, font_size=14, bold=True, color=(1, 1, 1, 1), size_hint=(1, None), height=20, halign="center", valign="middle")
        self.label.bind(size=self._update_label_text_size)

        self.add_widget(self.image)
        self.add_widget(self.label)

        self.bind(pos=self.update_bg, size=self.update_bg)
        self.bind(icon=self.update_icon, text=self.update_text)
    
    def _update_label_text_size(self, instance, size):
        instance.text_size = (size[0], None)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update_icon(self, *args):
        self.image.source = self.icon

    def update_text(self, *args):
        self.label.text = self.text

    def on_press(self):
        Animation(scale=0.95, duration=0.1).start(self)

    def on_release(self):
        Animation(scale=1.0, duration=0.1).start(self)

    def _update_scale_origin(self, *args):
        if hasattr(self, "scale_matrix"):
            self.scale_matrix.origin = self.center

    def _update_scale(self, instance, value):
        self.scale_matrix.x = value
        self.scale_matrix.y = value

