from django.urls import reverse
from urllib.parse import urlencode

def reverse_with_query(viewname, query_params=None, **kwargs):
    url = reverse(viewname, **kwargs)
    if query_params:
        url = f"{url}?{urlencode(query_params)}"
    return url