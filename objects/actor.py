import objects.movable


class Actor(objects.movable.Movable):
    def update(self, window, delta_time):
        super().update(window, delta_time)
