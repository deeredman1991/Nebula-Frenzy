from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from Sprite import Sprite
from Player import PlayerLazer

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
        
        self.lazers_on = False
        
        self.timer = 0
        
        '''
        with self.canvas:
            Color(0.5,1,1,1)
            Rectangle(pos = self.pos, size = self.size)
        #'''
        
    def _reset_lazer_count(self, *ignore):
        self.lazercount = 0
        
    def _on_joy_button_down(self, window, stickid, buttonid):
        if buttonid == 0:
            self.lazers_on = True
        
    def _on_joy_button_up(self, window, stickid, buttonid):
        self.lazers_on = False
    
    def on_touch_down(self, touch):
        tx, ty = touch.pos
        if tx  <= self.x+self.width and ty <= self.y+self.height and tx >= self.x and ty >= self.y:
            self.lazers_on = True
            
    def on_touch_up(self, touch):
        self.lazers_on = False
        
    def spawn_lazer(self, *ignore):
        if self.lazercount == 0:
            Clock.schedule_once(self._reset_lazer_count, self.parent.player.lazercooldown)
        if self.lazercount < self.parent.player.max_shots:
            self.lazercount += 1
            self.parent.lazersound.play()
            new_projectile = PlayerLazer(self.parent.scale, self.parent.player)
            self.parent.add_widget(new_projectile)
            self.parent.projectileList.append(new_projectile)
            
    def update(self):
    
        if self.lazers_on and self.timer % self.player.firerate == 0:
            self.spawn_lazer()
    
        self.timer += 1
        if self.timer >= 1000:
            self.timer = 0
            
            
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
        else:
            self.on_touch_up()
    
    def on_touch_down(self, touch):
        self.touch_handler(touch)
        
    def on_touch_move(self, touch):
        self.touch_handler(touch)
        
    def on_touch_up(self, *ignore):
        self.player.velocity_x = 0
        self.player.velocity_y = 0