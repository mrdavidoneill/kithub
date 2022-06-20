from behave import register_type, then
import parse


@parse.with_pattern(r"\d+")
def parse_number(text):
    return int(text)


register_type(Number=parse_number)


@then("I should see the behave tests run")
def is_running(context):
    pass


@then("django_ready should be called")
def django_context(context):
    assert context.django


@then('I should see the "{key}" is "{value}"')
def see_key_value(context, key, value):
    response = context.response
    print(response.data)
    context.test.assertEqual(response.data[key], value)


@then('I should see the "{key}" is number "{value:Number}"')
def see_numeric_key_value(context, key, value):
    response = context.response
    print(response.data)
    context.test.assertEqual(response.data[key], value)


@then('the first item should have "{key}" equal to "{value}"')
def see_key_value_of_first(context, key, value):
    response = context.response
    print(response.data)
    context.test.assertEqual(response.data[0][key], value)


@then('the first item should have "{key}" equal to number "{value:Number}"')
def see_numeric_key_value_of_first(context, key, value):
    response = context.response
    print(response.data)
    context.test.assertEqual(response.data[0][key], value)


@then('the last part should have "{key}" equal to "{value}"')
def see_key_value_of_last(context, key, value):
    response = context.response
    print(response.data)
    context.test.assertEqual(response.data[-1][key], value)


@then('the last part should have "{key}" equal to number "{value:Number}"')
def see_numeric_key_value_of_last(context, key, value):
    response = context.response
    print(response.data)
    context.test.assertEqual(response.data[-1][key], value)


@then('the status code should be "{code:Number}"')
def status_code_check(context, code):
    response = context.response
    context.test.assertEqual(response.status_code, code)
