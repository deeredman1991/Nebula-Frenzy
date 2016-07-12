from kivy.uix.image import Image

class Sprite(Image):
    def __init__(self, scale, **kwargs):
        super(Sprite, self).__init__(allow_stretch = True, **kwargs)
        self.texture.mag_filter = 'nearest'
        w, h = self.texture_size
        self.size = (scale * w, scale * h)