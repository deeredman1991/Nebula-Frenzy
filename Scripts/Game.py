from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock

from Scripts.Background import Background
from Scripts.Player import PlayerShip
from Scripts.GUI import DPad
from Scripts.GUI import LazerButton
from Scripts.GUI import Score
from Scripts.GUI import ShieldGUI
from Scripts.GUI import MetalGUI
from Scripts.GUI import HullGUI
from Scripts.MultiSound import MultiSound
from Scripts.Spawner import Spawner

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
        
        self.metal_label = MetalGUI(self.scale, self.background)
        self.add_widget(self.metal_label)
        self.metal_label.update()
        
        self.hull_gui = HullGUI(self.background)
        self.add_widget(self.hull_gui)
        self.hull_gui.update()
        
        self.shield_gui = ShieldGUI()
        self.add_widget(self.shield_gui)
        self.shield_gui.on_start()
        self.shield_gui.update()
        
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