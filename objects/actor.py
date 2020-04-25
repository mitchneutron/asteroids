from objects.movable import Movable


class Actor(Movable):
    def update(self, window, delta_time):
        super().update(window, delta_time)
