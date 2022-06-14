from django.db import models


class KitType(models.Model):
    """Kit Type Model
    Defines attributes of a DIY Kit type"""

    kind = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.kind


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

    kind = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.kind


class Bag(models.Model):
    """Bag Model
    Defines attributes of a Bag"""

    name = models.CharField(max_length=255, default="", blank=True)
    quantity = models.PositiveIntegerField(default=0)  # 0 to 2147483647
    complete = models.BooleanField(default=False)
    kind = models.ForeignKey(BagType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class KitIngredient(models.Model):
    """Kit Ingredient Model
    Represents a Bag to be placed in a Kit"""

    name = models.CharField(max_length=4)
    kittype = models.ForeignKey(
        KitType, related_name="ingredients", on_delete=models.CASCADE
    )
    bagtype = models.ForeignKey(
        BagType, related_name="needed", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()  # 0 to 2147483647

    class Meta:
        unique_together = [["name", "kittype"]]

    def __str__(self):
        return f"{self.name} in {self.bagtype.kind}"


class Part(models.Model):
    """Part Model
    Defines attributes of a Part"""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)  # 0 to 2147483647

    def __str__(self):
        return self.name


class BagIngredient(models.Model):
    """Bag Ingredient Model
    Represents a Part to be placed in a Bag"""

    name = models.CharField(max_length=4)
    bagtype = models.ForeignKey(
        BagType, related_name="ingredients", on_delete=models.CASCADE
    )
    part = models.ForeignKey(Part, related_name="needed", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # 0 to 2147483647

    class Meta:
        unique_together = [["name", "bagtype"]]

    def __str__(self):
        return f"{self.name} in {self.bagtype.kind}"


class Purchase(models.Model):
    """Purchase Model
    Defines attributes of a Part Purchase"""

    date = models.DateField()
    shop = models.CharField(max_length=255)
    shop_part_no = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=5)
    quantity = models.PositiveIntegerField(default=0)  # 0 to 2147483647
    part = models.ForeignKey(Part, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}: {self.part.name} x {self.quantity} @ {self.price} GBP"
