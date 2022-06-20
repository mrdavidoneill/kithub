from django.urls import reverse


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
