from behave import given
from django.urls import reverse
from utils import get_part_by_name, get_bagtype_by_kind


@given("this step exists")
def step_exists(context):
    pass


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
                "quantity": row["quantity"],
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


@given('a bag type "{name}" with parts list of')
def create_specific_bagtype(context, name):
    bagtype = context.test.client.post(
        reverse("bagtype-list"),
        {"kind": name},
    )
    print(f"bagtype.data {bagtype.data}")

    parts = context.test.client.get(reverse("part-list")).data

    print(parts)

    for row in context.table:
        context.response = context.test.client.post(
            reverse("bagingredient-list"),
            {
                "name": name,
                "bagtype": bagtype.data["id"],
                "quantity": row["quantity"],
                "part": get_part_by_name(parts, row["part"]),
            },
        )


@given('I read all "{model}"')
def read_models(context, model):
    context.response = context.test.client.get(reverse(f"{model}-list"))
