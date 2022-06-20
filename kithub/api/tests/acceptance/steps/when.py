import string
import json
from behave import when
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from utils import get_bagtype_by_kind, get_item_by_key


@when('I run "python manage.py behave"')
def run_command(context):
    pass


@when('I create a "{model}" called "{name}"')
def create_model(context, model, name):

    if model == "part":

        payload = {"name": name, "description": f"A description of {name}"}
    else:
        payload = {"kind": name}

    context.response = context.test.client.post(reverse(f"{model}-list"), payload)


@when(
    'I create "{quantity:Number}" "{model}" of "{kind}" "{kindmodel}" with name "{name}"'
)
def create_model_with_name(context, quantity, model, kind, kindmodel, name):

    kinds = context.test.client.get(reverse(f"{kindmodel}-list")).data

    if model == "bag" or model == "kit":
        payload = {
            "name": name,
            "quantity": int(quantity),
            "complete": False,
            "kind": get_item_by_key(kinds, kind, key="kind")["id"],
        }
    else:
        payload = {"kind": name}

    context.response = context.test.client.post(reverse(f"{model}-list"), payload)


@when('I create "{quantity}" "{model}" of "{kind}" "{kindmodel}"')
def create_model(context, quantity, model, kind, kindmodel):

    kinds = context.test.client.get(reverse(f"{kindmodel}-list")).data

    if model == "bag" or model == "kit":
        payload = {
            "name": "",
            "quantity": int(quantity),
            "complete": False,
            "kind": get_item_by_key(kinds, kind, key="kind")["id"],
        }
    else:
        payload = {"kind": name}

    context.response = context.test.client.post(reverse(f"{model}-list"), payload)


@when('I read the first "{model}"')
def read_first_model(context, model):
    context.response = context.test.client.get(reverse(f"{model}-list"))

    context.response = context.test.client.get(
        reverse(f"{model}-detail", args=(context.response.data[0]["id"],))
    )


@when('I read all "{model}"')
def read_models(context, model):
    context.response = context.test.client.get(reverse(f"{model}-list"))
    print(f"All {model}: {context.response.data}")


@when('I update a "{model}" called "{name}"')
def read_model(context, model, name):
    context.response = context.test.client.put(
        reverse(f"{model}-list", args=(name,)),
        {
            "name": name,
            "description": f"A description of {name}",
        },
    )


@when("I update the first part as follows")
def update_part(context):
    for row in context.table:
        data = {
            "name": row["name"],
            "description": row["description"],
            "quantity": int(row["quantity"]),
        }
        context.response = context.test.client.put(
            reverse(
                "part-detail",
                kwargs={
                    "pk": context.response.data[0]["id"],
                },
            ),
            data=json.dumps(data, cls=DjangoJSONEncoder),
            content_type="application/json",
        )


@when("I update the first bag as follows")
def update_bag(context):
    bagtypes = context.test.client.get(reverse("bagtype-list")).data
    context.response = context.test.client.get(reverse("bag-list"))

    for row in context.table:
        data = {
            "name": row["name"],
            "kind": get_bagtype_by_kind(bagtypes, row["kind"])["id"],
            "complete": bool(row["complete"]),
            "quantity": int(row["quantity"]),
        }
        context.response = context.test.client.put(
            reverse(
                "bag-detail",
                kwargs={
                    "pk": context.response.data[0]["id"],
                },
            ),
            data=json.dumps(data, cls=DjangoJSONEncoder),
            content_type="application/json",
        )


@when("I update the first kit as follows")
def update_kit(context):
    kittypes = context.test.client.get(reverse("kittype-list")).data
    context.response = context.test.client.get(reverse("kit-list"))

    for row in context.table:
        data = {
            "name": row["name"],
            "kind": get_item_by_key(kittypes, row["kind"], "kind")["id"],
            "complete": bool(row["complete"]),
            "quantity": int(row["quantity"]),
        }
        context.response = context.test.client.put(
            reverse(
                "kit-detail",
                kwargs={
                    "pk": context.response.data[0]["id"],
                },
            ),
            data=json.dumps(data, cls=DjangoJSONEncoder),
            content_type="application/json",
        )


@when('I delete the first "{model}"')
def delete_first_model(context, model):
    context.response = context.test.client.get(reverse(f"{model}-list"))

    context.response = context.test.client.delete(
        reverse(f"{model}-detail", args=(context.response.data[0]["id"],))
    )
    print(context.response)
    print(context.response.data)


@when('I request a partlist for "{quantity:Number}" of "{kittype}"')
def request_partslist(context, quantity, kittype):
    kittypes = context.test.client.get(reverse("kittype-list")).data
    print(f"kittypes: {kittypes}")
    kittype = get_item_by_key(kittypes, kittype, "kind")
    print(f"kittype: {kittype}")
    context.response = context.test.client.get(
        reverse("partstobuyforkit", args=(kittype["id"], quantity))
    )

    print(context.response)
    print(context.response.data)


@when('I request potential kits of "{kittype}"')
def request_potential_kits(context, kittype):
    kittypes = context.test.client.get(reverse("kittype-list")).data
    print(f"kittypes: {kittypes}")
    kittype = get_item_by_key(kittypes, kittype, "kind")
    print(f"kittype: {kittype}")
    context.response = context.test.client.get(
        reverse("potentialkits", args=(kittype["id"],))
    )

    print(context.response)
    print(context.response.data)


@when('I create a kit type "{name}" with bags list of')
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
