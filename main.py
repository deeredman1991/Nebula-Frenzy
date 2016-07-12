from kivy.app import App
from kivy.core.window import Window
from Scripts.Game import Game
import random

class GameApp(App):
    def build(self):
        Window.size = (random.randint(500, 1000), random.randint(500, 1000))
        #Window.size = (300, 500)
        self.title = 'Nebula Frenzy'
        #self.icon = 'images/icon.png'
        return Game()
        
if __name__ == "__main__":
    GameApp().run()