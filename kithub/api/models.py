from django.db import models
import string
from random import randint


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

    def decrement(self, quantity=1):
        """Decrease quantity by quantity passed, or 1"""
        self.quantity -= quantity
        self.save()

    def increment(self, quantity=1):
        """Increase quantity by quantity passed, or 1"""
        self.quantity += quantity
        self.save()

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

    def decrement(self, quantity=1):
        """Decrease quantity by quantity passed, or 1"""
        self.quantity -= quantity
        self.save()

    def increment(self, quantity=1):
        """Increase quantity by quantity passed, or 1"""
        self.quantity += quantity
        self.save()

    def add_part(self, part_letter):
        """Add part into bag, by changing bag name"""
        index = string.ascii_letters.index(part_letter.lower())
        new_bag_name = list(self.name)
        new_bag_name[index] = part_letter
        new_bag_name = "".join(new_bag_name)
        self.name = new_bag_name
        self.save()

    def remove_part(self, part_letter):
        """Remove part into bag, by changing bag name"""
        index = self.name.lower().index(part_letter.lower())
        new_bag_name = list(self.name)
        new_bag_name[index] = " "
        new_bag_name = "".join(new_bag_name)
        self.name = new_bag_name
        self.save()

    def __str__(self):
        return f"{self.kind} - {self.name} x {self.quantity}"


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
        return f"{self.name}: {self.bagtype} x {self.quantity} in {self.kittype.kind}"


class Part(models.Model):
    """Part Model
    Defines attributes of a Part"""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)  # 0 to 2147483647

    def decrement(self, quantity=1):
        """Decrease quantity by quantity passed, or 1"""
        self.quantity -= quantity
        self.save()

    def increment(self, quantity=1):
        """Increase quantity by quantity passed, or 1"""
        self.quantity += quantity
        self.save()

    def __str__(self):
        return f"{self.name } {self.quantity} pcs"


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
    part = models.ForeignKey(Part, related_name="purchases", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}: {self.part.name} x {self.quantity} @ {self.price} GBP"


def create_parts(num=2):
    for i in range(num):
        part = Part.objects.create(
            name=f"PART{i + 1}",
            description=f"A part description for PART{i + 1}",
            quantity=100,
        )


def create_bagtypes(num=2):
    for i in range(num):
        bagtype = BagType.objects.create(kind=f"BAGTYPE{i + 1}")


def create_bagingredients(
    bagtype,
    num=2,
):
    parts = Part.objects.all()
    for i in range(num):
        bagtype_obj = BagType.objects.get(pk=bagtype)
        BagIngredient.objects.create(
            name=string.ascii_letters[i].upper(),
            bagtype=bagtype_obj,
            part=parts[i],
            quantity=randint(1, 50),
        )


def create_bags(kind, quantity=100, complete=False, name=None):

    ingredients = BagIngredient.objects.filter(bagtype=kind)

    kind = BagType.objects.get(pk=kind)

    if name is None:
        name = " " * len(ingredients)

    Bag.objects.create(kind=kind, quantity=quantity, complete=complete, name=name)


def create_kitingredients(
    kittype,
    num=2,
):
    bagtypes = BagType.objects.all()
    for i in range(num):
        kittype_obj = KitType.objects.get(pk=kittype)
        KitIngredient.objects.create(
            name=string.ascii_letters[i].upper(),
            kittype=kittype_obj,
            bagtype=bagtypes[i],
            quantity=randint(1, 50),
        )


def create_kittypes(num=2):
    for i in range(num):
        kittype = KitType.objects.create(kind=f"KITTYPE{i + 1}")


def delete_parts():
    print(f"Deleting parts:", end="")
    response = Part.objects.all().delete()
    print(f"{response} deleted")


def delete_bags():
    print(f"Deleting bags:", end="")
    response = Bag.objects.all().delete()
    print(f"{response} deleted")


def delete_bagtypes():
    print(f"Deleting bagtypes:", end="")
    response = BagType.objects.all().delete()
    print(f"{response} deleted")


def delete_kits():
    print(f"Deleting kits:", end="")
    response = Kit.objects.all().delete()
    print(f"{response} deleted")


def delete_kittypes():
    print(f"Deleting kittypes:", end="")
    response = KitType.objects.all().delete()
    print(f"{response} deleted")


def delete_bagingredients():
    print(f"Deleting bagingredients:", end="")
    response = BagIngredient.objects.all().delete()
    print(f"{response} deleted")


def delete_kitingredients():
    print(f"Deleting kitingredients:", end="")
    response = KitIngredient.objects.all().delete()
    print(f"{response} deleted")


def delete_purchases():
    print(f"Deleting purchases:", end="")
    response = Purchase.objects.all().delete()
    print(f"{response} deleted")


def delete_everything():
    delete_bagingredients()
    delete_kitingredients()
    delete_purchases()
    delete_parts()
    delete_bagtypes()
    delete_kittypes()
    delete_bags()
    delete_kits()


def create_kits(kind, quantity=100, complete=False, name=None):

    ingredients = KitIngredient.objects.filter(kittype=kind)

    kind = KitType.objects.get(pk=kind)

    if name is None:
        name = " " * len(ingredients)

    Kit.objects.create(kind=kind, quantity=quantity, complete=complete, name=name)
