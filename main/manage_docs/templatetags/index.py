from django import template
import re

register = template.Library()


@register.filter
def document_from_valid_html_name(document_set, html_name):
    # only use valid fields, and return relevant document
    pattern = "document_[0-9]+_valid"
    if interval := re.fullmatch(pattern, html_name):
        id = int(re.search("[0-9]+", interval.group()).group())
        return document_set.get(id=id)
    return None


@register.filter
def get_document_request_field_from_valid(fields, html_name):
    # other generated fields have the same id in them
    pattern = "document_{}_request".format(re.search("[0-9]+", html_name).group())
    for f in fields:
        if f.html_name == pattern:
            return f
    return None


@register.filter
def get_document_from_file_html_name(document_set, html_name):
    # other generated fields have the same id in them
    pattern = "document_[0-9]+_file"
    if interval := re.fullmatch(pattern, html_name):
        id = int(re.search("[0-9]+", interval.group()).group())
        return document_set.get(id=id)
    return None
