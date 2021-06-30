from django import template

register = template.Library()

@register.filter(name='getattr')
def getattrfilter(object, attr):
    return getattr(object, attr, "Unknown")

@register.filter
def get_object_fields(object):
    return [field.name for field in object._meta.get_fields() if field.name != "imdb_id"]