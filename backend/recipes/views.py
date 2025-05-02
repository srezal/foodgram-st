from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import RecipeSerializer
from .models import Recipe
from core.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from short_links.models import LinkPair


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['author']
    serializer_class = RecipeSerializer


    @action(
        methods=['get'],
        detail=True,
        url_path='get-link',
        url_name='get-link',
    )
    def get_link(self, request, pk):
        short_link = LinkPair.get_or_create_short_link(f'/api/recipes/{pk}/')
        return Response({
            'short-link': request.build_absolute_uri(short_link)
        })

