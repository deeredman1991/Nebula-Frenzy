from Sprite import Sprite

class PlayerShip(Sprite):
    def __init__(self, scale, background=None, **kwargs):
        super(PlayerShip, self).__init__( scale*0.75, center=(background.width/2, background.height/2), source='images/PlayerShip1.png')
        
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        
        self.firerate = 10 #less is faster
        self.lazercooldown = 1
        self.max_shots = 3
        
        self._score = 0
        self._metal = 0
        
        self.active_powerups = {}
        
    @property
    def score(self):
        return self._score
        
    @score.setter
    def score(self, value):
        self._score = value
        self.parent.score_label.update()
        
    @property
    def metal(self):
        return self._metal
        
    @metal.setter
    def metal(self, value):
        self._metal = value
        print(self._metal)
        #self.parent.metal_label.update()
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.x < 0:
            self.x = 0
        elif self.x > self.parent.background.width-self.width:
            self.x = self.parent.background.width-self.width
        if self.y < 0:
            self.y = 0
        elif self.y > self.parent.background.height-self.height:
            self.y = self.parent.background.height-self.height
            
        for k, v in self.active_powerups.copy().iteritems():
            v.update()
            if v.timer <= 0:
                del self.active_powerups[k]
                
class PlayerLazer(Sprite):
    def __init__(self, scale, player=None, **kwargs):
        super(PlayerLazer, self).__init__( scale, pos=player.pos, source='images/BlueLazer.png')
        self.y += player.height
        self.x = player.x + player.width*0.15
        
        self.destroy = False
        self.collision = False
        
        self.speed = 6
        
    def update(self):
        self.y += self.speed
        
        if self.y >= self.parent.background.height:
            self.destroy = True
        
        for enemy in self.parent.enemyList:
            if self.x >= enemy.x-10 and self.right <= enemy.right+10 and self.y >= enemy.y-10 and self.top <= enemy.top+10:
                self.collision = True
                enemy.on_killed()
                enemy.collision = True
        
        if self.collision == True or self.destroy:
            self.parent.projectileList.remove(self)
            if self.collision:
                #Play Animation
                pass
            self.parent.remove_widget(self)