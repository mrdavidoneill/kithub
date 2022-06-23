import json
import string
import decimal
from datetime import date, datetime, timedelta
from random import choice, randint, shuffle
from kithub.api.models import *
from django.urls import reverse
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import status
from rest_framework.test import APIClient

#####################
#     CONSTANTS     #
#####################

MODEL_NAMES = {
    "kit": Kit,
    "kittype": KitType,
    "bag": Bag,
    "bagtype": BagType,
    "part": Part,
    "purchase": Purchase,
}

##########################
# Utility functions #
##########################


def comparePayloadToRepsonseData(test_instance, payload, response):
    """Compare payload dictionary to response from API"""
    # Compare payload sent to response returned
    for param_key, param_value in payload.items():

        # If key is name of a Model
        if param_key in MODEL_NAMES:
            # If key is a primary key
            if type(param_value) is int:

                # If response is an integer ID
                if type(response[param_key]) is int:
                    test_instance.assertEqual(param_value, response[param_key])

                # Compare to object
                else:
                    test_instance.assertEqual(param_value, response[param_key]["id"])

            # If key is dict representation of a model
            else:
                # Test that there is an object there with same k,v as param
                comparePayloadToRepsonseData(
                    test_instance, payload[param_key], response[param_key]
                )

        # If key is a date
        elif type(param_value) is date:
            test_instance.assertEqual(
                param_value, datetime.strptime(response[param_key], "%Y-%m-%d").date()
            )
        # If key is a list
        elif type(param_value) is list:
            for index, item in enumerate(param_value):
                comparePayloadToRepsonseData(
                    test_instance, item, response[param_key][index]
                )
        # If key is a Decimal
        elif type(param_value) is decimal.Decimal:
            test_instance.assertEqual(param_value, decimal.Decimal(response[param_key]))
        # Compare directly for everything else
        else:
            test_instance.assertEqual(param_value, response[param_key])


#############################
# 'Create random' functions #
#############################


def random_boolean():
    """Return random boolean"""
    return bool(randint(0, 1))


def random_description():
    """Return random description"""
    colour = choice(("red", "green", "blue", "black", "silver", "white"))
    part = choice(("pot", "resistor", "screw", "L-bracket", "PCB"))
    return f"A {colour} {randint(100, 1500)} {part}"


def random_kind():
    letters = [choice(string.ascii_letters) for n in range(10)]
    letters.append(str(choice(range(9999))))
    return "".join(letters)


def random_money():
    """Return random money amount
    max 10 digits, and 5 decimal places
    eg. 10.00 or 0.004
    """
    return decimal.Decimal(f"{round(randint(1, 50) / 10, 2)}")


def random_name():
    """Return random name for kit or bag
    Name is based on contents contained,
    eg. ABCDEFGH or A C EFG
    """
    completed = string.ascii_letters[26 : randint(34, 41)]
    uncompleted = ""
    for letter in completed:
        uncompleted += choice((letter, " "))
    return uncompleted


def random_past_date(end=365 * 10, **kwargs):
    """Return random date in the past 10 years, or back until end number of days"""
    return date.today() - timedelta(days=choice(range(end)))


def random_quantity(min=1, max=100):
    """Return number between min and max inclusive"""
    return randint(min, max)


def random_shop():
    """Return random shop name"""
    shops = ("Mouser", "RS", "Farnell", "CPC", "Quick-Teck")
    return choice(shops)


##########################
# Create model functions #
##########################


def create_kittype():
    """Return a random kittype"""
    return KitType.objects.create(kind=random_kind())


def create_kit(kind=None):
    """Return a random kit of passed kind, or newly created kind"""
    if not kind:
        kind = create_kittype()

    kwargs = {
        "name": random_name(),
        "quantity": random_quantity(),
        "complete": random_boolean(),
        "kind": kind,
    }

    return Kit.objects.create(**kwargs)


def create_bagtype():
    """Return a random bagtype"""
    return BagType.objects.create(kind=random_kind())


def create_bag(kind=None):
    """Return a random bag of passed kind, or newly created kind"""
    if not kind:
        kind = create_bagtype()

    kwargs = {
        "name": random_name(),
        "quantity": random_quantity(),
        "complete": random_boolean(),
        "kind": kind,
    }
    return Bag.objects.create(**kwargs)


def create_bagingredient(name=None, bagtype=None, part=None, quantity=None):
    """Return a random bag of passed kind, or newly created kind"""
    if not name:
        name = random_kind()[:4]
    if not bagtype:
        bagtype = create_bagtype()
    if not part:
        part = create_part()
    if not quantity:
        quantity = random_quantity()
    kwargs = {
        "name": name,
        "bagtype": bagtype,
        "part": part,
        "quantity": quantity,
    }
    return BagIngredient.objects.create(**kwargs)


def create_kitingredient(name=None, kittype=None, bagtype=None, quantity=None):
    """Return a random kit ingredient of passed kittype, or newly created KitType,
    with a passed bagtype, or newly created BagType"""
    if not bagtype:
        bagtype = create_bagtype()
    if not kittype:
        kittype = create_kittype()
    if not quantity:
        quantity = random_quantity()
    kwargs = {
        "name": random_kind()[:4],
        "bagtype": bagtype,
        "kittype": kittype,
        "quantity": quantity,
    }
    return KitIngredient.objects.create(**kwargs)


def create_part(kind=None):
    """Return a random part"""
    kwargs = {
        "name": random_kind(),
        "description": random_description(),
        "quantity": random_quantity(0, 10_000),
    }
    return Part.objects.create(**kwargs)


def create_purchase(part=None):
    """Return a purchase or part passed, or newly created part"""
    if not part:
        part = create_part()
    kwargs = {
        "date": random_past_date(),
        "shop": random_shop(),
        "shop_part_no": random_kind(),
        "price": random_money(),
        "quantity": random_quantity(1, 10_000),
        "part": part,
    }
    return Purchase.objects.create(**kwargs)


#############################
# Create payload functions #
#############################
def create_bag_payload(kind=None):
    """Return a random bag payload of passed kind, or newly created Kind"""
    if kind is None:
        kind = create_bagtype()

    payload = {
        "name": random_name(),
        "quantity": random_quantity(),
        "complete": random_boolean(),
        "kind": kind.pk,
    }
    return payload


def create_bagingredient_payload(kind=None, part=None):
    """Return a random bag ingredient payload of passed kind, or newly created Kind
    For passed part, or newly created Part"""

    if kind is None:
        kind = create_bagtype()
    if part is None:
        part = create_part()

    payload = {
        "name": random_kind()[:4],
        "bagtype": kind.pk,
        "part": part.pk,
        "quantity": random_quantity(1, 10),
    }
    return payload


def create_kitingredient_payload(kind=None, bagtype=None):
    """Return a random kit ingredient payload of passed kind, or newly created Kind
    For passed bagtype, or newly created BagType"""

    if kind is None:
        kind = create_kittype()
    if bagtype is None:
        bagtype = create_bagtype()

    payload = {
        "name": random_kind()[:4],
        "kittype": kind.pk,
        "bagtype": bagtype.pk,
        "quantity": random_quantity(1, 10),
    }
    return payload


def create_bagtype_payload():
    """Return a random bagtype payload"""
    payload = {
        "kind": random_kind(),
    }
    return payload


def create_kit_payload(kind=None):
    """Return a random kit payload of passed kind, or newly created Kind"""
    if kind is None:
        kind = create_kittype()

    payload = {
        "name": random_name(),
        "quantity": random_quantity(),
        "complete": random_boolean(),
        "kind": kind.pk,
    }
    return payload


def create_kittype_payload():
    """Return a random kittype payload"""
    payload = {
        "kind": random_kind(),
    }
    return payload


def create_part_payload():
    """Return a random part payload"""
    payload = {
        "name": random_kind(),
        "description": random_description(),
        "quantity": random_quantity(0, 10_000),
    }
    return payload


def create_purchase_payload(part=None):
    """Return a random purchase payload of passed part, or newly created Part"""
    if part is None:
        part = create_part()

    payload = {
        "date": random_past_date(),
        "shop": random_shop(),
        "shop_part_no": random_kind(),
        "price": random_money(),
        "quantity": random_quantity(1, 10_000),
        "part": part.pk,
    }
    return payload


def create_parts(num=100):
    for i in range(num):
        create_part()


def create_bagtypes(num=50):
    for i in range(num):
        create_bagtype()


def create_kittypes(num=10):
    for i in range(num):
        create_kittype()


def create_bagtype_ingredients(bagtype):
    parts = Part.objects.all()
    parts = list(parts)
    shuffle(parts)  # Inline shuffle
    num_of_parts = randint(5, 12)
    # Place num_of_parts if not exceeding stocked parts
    for i, part in enumerate(parts):
        if i > num_of_parts:
            break
        create_bagingredient(
            name=string.ascii_letters[i].upper(),
            bagtype=bagtype,
            part=part,
            quantity=randint(1, 10),
        )


def create_all_bagtype_ingredients():
    bagtypes = BagType.objects.all()
    for bagtype in bagtypes:
        create_bagtype_ingredients(bagtype)


def create_kittype_ingredients(kittype):
    bagtypes = BagType.objects.all()
    bagtypes = list(bagtypes)
    shuffle(bagtypes)  # Inline shuffle
    num_of_bagtypes = randint(5, 12)
    # Place num_of_bagtypes if not exceeding stocked bagtypes
    for i, bagtype in enumerate(bagtypes):
        if i > num_of_bagtypes:
            break
        create_kitingredient(
            name=string.ascii_letters[i].upper(),
            kittype=kittype,
            bagtype=bagtype,
            quantity=randint(1, 10),
        )


def create_all_kittype_ingredients():
    kittypes = KitType.objects.all()
    for kittype in kittypes:
        create_kittype_ingredients(kittype)


def create_fresh_world():
    delete_everything()
    create_parts()
    create_bagtypes()
    create_kittypes()
    create_all_bagtype_ingredients()
    create_all_kittype_ingredients()


###########################
# MODEL TESTING FUNCTIONS #
###########################


def retrieve_by_pk(test, model, new_instance):
    retrieved = model.objects.get(pk=new_instance.pk)
    # Get dictionary of new instance before DB, and retrieved instance from DB
    new_instance_dict = vars(new_instance)
    retrieved_dict = vars(retrieved)
    # Check comparing different states - eg. one from creating for DB and one from retrieving from DB
    new_instance_state = new_instance_dict.pop("_state")
    retrieved_state = retrieved_dict.pop("_state")
    test.assertNotEqual(new_instance_state, retrieved_state)
    # Check all properties are the same
    for k, v in new_instance_dict.items():
        test.assertEqual(new_instance_dict[k], retrieved_dict[k])


##########################
# VIEW TESTING FUNCTIONS #
##########################


def test_get_all(
    client,
    route,
    instance,
    model,
    serializer,
    expected_number=None,
):
    """Test that all items are returned"""
    print(f"\nGET_ALL: {route}")
    # Client visit route with token
    response = client.get(reverse(route))

    print(f"\n GET_ALL_RESPONSE ({len(response.data)}): {response.data}")

    # Artificially return expected result from DB
    items = model.objects.all()
    serializer = serializer(items, many=True)

    print(f"\nGET_ALL_RESPONSE ({response.data}")
    print(f"\nDB_RESPONSE ({serializer.data}")

    # Compare
    instance.assertEqual(response.data, serializer.data)
    instance.assertEqual(response.status_code, status.HTTP_200_OK)

    if expected_number:
        instance.assertEqual(len(response.data), expected_number)


def test_valid_get_single_item(client, route, instance, item, model, serializer):
    """Test that an item returns"""
    # Client visit route
    response = client.get(reverse(route, kwargs={"pk": item.pk}))

    # Compare item data
    new_item = model.objects.get(pk=response.data["id"])
    serializer = serializer(new_item)
    instance.assertEqual(response.data, serializer.data)
    instance.assertEqual(response.status_code, status.HTTP_200_OK)


def test_invalid_get_single_item(client, route, instance, model, serializer):
    """Test for invalid item"""
    # Client visit route with token
    response = client.get(reverse(route, kwargs={"pk": -1}))
    instance.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


def test_valid_create(
    client, route, payload, instance, model, serializer, detail_route
):
    """Test that can create item"""

    print(f"\nVALID_CREATE_PAYLOAD: {payload}")

    post_response = client.post(
        reverse(route),
        data=json.dumps(payload, cls=DjangoJSONEncoder),
        content_type="application/json",
    )

    print(f"\tPOST response: {post_response.data}")

    get_response = client.get(
        reverse(detail_route, kwargs={"pk": post_response.data["id"]})
    )

    # Retrieve item direct from DB
    new_item = model.objects.get(pk=post_response.data["id"])
    serializer = serializer(new_item)

    print(f"VALID_CREATE_POST_RESPONSE: {post_response.data}")
    print(f"VALID_CREATE_GET_RESPONSE: {get_response.data}")
    print(f"VALID_CREATE_FROM_DB_DIRECTLY: {serializer.data}")

    comparePayloadToRepsonseData(instance, payload, post_response.data)
    comparePayloadToRepsonseData(instance, payload, get_response.data)
    instance.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

    # Compare item data from GET response & direct from DB
    instance.assertEqual(get_response.data, serializer.data)
    instance.assertEqual(get_response.status_code, status.HTTP_200_OK)


def test_empty_create(
    client, route, payload, instance, model, serializer, detail_route
):
    print(f"NO_DATA_CREATE_PAYLOAD: {payload}")

    response = client.post(
        reverse(route),
        data=json.dumps(payload, cls=DjangoJSONEncoder),
        content_type="application/json",
    )
    print(f"\tPOST response: {response.data}")

    instance.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


def test_valid_update(client, route, item, payload, instance):

    print(f"\nVALID_UPDATE_ITEM: {vars(item)}")
    print(f"VALID_UPDATE_PAYLOAD: {payload}")
    response = client.put(
        reverse(route, kwargs={"pk": item.pk}),
        data=json.dumps(payload, cls=DjangoJSONEncoder),
        content_type="application/json",
    )
    get_response = client.get(reverse(route, kwargs={"pk": item.pk}))
    print(f"VALID_UPDATE_PUT_RESPONSE: {response.data}")
    print(f"VALID_UPDATE_GET_RESPONSE: {get_response.data}")

    comparePayloadToRepsonseData(instance, payload, response.data)
    comparePayloadToRepsonseData(instance, payload, get_response.data)
    instance.assertEqual(response.status_code, status.HTTP_200_OK)


def test_empty_update(client, route, item, payload, instance):
    print(f"\nNO_DATA_UPDATE_ITEM: {vars(item)}")
    print(f"NO_DATA_UPDATE_PAYLOAD: {payload}")
    response = client.put(
        reverse(route, kwargs={"pk": item.pk}),
        data=json.dumps(payload, cls=DjangoJSONEncoder),
        content_type="application/json",
    )
    get_response = client.get(reverse(route, kwargs={"pk": item.pk}))
    print(f"NO_DATA_UPDATE_PUT_RESPONSE: {response.data}")
    print(f"NO_DATA_UPDATE_GET_RESPONSE: {get_response.data}")
    instance.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


def test_valid_delete(
    client,
    route,
    route_list,
    item,
    instance,
    model,
):
    """Test that item is deleted with valid item"""
    print(f"TEST VALID DELETE: {item}")
    # Test can get item
    get_all_response_before = client.get(reverse(route_list))
    get_item_response_before = client.get(reverse(route, kwargs={"pk": item.pk}))

    print(f"GET ALL BEFORE DELETE: {len(get_all_response_before.data)} items")
    print(f"GET ITEM BEFORE DELETE: {get_item_response_before.data}")

    # Perform delete
    response = client.delete(reverse(route, kwargs={"pk": item.pk}))

    # Test cannot get item
    get_item_response_after = client.get(reverse(route, kwargs={"pk": item.pk}))
    get_all_response_after = client.get(reverse(route_list))

    print(f"GET ALL AFTER DELETE: {len(get_all_response_after.data)} items")
    print(f"GET ITEM AFTER DELETE: {get_item_response_after.data}")

    instance.assertEqual(
        len(get_all_response_before.data),
        len(get_all_response_after.data) + 1,
    )
    instance.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    instance.assertEqual(get_item_response_before.status_code, status.HTTP_200_OK)
    instance.assertEqual(get_item_response_after.status_code, status.HTTP_404_NOT_FOUND)


def test_invalid_id_delete(
    client,
    route,
    route_list,
    item_id,
    instance,
    model,
):
    """Test that invalid item is handled"""
    response = client.delete(reverse(route, kwargs={"pk": item_id}))
    instance.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
