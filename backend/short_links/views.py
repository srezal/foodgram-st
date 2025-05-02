from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import LinkPair


def handle_short_link(request, slug):
    print(request.build_absolute_uri(f'/{slug}/'))
    try:
        link_pair = LinkPair.objects.get(short_link=f'/{slug}/')
    except LinkPair.DoesNotExist:
        return JsonResponse({
            'detail': 'Not page found.'
        }, status=404)
    print(request.build_absolute_uri(f'{link_pair.original_link}'))
    return HttpResponseRedirect(request.build_absolute_uri(f'{link_pair.original_link}'))
