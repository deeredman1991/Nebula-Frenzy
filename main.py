from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock

from kivy.graphics import Color, Rectangle

import random



class Sprite(Image):
    def __init__(self, scale, **kwargs):
        super(Sprite, self).__init__(allow_stretch = True, **kwargs)
        self.texture.mag_filter = 'nearest'
        w, h = self.texture_size
        self.size = (scale * w, scale * h)
        
class PlayerShip(Sprite):
    def __init__(self, scale, center=(0,0), **kwargs):
        super(PlayerShip, self).__init__( scale*0.8, center=center, source='images/PlayerShip1.png')
        self.velocity_y = 0
        self.velocity_x = 0
        
    def update(self):
        self.y += self.velocity_y
        self.x += self.velocity_x
        
class DPad(Widget):
    def __init__(self, scale, player, **kwargs):
        super(DPad, self).__init__(**kwargs)
        
        self.image = Image(source = 'images/DPad.png')
        self.add_widget(self.image)
        
        self.size = self.image.size
        
        '''
        with self.canvas:
            Color(0.5, 0.5, 1.0)
            Rectangle(pos=self.pos, size=self.size)
        '''
        
        self.player = player
        
    def on_touch_down(self, touch):
        print(touch)
        
class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        
        self.size = Window.size
        
        self.image = Image(allow_stretch=True, keep_ratio = False, source=source)
        self.image.size = Window.size
        self.image.height = self.image.width*4
        self.add_widget(self.image)
        
        self.image_dupe = Image(allow_stretch=True, keep_ratio = False, source=source)
        self.image_dupe.size = Window.size
        self.image_dupe.height = self.image_dupe.width*4
        self.image_dupe.y = self.image.height-1
        self.add_widget(self.image_dupe)
        
    def update(self, scale):
        self.image.y -= 5 * scale
        self.image_dupe.y -= 5 * scale
        
        if self.image.top <= 0:
            self.image.y = 0
            self.image_dupe.y = self.image.height-1
    
class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        
        self.background = Background(source='images/background.png')
        self.size = self.background.size
        self.add_widget(self.background)
        
        w, h = Window.size
        w = float(w)/ self.background.width
        h = float(h)/ 384
        self.scale = min(w, h)
        
        self.player = PlayerShip( self.scale, center=(self.background.width/2, self.background.height/2) )
        self.add_widget(self.player)
        
        print(self.background.pos)
        
        self.dpad = DPad ( self.scale, self.player, pos=self.background.pos )
        self.add_widget( self.dpad )
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        
    def update(self, dt):
        self.background.update(self.scale)

class GameApp(App):
    def build(self):
        Window.size = (random.randint(200, 1000), random.randint(200, 1000))
        #Window.size = (300, 500)
        self.title = 'Nebula Frenzy'
        #self.icon = 'images/icon.png'
        return Game()
        
if __name__ == "__main__":
    GameApp().run()