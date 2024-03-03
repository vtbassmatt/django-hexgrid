from django.db import models


_DIRECTION_VECTOR = (
    # four o'clock is to the southeast, then proceed counterclockwise
    (+1, 0, -1), (+1, -1, 0), (0, -1, +1), 
    (-1, 0, +1), (-1, +1, 0), (0, +1, -1),
)

class HexCell(models.Model):
    class Direction(models.IntegerChoices):
        TWO_OCLOCK = 1
        FOUR_OCLOCK = 0
        SIX_OCLOCK = 5
        EIGHT_OCLOCK = 4
        TEN_OCLOCK = 3
        TWELVE_OCLOCK = 2

    q = models.IntegerField()
    r = models.IntegerField()
    s = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(s=models.F('q') * -1 - models.F('r')),
                name='coord_invariant',
            ),
            models.UniqueConstraint(
                fields=['q', 'r', 's'],
                name='unique_coords',
            )
        ]

    def __str__(self):
        return f"({self.q}, {self.r}, {self.s})"

    @classmethod
    def from_axial(cls, q: int, r: int):
        return cls(q=q, r=r, s=-q-r)

    @classmethod
    def get_or_create_origin(cls):
        return cls._default_manager.get_or_create(q=0, r=0, s=0)

    def get_or_create_neighbor(self, direction: Direction):
        deltas = _DIRECTION_VECTOR[direction.value]
        return self._meta.default_manager.get_or_create(
            q=self.q + deltas[0],
            r=self.r + deltas[1],
            s=self.s + deltas[2],
        )

    def get_neighbors(self):
        return self._meta.default_manager.filter(
            # find our neighbors
            q__in=[self.q-1, self.q, self.q+1],
            r__in=[self.r-1, self.r, self.r+1],
            s__in=[self.s-1, self.s, self.s+1],
        ).exclude(
            # but exclude the exact match (self)
            q=self.q, r=self.r, s=self.s
        )
