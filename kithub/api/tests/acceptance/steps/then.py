from behave import register_type, then
import parse
import decimal
from django.urls import reverse
from utils import get_item_by_key


@parse.with_pattern(r"\d+")
def parse_number(text):
    return int(text)


@parse.with_pattern(r"(True)|(False)")
def parse_bool(text):
    if text == "True":
        return True
    else:
        return False


register_type(Number=parse_number)
register_type(Boolean=parse_bool)


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


@then('I should see the "{key}" is boolean "{value:Boolean}"')
def see_boolean_key_value(context, key, value):
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


@then('the last item should have "{key}" equal to "{value}"')
def see_key_value_of_last(context, key, value):
    response = context.response
    print(response.data)
    context.test.assertEqual(response.data[-1][key], value)


@then('the last item should have "{key}" equal to number "{value:Number}"')
def see_numeric_key_value_of_last(context, key, value):
    response = context.response
    print(response.data)
    context.test.assertEqual(response.data[-1][key], value)


@then('the first purchase should have "{key}" equal to "{value}"')
def see_key_value_of_first_purchase(context, key, value):
    response = context.response
    print(response.data)
    actual = response.data["purchases"][0][key]
    if key == "price":
        value = decimal.Decimal(value)
        actual = decimal.Decimal(actual)
    context.test.assertEqual(actual, value)


@then('the last purchase should have "{key}" equal to "{value}"')
def see_key_value_of_last_purchase(context, key, value):
    response = context.response
    print(response.data)
    actual = response.data["purchases"][-1][key]
    if key == "price":
        value = decimal.Decimal(value)
        actual = decimal.Decimal(actual)
    context.test.assertEqual(actual, value)


@then('the status code should be "{code:Number}"')
def status_code_check(context, code):
    response = context.response
    context.test.assertEqual(response.status_code, code)


@then('the parts list should contain "{part_name}" with quantity "{quantity:Number}"')
def check_part_in_partlist(context, part_name, quantity):
    parts = context.response.data["parts_to_buy"]
    context.test.assertEqual(parts[part_name], quantity)


@then('"{item}" "{model}" should need to buy "{quantity:Number}" "{missing}"')
def get_need_to_buy(context, item, model, quantity, missing):
    response = context.response.data
    models = context.test.client.get(reverse(f"{model}-list")).data
    model_id = get_item_by_key(models, item, "kind")["id"]
    print(f"response {response}")
    item = get_item_by_key(response, model_id, model)
    print(f"item {item}")
    parts_to_buy = item["parts_to_buy"]
    context.test.assertEqual(parts_to_buy[missing], quantity)


@then('I should see "{letter}" is "{quantity:Number}" of part "{part_name}"')
def check_part_in_ingredient(context, letter, quantity, part_name):
    ingredients = context.response.data["ingredients"]
    ingredient = get_item_by_key(ingredients, letter, "name")
    parts = context.test.client.get(reverse("part-list")).data
    part = get_item_by_key(parts, part_name, "name")

    context.test.assertEqual(ingredient["part"], part["id"])
    context.test.assertEqual(ingredient["quantity"], quantity)
