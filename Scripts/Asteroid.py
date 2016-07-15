from kivy.graphics import Color, Rectangle, Rotate
from kivy.graphics.context_instructions import PushMatrix, PopMatrix
from kivy.core.audio import SoundLoader
import random

from Sprite import Sprite

class Asteroid(Sprite):
    def __init__(self, scale, background=None, **kwargs):
        super(Asteroid, self).__init__(scale*random.uniform(0.75, 1), source='images/Asteroid{}.png'.format(random.randint(1,5)), **kwargs)
        
        self.pos = (random.randint(0, int(background.width-self.width)), int(background.height))
        
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            
        with self.canvas.after:
            PopMatrix()
        
        self.rot_velocity = random.randrange(-4, 4)
        self.speed = random.uniform(3, 5)
        self.velocity_x = random.uniform(-self.speed*0.1, self.speed*0.1)
        self.velocity_y = self.speed
        
        self.score_value = 10
        
        self.collision = False
        
    def update(self):
        self.x -= self.velocity_x
        self.y -= self.velocity_y
        
        self.rot.origin = self.center
        self.rot.angle += self.rot_velocity
        
        if self.y < -self.height:
            self.collision = True
            
        if self.collision == True:
            self.parent.enemyList.remove(self)
            self.parent.remove_widget(self)
            
    def on_killed(self):
        self.parent.player.score += self.score_value