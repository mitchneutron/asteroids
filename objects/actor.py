from objects.drawable import Drawable


class Actor(Drawable):
    def get_actors(self):
        return [self]

    def update(self, screen):
        pass
