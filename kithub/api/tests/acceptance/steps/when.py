from behave import when
from django.urls import reverse


@when('I run "python manage.py behave"')
def run_command(context):
    pass


@when('I create a "{model}" called "{name}"')
def create_model(context, model, name):
    context.response = context.test.client.post(
        reverse(f"{model}-list"),
        {
            "name": name,
            "description": f"A description of {name}",
        },
    )


@when('I read a "{model}" called "{name}"')
def read_model(context, model, name):
    context.response = context.test.client.get(reverse(f"{model}-detail", args=(1,)))


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
