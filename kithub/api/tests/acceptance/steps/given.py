from behave import given
from django.urls import reverse


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
