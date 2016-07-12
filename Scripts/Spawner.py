from kivy.uix.widget import Widget
import random

from Powerup import Powerup
from Asteroid import Asteroid

class Spawner(Widget):
    def __init__(self, **kwargs):
        super(Spawner, self).__init__(**kwargs)
        self.debug = True
    
    def spawn_asteroid(self):
        new_asteroid = Asteroid( self.parent.scale, self.parent.background )
        self.parent.add_widget(new_asteroid)
        self.parent.enemyList.append(new_asteroid)
        
    def spawn_powerup(self):
        new_powerup = Powerup (self.parent.scale, self.parent.background)
        self.parent.add_widget(new_powerup)
        self.parent.powerupList.append(new_powerup)
        
    def update(self):
        if self.debug and random.uniform(0, 100) <= 10:
            self.spawn_powerup()
            
        if random.uniform(0, 100) <= 3:
            self.spawn_asteroid()
            
        if random.uniform(0, 100) <= 0.1:
            self.spawn_powerup()