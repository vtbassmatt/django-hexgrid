from django.db import models


class HexCell(models.Model):
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
