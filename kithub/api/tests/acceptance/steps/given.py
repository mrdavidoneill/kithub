import string
from behave import given
from django.urls import reverse
from utils import get_part_by_name, get_bagtype_by_kind, get_item_by_key


@given('a part called "{name}"')
def create_part(context, name):
    context.response = context.test.client.post(
        reverse("part-list"),
        {
            "name": name,
            "description": f"A description of {name}",
        },
    )


@given("a set of specific parts")
def create_set_of_parts(context):
    for row in context.table:
        context.response = context.test.client.post(
            reverse("part-list"),
            {
                "name": row["name"],
                "description": row["description"],
                "quantity": int(row["quantity"]),
            },
        )


@given("a set of specific bags")
def create_set_of_bags(context):
    bagtypes = context.test.client.get(reverse("bagtype-list")).data

    for row in context.table:
        context.response = context.test.client.post(
            reverse("bag-list"),
            {
                "name": row["name"],
                "quantity": int(row["quantity"]),
                "complete": bool(row["complete"]),
                "kind": get_bagtype_by_kind(bagtypes, row["kind"])["id"],
            },
        )


@given("a set of specific kits")
def create_set_of_kits(context):
    kittypes = context.test.client.get(reverse("kittype-list")).data

    print(f"All kitypes: {kittypes}")

    for row in context.table:
        context.response = context.test.client.post(
            reverse("kit-list"),
            {
                "name": row["name"],
                "quantity": int(row["quantity"]),
                "complete": bool(row["complete"]),
                "kind": get_item_by_key(kittypes, row["kind"], "kind")["id"],
            },
        )


@given('a bag type "{name}" with parts list of')
def create_specific_bagtype(context, name):
    bagtype = context.test.client.post(
        reverse("bagtype-list"),
        {"kind": name},
    )
    print(f"bagtype.data {bagtype.data}")

    parts = context.test.client.get(reverse("part-list")).data

    print(parts)

    for index, row in enumerate(context.table):
        context.response = context.test.client.post(
            reverse("bagingredient-list"),
            {
                "name": string.ascii_letters[index].upper(),
                "bagtype": bagtype.data["id"],
                "quantity": int(row["quantity"]),
                "part": get_part_by_name(parts, row["part"])["id"],
            },
        )


@given('a kit type "{name}" with bags list of')
def create_specific_kittype(context, name):
    kittype = context.test.client.post(
        reverse("kittype-list"),
        {"kind": name},
    )
    print(f"kittype.data {kittype.data}")

    bagtypes = context.test.client.get(reverse("bagtype-list")).data

    print(bagtypes)

    for index, row in enumerate(context.table):
        context.response = context.test.client.post(
            reverse("kitingredient-list"),
            {
                "name": string.ascii_letters[index].upper(),
                "kittype": kittype.data["id"],
                "quantity": int(row["quantity"]),
                "bagtype": get_item_by_key(bagtypes, row["bagtype"], key="kind")["id"],
            },
        )


@given("a set of specific purchases")
def create_set_of_purchases(context):
    parts = context.test.client.get(reverse("part-list")).data

    print(f"All parts: {parts}")

    for row in context.table:
        context.response = context.test.client.post(
            reverse("purchase-list"),
            {
                "date": row["date"],
                "shop": row["shop"],
                "shop_part_no": row["shop_part_no"],
                "price": row["price"],
                "quantity": int(row["quantity"]),
                "part": get_item_by_key(parts, row["part"], "name")["id"],
            },
        )


@given('I read all "{model}"')
def read_models(context, model):
    context.response = context.test.client.get(reverse(f"{model}-list"))
