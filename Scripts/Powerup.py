import random

from Sprite import Sprite

class Powerup(Sprite):
    def __init__(self, scale, background=None, **kwargs):
        
        if random.randint(1,100) < 5:
            self.omnipowerup = True
        else:
            self.omnipowerup = False
            
        if self.omnipowerup == True:
            self.animspeed = 10
        else:
            self.animspeed = random.randint(5,15)
            
        self.animframe = 1
        self.framecount = 1
        self.totalPowerupTypes = 6
        
        self.powerupID = random.randint(1,self.totalPowerupTypes)
        super(Powerup, self).__init__(scale*0.75, source='images/Powerup{}-1.png'.format(self.powerupID), **kwargs)
        
        self.pos = (random.randint(0, int(background.width-self.width)), int(background.height))
        
        self.speed = random.uniform(3, 5)
        self.velocity_x = random.uniform(-self.speed*0.1, self.speed*0.1)
        self.velocity_y = self.speed
        
        self.collision = False
        
    def animate(self):
        self.animframe += 1
        if self.animframe > 4:
            self.animframe = 1
        if self.omnipowerup == True:
            self.powerupID = random.randint(1,self.totalPowerupTypes)
        self.source = 'images/Powerup{}-{}.png'.format(self.powerupID,self.animframe)
    
    def update(self):
        self.x -= self.velocity_x
        self.y -= self.velocity_y
    
        self.framecount += 1
        if self.framecount == self.animspeed:
            self.framecount = 1
            self.animate()
            
        if self.y < -self.height:
            self.collision = True
            
        player = self.parent.player
        if self.x >= player.x-10 and self.right <= player.right+10 and self.y >= player.y-10 and self.top <= player.top+10:
            self.collision = True
            player.active_powerups[self.powerupID] = ActivePowerup(self.powerupID, self.parent.player)
            
        if self.collision == True:
            self.parent.powerupList.remove(self)
            self.parent.remove_widget(self)
            
class ActivePowerup(object):
    def __init__(self, powerupID, player, timer=1):
        self.player = player
        self.powerupID = powerupID
        self.timer = timer
        
        self.tripped = False
        
    def update(self):
        #Activate Powerups
        if self.powerupID == 1: #Green
            if self.tripped == False:
                self.player.max_shots = 1000
                self.player.firerate -= 2 #lower numbers are faster
                self.timer = 480
                self.tripped = True
        elif self.powerupID == 2: #Red
            print("Powerup ID {} not implimented.".format(self.powerupID))
        elif self.powerupID == 3: #Blue
            print("Powerup ID {} not implimented.".format(self.powerupID))
        elif self.powerupID == 4: #Yellow
            print("Powerup ID {} not implimented.".format(self.powerupID))
        elif self.powerupID == 5: #Purple
            print("Powerup ID {} not implimented.".format(self.powerupID))
        elif self.powerupID == 6: #Pink
            print("Powerup ID {} not implimented.".format(self.powerupID))
        else:
            print("PowerupID {} has no activate condition see 'ActivePowerup' class.".format(self.powerupID))
        self.timer -= 1
        
        #Deactivate Powerups
        if self.timer <= 0:
            if self.powerupID == 1:
                self.player.max_shots = 3
                self.player.firerate += 2 #higher numbers are slower
            elif self.powerupID == 2:
                print("Powerup ID {} no deactivate logic.".format(self.powerupID))
            elif self.powerupID == 3:
                print("Powerup ID {} no deactivate logic.".format(self.powerupID))
            elif self.powerupID == 4:
                print("Powerup ID {} no deactivate logic.".format(self.powerupID))
            elif self.powerupID == 5:
                print("Powerup ID {} no deactivate logic.".format(self.powerupID))
            elif self.powerupID == 6:
                print("Powerup ID {} no deactivate logic.".format(self.powerupID))
            else:
                print("PowerupID {} has no deactivate condition see 'ActivePowerup' class.".format(self.powerupID))
            