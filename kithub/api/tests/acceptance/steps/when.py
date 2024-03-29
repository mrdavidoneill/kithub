import string
import json
from behave import when
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from utils import JSON_CONTENT, get_bagtype_by_kind, get_item_by_key


@when(
    'I create a "{model}" called "{name}" with quantity "{quantity:Number}" and description "{description}"'
)
def create_model_with_quantity_and_description(
    context, model, name, quantity, description
):

    if model == "part":

        payload = {
            "name": name,
            "description": f"A description of {name}",
            "quantity": quantity,
        }
    else:
        payload = {"kind": name, "quantity": quantity}

    context.response = context.test.client.post(reverse(f"{model}-list"), payload)


@when('I create a "{model}" called "{name}" with quantity "{quantity:Number}"')
def create_model_with_quantity(context, model, name, quantity):

    if model == "part":

        payload = {
            "name": name,
            "description": f"A description of {name}",
            "quantity": quantity,
        }
    else:
        payload = {"kind": name, "quantity": quantity}

    context.response = context.test.client.post(reverse(f"{model}-list"), payload)


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


@when('I read "{model}" with "{key}" "{value}"')
def read_model_by_key_value(context, model, value, key):
    items = context.test.client.get(reverse(f"{model}-list")).data
    item = get_item_by_key(items, value, key)
    context.response = context.test.client.get(
        reverse(f"{model}-detail", args=(item["id"],))
    )
    print(f"parts::: {context.response.data}")
    print(f"purchases::: {context.response.data['purchases']}")


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
            content_type=JSON_CONTENT,
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
            content_type=JSON_CONTENT,
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
            content_type=JSON_CONTENT,
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


@when('I request potential bags of "{bagtype}"')
def request_potential_bags(context, bagtype):
    bagtypes = context.test.client.get(reverse("bagtype-list")).data
    print(f"bagtypes: {bagtypes}")
    bagtype = get_item_by_key(bagtypes, bagtype, "kind")
    print(f"bagtype: {bagtype}")
    context.response = context.test.client.get(
        reverse("potentialbags", args=(bagtype["id"],))
    )

    print(context.response)
    print(context.response.data)


@when("I request unfinished bags")
def request_unfinished_bags(context):
    print("HELLO")
    context.response = context.test.client.get(reverse("allunfinishedbags"))
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


@when('I divide off "{quantity:Number}" of the first bag')
def divide_bag(context, quantity):
    bags = context.test.client.get(reverse("bag-list")).data
    data = {"bag": bags[0]["id"], "quantity": quantity}
    context.response = context.test.client.put(
        reverse("dividebag"),
        data=json.dumps(data, cls=DjangoJSONEncoder),
        content_type=JSON_CONTENT,
    )


@when('I divide off "{quantity:Number}" of the first kit')
def divide_kit(context, quantity):
    kits = context.test.client.get(reverse("kit-list")).data
    data = {"kit": kits[0]["id"], "quantity": quantity}
    context.response = context.test.client.put(
        reverse("dividekit"),
        data=json.dumps(data, cls=DjangoJSONEncoder),
        content_type=JSON_CONTENT,
    )


@when('I request the ingredients of bagtype "{bagtype}"')
def request_bag_ingredients(context, bagtype):
    bagtypes = context.test.client.get(reverse("bagtype-list")).data
    print(f"bagtypes: {bagtypes}")
    bagtype = get_item_by_key(bagtypes, bagtype, "kind")
    print(f"bagtype: {bagtype}")
    context.response = context.test.client.get(
        reverse("bagtype-detail", args=(bagtype["id"],))
    )

    print(context.response)
    print(context.response.data)
