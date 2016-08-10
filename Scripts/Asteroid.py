from kivy.graphics import Color, Rectangle, Rotate
from kivy.graphics.context_instructions import PushMatrix, PopMatrix
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import random

from Sprite import Sprite

class Asteroid(Sprite):
    def __init__(self, scale, background=None, **kwargs):
    
        self.metal = True if random.randint(1,2) == 1 else False
        
        self.source = 'images/{}Asteroid{}.png'.format('Metal' if self.metal else '', random.randint(1,5))
        
        super(Asteroid, self).__init__(scale*random.uniform(0.75, 1), **kwargs)
        
        self.background_width = background.width
        self.background_height = background.height
        
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            
        with self.canvas.after:
            PopMatrix()
        
        self.on_start()
        
    def on_start(self):
        self.rot_velocity = random.randrange(-4, 4)
        self.speed = random.uniform(3, 5)
        self.velocity_x = random.uniform(-self.speed*0.1, self.speed*0.1)
        self.velocity_y = self.speed
        
        self.collision = False
        
        self.score_value = 10
        self.metal_value = 1
        
        
    def update(self):
        self.x -= self.velocity_x
        self.y -= self.velocity_y
        
        self.rot.angle += self.rot_velocity
        self.rot.origin = self.center
        
        if self.y < -self.height+40:
            self.collision = True
            
        if self.collision == True:
            self.parent.enemyList.remove(self)
            
            #Optimized to recycle asteroids but causes graphical errors
            #self.parent.standby_enemyList.append(self)
            
            #temporary
            parent = self.parent
            self.parent.standby_enemyList.append(self)
            self.parent.remove_widget(self)
            self.pos = (random.randint(0, int(self.background_width-self.width)), Window.height+((self.height+self.width)*2))
            
    def on_killed(self):
        self.y = -self.height
        self.parent.player.score += self.score_value
        if self.metal == True:
            self.parent.player.metal += self.metal_value