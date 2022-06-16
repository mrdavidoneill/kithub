from behave import then


@then("I should see the behave tests run")
def is_running(context):
    pass


@then("django_ready should be called")
def django_context(context):
    assert context.django
