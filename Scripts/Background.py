from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image

class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        
        self.size = Window.size
        
        self.image = Image(allow_stretch=True, keep_ratio = False, source=source)
        self.image.size = Window.size
        self.image.height = int(self.image.width*4)
        self.image.width = self.image.width+4
        self.image.x = -2
        self.add_widget(self.image)
        
        self.image_dupe = Image(allow_stretch=True, keep_ratio = False, source=source)
        self.image_dupe.size = Window.size
        self.image_dupe.height = int(self.image_dupe.width*4)
        self.image_dupe.width = self.image_dupe.width+4
        self.image_dupe.x = -2
        self.image_dupe.y = self.image.height-2
        self.add_widget(self.image_dupe)
        
    def update(self):
        self.image.y -= 4 * self.parent.scale
        self.image_dupe.y -= 4 * self.parent.scale
        
        if self.image.top <= 0:
            self.image.y = 0
            self.image_dupe.y = self.image.height-2