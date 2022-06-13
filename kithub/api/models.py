from django.db import models


class KitType(models.Model):
    """Kit Type Model
    Defines attributes of a DIY Kit type"""

    kind = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Kit(models.Model):
    """Kit Model
    Defines attributes of a DIY Kit"""

    name = models.CharField(max_length=255, default="", blank=True)
    quantity = models.PositiveIntegerField(default=0)  # 0 to 2147483647
    complete = models.BooleanField(default=False)
    kind = models.ForeignKey(KitType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BagType(models.Model):
    """Bag Type Model
    Defines attributes of a Bag type"""

    kind = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Bag(models.Model):
    """Bag Model
    Defines attributes of a Bag"""

    name = models.CharField(max_length=255, default="", blank=True)
    quantity = models.PositiveIntegerField(default=0)  # 0 to 2147483647
    complete = models.BooleanField(default=False)
    kind = models.ForeignKey(BagType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class KitContents(models.Model):
    """Kit Contents Model
    Represents a Bag placed in a Kit"""

    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bag.name} in {self.kit.name}"


class Part(models.Model):
    """Part Model
    Defines attributes of a Part"""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)  # 0 to 2147483647

    def __str__(self):
        return self.name


class BagContents(models.Model):
    """Bag Contents Model
    Represents a Part placed in a Bag"""

    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.part.name} in {self.bag.name}"


class Purchase(models.Model):
    """Purchase Model
    Defines attributes of a Part Purchase"""

    date = models.DateField()
    shop = models.CharField(max_length=255)
    shop_part_no = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=5)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
