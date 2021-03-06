from kivy.uix.widget import Widget
import random

from Scripts.Powerup import Powerup
from Scripts.Asteroid import Asteroid

class Spawner(Widget):
    def __init__(self, **kwargs):
        super(Spawner, self).__init__(**kwargs)
        self.powerup_debug = False
    
    def spawn_asteroid(self):
        standby_asteroid = len(self.parent.standby_enemyList)
        if standby_asteroid > 0:
            recycled_asteroid = self.parent.standby_enemyList.pop(random.randint(0, standby_asteroid-1))
            recycled_asteroid.on_start()
            self.parent.add_widget(recycled_asteroid)
            self.parent.enemyList.append(recycled_asteroid)
        else:
            new_asteroid = Asteroid( self.parent.scale, self.parent.background )
            self.parent.add_widget(new_asteroid)
            self.parent.enemyList.append(new_asteroid)
        
    def spawn_powerup(self):
        new_powerup = Powerup (self.parent.scale, self.parent.background)
        self.parent.add_widget(new_powerup)
        self.parent.powerupList.append(new_powerup)
        
    def update(self):
        if self.powerup_debug and random.uniform(0, 100) <= 10:
            self.spawn_powerup()
            
        if random.uniform(0, 100) <= 3:
            self.spawn_asteroid()
            
        if random.uniform(0, 100) <= 0.1:
            self.spawn_powerup()