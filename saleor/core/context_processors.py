import json
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from ..core.utils import build_absolute_uri
from ..product.models import Category


def get_setting_as_dict(name, short_name=None):
    short_name = short_name or name
    try:
        return {short_name: getattr(settings, name)}
    except AttributeError:
        return {}


# request is a required parameter
# pylint: disable=W0613
def default_currency(request):
    return get_setting_as_dict('DEFAULT_CURRENCY')


# request is a required parameter
# pylint: disable=W0613
def categories(request):
    return {'categories': Category.tree.root_nodes().filter(is_hidden=False)}


def search_enabled(request):
    return {'SEARCH_IS_ENABLED': settings.ENABLE_SEARCH}


def webpage_schema(request):
    site = get_current_site(request)
    url = build_absolute_uri(location='/')
    data = {
        '@context': 'http://schema.org',
        '@type': 'WebSite',
        'url': url,
        'name': site.name,
        'description': site.settings.description}
    if settings.ENABLE_SEARCH:
        search_url = urljoin(url, reverse('search:search'))
        data['potentialAction'] = {
            '@type': 'SearchAction',
            'target': '%s?q={q}' % search_url,
            'query-input': 'required name=q'}
    return {'webpage_schema': json.dumps(data)}
