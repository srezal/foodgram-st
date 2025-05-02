from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.http import FileResponse
from io import BytesIO
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import RecipeSerializer, AddRecipeInShoppingCartSerializer
from .models import Recipe, ShoopingCart
from core.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from short_links.models import LinkPair
from .pdf import ShoppingCartDocument


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['author']
    serializer_class = RecipeSerializer


    @action(
        permission_classes=[IsAuthenticated],
        methods=['post'],
        detail=True,
        url_path='shopping_cart',
        url_name='shopping_cart'
    )
    def add_in_shopping_cart(self, request, pk):
        serializer = AddRecipeInShoppingCartSerializer(
            data={
                'user': self.request.user,
                'recipe': pk
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @action(
        permission_classes=[IsAuthenticated],
        methods=['get'],
        detail=False,
        url_path='download_shopping_cart',
        url_name='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        recipes = [
            item.recipe for item in ShoopingCart.objects.filter(
                user=request.user
            ) 
        ]
        serializer = RecipeSerializer(recipes, many=True, context={'request': request})
        doc = ShoppingCartDocument(serializer.data)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='foodgram_shopping_list.pdf',
        )
        


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

