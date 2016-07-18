from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock

from Background import Background
from Player import PlayerShip
from GUI import DPad
from GUI import LazerButton
from GUI import Score
from MultiSound import MultiSound
from Spawner import Spawner

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
        
        self.score_label = Score()
        self.add_widget(self.score_label)
        self.score_label.update()
        
        
        self.projectileList = []
        
        self.standby_enemyList = []
        self.enemyList = []
        
        self.dpad = DPad ( self.scale, self.player, pos=self.background.pos )
        self.add_widget( self.dpad )
        
        self.lazersound = MultiSound('audio/lazer.wav', 6)
        
        self.lazerbutton = LazerButton ( self.scale, self.background, self.player )
        self.add_widget ( self.lazerbutton )
        
        self.powerupList = []
        
        self.spawner = Spawner()
        self.add_widget(self.spawner)
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        
    def update(self, dt):
        self.background.update()
        self.player.update()
        self.lazerbutton.update()
        
        for projectile in self.projectileList:
            projectile.update()
            
        for enemy in self.enemyList:
            enemy.update()
            
        for powerup in self.powerupList:
            powerup.update()
            
        self.spawner.update()