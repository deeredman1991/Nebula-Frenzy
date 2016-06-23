from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.clock import Clock

from kivy.graphics import Color, Rectangle, Rotate
from kivy.graphics.context_instructions import PushMatrix, PopMatrix#, Rotate


import random



class Sprite(Image):
    def __init__(self, scale, **kwargs):
        super(Sprite, self).__init__(allow_stretch = True, **kwargs)
        self.texture.mag_filter = 'nearest'
        w, h = self.texture_size
        self.size = (scale * w, scale * h)
        
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
    
class AsteroidSpawner(Widget):
    def spawn_asteroid(self, *ignore):
        new_asteroid = Asteroid( self.parent.scale, self.parent.background )
        self.parent.add_widget(new_asteroid)
        self.parent.enemyList.append(new_asteroid)
    
class PlayerShip(Sprite):
    def __init__(self, scale, background=None, **kwargs):
        super(PlayerShip, self).__init__( scale*0.75, center=(background.width/2, background.height/2), source='images/PlayerShip1.png')
        
        self.speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        
        self.firerate = 0.2
        self.lazercooldown = 1
        self.max_shots = 3
        
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
            if  self.x >= enemy.x-10 and self.right <= enemy.right+10 and self.y >= enemy.y-10 and self.top <= enemy.top+10:
                self.collision = True
                enemy.collision = True
        
        if self.collision == True or self.destroy:
            self.parent.projectileList.remove(self)
            if self.collision:
                #Play Animation
                pass
            self.parent.remove_widget(self)
        
class LazerButton(Widget):
    def __init__(self, scale, background, player, **kwargs):
        super(LazerButton, self).__init__(**kwargs)
        
        Window.bind(on_joy_button_down=self._on_joy_button_down)
        Window.bind(on_joy_button_up=self._on_joy_button_up)
        
        self.image = Sprite(scale*1.5, source = 'images/LazerButton.png')
        
        self.size = self.image.size
        
        self.right = self.image.right = background.right-30*scale
        self.y = self.image.y = 30*scale
        
        self.add_widget(self.image)
        
        self.player = player
        
        self.lazercount = 0
        
        '''
        with self.canvas:
            Color(0.5,1,1,1)
            Rectangle(pos = self.pos, size = self.size)
        #'''
        
    def _reset_lazer_count(self, *ignore):
        self.lazercount = 0
        
    def _on_joy_button_down(self, window, stickid, buttonid):
        if buttonid == 0:
            self.spawn_lazer()
            Clock.schedule_interval(self.spawn_lazer, self.player.firerate)
        
    def _on_joy_button_up(self, window, stickid, buttonid):
        Clock.unschedule(self.spawn_lazer, all=True)
    
    def on_touch_down(self, touch):
        tx, ty = touch.pos
        if tx  <= self.x+self.width and ty <= self.y+self.height and tx >= self.x and ty >= self.y:
            self.spawn_lazer()
            Clock.schedule_interval(self.spawn_lazer, self.player.firerate)
            
    def on_touch_up(self, touch):
        Clock.unschedule(self.spawn_lazer, all=True)
        
    def spawn_lazer(self, *ignore):
        if self.lazercount == 0:
            Clock.schedule_once(self._reset_lazer_count, self.parent.player.lazercooldown)
        if self.lazercount < self.parent.player.max_shots:
            self.lazercount += 1
            new_projectile = PlayerLazer(self.parent.scale, self.parent.player)
            self.parent.add_widget(new_projectile)
            self.parent.projectileList.append(new_projectile)
            
    def update(self):
        pass
        
class DPad(Widget):
    def __init__(self, scale, player, **kwargs):
        super(DPad, self).__init__(**kwargs)
        
        #Window.bind(on_joy_axis=self._on_joy_axis)
        Window.bind(on_joy_hat=self._on_joy_hat)
        
        self.image = Sprite(scale*1.5, source = 'images/DPad.png')
        self.add_widget(self.image)
        
        self.size = self.image.size
        
        self.player = player
        
        self.deadzone = 0.15
        
    '''
    def _on_joy_axis(self, window, stickid, axisid, value):
        if value > 1600 or value < -1600:
            print('StickID: {} | AxisID: {} | Value: {}'.format(stickid, axisid, value))
            
    '''
            
    def _on_joy_hat(self, window, stickid, hatid, value):
        vx, vy = value
        self.player.velocity_x = self.player.speed*vx
        self.player.velocity_y = self.player.speed*vy
    
    
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
        self.image.height = int(self.image.width*4)
        self.image.width = self.image.width+4
        self.image.x = -2
        self.add_widget(self.image)
        
        self.image_dupe = Image(allow_stretch=True, keep_ratio = False, source=source)
        self.image_dupe.size = Window.size
        self.image_dupe.height = int(self.image_dupe.width*4)
        self.image_dupe.width = self.image_dupe.width+4
        self.image_dupe.x = -2
        self.image_dupe.y = self.image.height-2
        self.add_widget(self.image_dupe)
        
    def update(self):
        self.image.y -= 4 * self.parent.scale
        self.image_dupe.y -= 4 * self.parent.scale
        
        if self.image.top <= 0:
            self.image.y = 0
            self.image_dupe.y = self.image.height-2
    
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
        
        #self.projectiletest = PlayerLazer( self.scale, self.player)
        #self.add_widget(self.projectiletest)
        
        self.projectileList = []
        
        #self.asteroidtest = Asteroid( self.scale, background=self.background )
        #self.add_widget(self.asteroidtest)
        
        self.asteroidSpawner = AsteroidSpawner()
        self.add_widget(self.asteroidSpawner)
        
        self.enemyList = []
        
        self.dpad = DPad ( self.scale, self.player, pos=self.background.pos )
        self.add_widget( self.dpad )
        
        self.lazerbutton = LazerButton ( self.scale, self.background, self.player )
        self.add_widget ( self.lazerbutton )
        
        Clock.schedule_interval(self.update, 1.0/60.0)
        Clock.schedule_interval(self.asteroidSpawner.spawn_asteroid, 1.0/10)
        
    def update(self, dt):
        self.background.update()
        self.player.update()
        self.lazerbutton.update()
        
        for projectile in self.projectileList:
            projectile.update()
            
        for enemy in self.enemyList:
            enemy.update()

class GameApp(App):
    def build(self):
        Window.size = (random.randint(500, 1000), random.randint(500, 1000))
        #Window.size = (300, 500)
        self.title = 'Nebula Frenzy'
        #self.icon = 'images/icon.png'
        return Game()
        
if __name__ == "__main__":
    GameApp().run()