from django.http import HttpResponseRedirect, JsonResponse
from .models import LinkPair


def handle_short_link(request, slug):
    try:
        link_pair = LinkPair.objects.get(short_link=f"/s/{slug}/")
    except LinkPair.DoesNotExist:
        return JsonResponse({"detail": "Not page found."}, status=404)
    return HttpResponseRedirect(
        request.build_absolute_uri(f"{link_pair.original_link}")
    )
