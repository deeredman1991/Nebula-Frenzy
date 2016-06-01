from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock



class Spirte(Image):
    def __init__(self, scale, **kwargs):
        super(Sprite, self).__init__(allow_stretch = True, **kwargs)
        self.texture.mag_filter = 'nearest'
        w, h = self.texture_size
        self.size = (scale * w, scale * h)
        
class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        
        self.size = Window.size
        
        self.image = Image(source=source)
        self.image.size = Window.size
        self.add_widget(self.image)
        
        self.image_dupe = Image(source=source, y=self.height)
        self.image_dupe.size = Window.size
        self.add_widget(self.image_dupe)
        
    def update(self, scale):
        self.image.y -= 0.5 * scale
        self.image_dupe.y -= 0.5 * scale
        
        if self.image.top <= 0:
            self.image.y = 0
            self.image_dupe.y = self.height
    
class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        
        self.background = Background(source='images/background.png')
        self.size = self.background.size
        self.add_widget(self.background)
        
        w, h = Window.size
        w = float(w)/ self.background.width
        h = float(h)/ self.background.height
        self.scale = min(w, h)
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        
    def update(self, dt):
        self.background.update(self.scale)

class GameApp(App):
    def build(self):
        self.title = 'Nebula Frenzy'
        #self.icon = 'images/icon.png'
        return Game()
        
if __name__ == "__main__":
    GameApp().run()