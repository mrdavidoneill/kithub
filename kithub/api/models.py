from django.db import models


class Kit(models.Model):
    """Kit Model
    Defines attributes of a DIY Kit"""

    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)  # 0 to 2147483647
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class KitType(models.Model):
    """Kit Type Model
    Defines attributes of a DIY Kit type"""

    kind = models.CharField(max_length=255)

    def __str__(self):
        return self.name
