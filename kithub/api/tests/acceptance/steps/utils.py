from django.urls import reverse

JSON_CONTENT = "application/json"


def get_part_by_name(parts, name):
    for part in parts:
        print(part)
        if part["name"] == name:
            return part


def get_bagtype_by_kind(bagtypes, kind):
    for bagtype in bagtypes:
        print(bagtype)
        if bagtype["kind"] == kind:
            return bagtype


def get_item_by_key(items, value, key):
    for item in items:
        print(item)
        if item[key] == value:
            return item
