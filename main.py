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
    def __init__(self, scale, background=None, **kwargs):
        super(PlayerShip, self).__init__( scale*0.75, center=(background.width/2, background.height/2), source='images/PlayerShip1.png')
        
        self.background = background
        
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.x < 0:
            self.x = 0
        elif self.x > self.background.width-self.width:
            self.x = self.background.width-self.width
        if self.y < 0:
            self.y = 0
        elif self.y > self.background.height-self.height:
            self.y = self.background.height-self.height
            
class PlayerLazer(Sprite):
    def __init__(self, scale, player=None, **kwargs):
        super(PlayerLazer, self).__init__( scale, pos=player.pos, source='images/BlueLazer.png')
        self.y += player.height
        self.x = player.x - player.width*0.075
        
        self.speed = 6
    def update(self):
        self.y += self.speed
        
class DPad(Widget):
    def __init__(self, scale, player, **kwargs):
        super(DPad, self).__init__(**kwargs)
        
        self.image = Sprite(scale*1.5, source = 'images/DPad.png')
        self.add_widget(self.image)
        
        self.size = self.image.size
        
        self.player = player
        
        self.deadzone = 0.15
        
    def touch_handler(self, touch):
        tx, ty = touch.pos
        if tx  < self.width and ty < self.height:
            if tx > (self.width/2+self.width*self.deadzone):
                self.player.velocity_x = self.player.speed
            elif tx < (self.width/2-self.width*self.deadzone):
                self.player.velocity_x = -self.player.speed
            if ty > (self.height/2+self.height*self.deadzone):
                self.player.velocity_y = self.player.speed
            elif ty < (self.height/2-self.height*self.deadzone):
                self.player.velocity_y = -self.player.speed
    
    def on_touch_down(self, touch):
        self.touch_handler(touch)
        
    def on_touch_move(self, touch):
        self.touch_handler(touch)
    
    def on_touch_up(self, *ignore):
        self.player.velocity_x = 0
        self.player.velocity_y = 0
        
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
        self.image.y -= 1 * scale
        self.image_dupe.y -= 1 * scale
        
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
        
        self.player = PlayerShip( self.scale, background=self.background )
        self.add_widget(self.player)
        
        self.bullettest = PlayerLazer( self.scale, self.player)
        self.add_widget(self.bullettest)
        
        self.bulletlist = [self.bullettest]
        
        self.dpad = DPad ( self.scale, self.player, pos=self.background.pos )
        self.add_widget( self.dpad )
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        
    def update(self, dt):
        self.background.update(self.scale)
        self.player.update()
        
        for bullet in self.bulletlist:
            bullet.update()

class GameApp(App):
    def build(self):
        Window.size = (random.randint(200, 1000), random.randint(200, 1000))
        #Window.size = (300, 500)
        self.title = 'Nebula Frenzy'
        #self.icon = 'images/icon.png'
        return Game()
        
if __name__ == "__main__":
    GameApp().run()