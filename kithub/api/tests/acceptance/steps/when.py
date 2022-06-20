import json
from behave import when
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from utils import get_bagtype_by_kind


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


@when('I create "{quantity}" "{model}" of "{bagtype}" kind')
def create_model(context, quantity, model, bagtype):

    bagtypes = context.test.client.get(reverse("bagtype-list")).data

    if model == "bag":
        payload = {
            "name": "",
            "quantity": int(quantity),
            "complete": False,
            "kind": get_bagtype_by_kind(bagtypes, bagtype)["id"],
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
            "quantity": row["quantity"],
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


@when('I delete the first "{model}"')
def delete_first_model(context, model):
    context.response = context.test.client.get(reverse(f"{model}-list"))

    context.response = context.test.client.delete(
        reverse(f"{model}-detail", args=(context.response.data[0]["id"],))
    )
    print(context.response)
    print(context.response.data)
