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
        "Axial coordinates work like cubic, but the `s` is computed."
        return cls(q=q, r=r, s=-q-r)

    @classmethod
    def get_or_create_origin(cls):
        """
        Get or create the hex cell at (0,0,0).
        
        Like Django's get_or_create method, returns both the object
        and whether it's new. Does not save the new object!
        """
        return cls._default_manager.get_or_create(q=0, r=0, s=0)

    def get_or_create_neighbor(self, direction: Direction):
        """
        Get or create the hex cell neighboring this one.
        
        Like Django's get_or_create method, returns both the object
        and whether it's new. Does not save the new object!
        """
        deltas = _DIRECTION_VECTOR[direction.value]
        return self._meta.default_manager.get_or_create(
            q=self.q + deltas[0],
            r=self.r + deltas[1],
            s=self.s + deltas[2],
        )
    
    def get_neighbor_coords(self):
        """
        Gets the coordinates of all neighboring cells, whether or
        not they exist.
        """
        return {
            name: (
                self.q + _DIRECTION_VECTOR[HexCell.Direction[name]][0],
                self.r + _DIRECTION_VECTOR[HexCell.Direction[name]][1],
                self.s + _DIRECTION_VECTOR[HexCell.Direction[name]][2],
            )
            for name in HexCell.Direction.names
        }

    def get_neighbors(self):
        "Gets all the neighboring cells of this one as long as they exist."
        return self._meta.default_manager.filter(
            # find our neighbors
            q__in=[self.q-1, self.q, self.q+1],
            r__in=[self.r-1, self.r, self.r+1],
            s__in=[self.s-1, self.s, self.s+1],
        ).exclude(
            # but exclude the exact match (self)
            q=self.q, r=self.r, s=self.s
        )

    def distance_to(self, other: 'HexCell'):
        "Compute the distance between two cells."
        vector = (self.q - other.q, self.r - other.r, self.s - other.s)
        return max([abs(n) for n in vector])

    def is_origin(self):
        return self.q == 0 and self.r == 0 and self.s == 0