from django.db.models import Q
from rest_framework import viewsets, mixins, generics, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from products.filters import ProductFilter
from products.models import Product, ClickLike, Review, ProductImage, Favorite
from products.permissions import IsAuthorOrAdminPermission
from products.serializers import ProductDetailSerializer, ProductListSerializer, ReviewSerializers, PostImageSerializer, FavoriteListSerializer
import django_filters.rest_framework as filters


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['title', 'price']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        elif self.action in ['create_review', 'like', 'favorites']:
            return [IsAuthenticated()]
        return []

    @action(detail=False, methods=["GET"])
    def search(self, request, pk=None):
        q = request.query_params.get("q")
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q))
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def create_review(self, request, pk):
        data = request.data.copy()
        data['product'] = pk
        serializer = ReviewSerializers(data=data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        like_obj, created = ClickLike.objects.get_or_create(product=product, user=user)
        if like_obj.is_like:
            like_obj.is_like = False
            like_obj.save()
            return Response('disliked')
        else:
            like_obj.is_like = True
            like_obj.save()
            return Response('liked')

    @action(detail=True, methods=['POST'])
    def favorites(self, request, pk):
        product = self.get_object()
        user = request.user
        favorit, created = Favorite.objects.get_or_create(product=product, user=user)
        if favorit.favorite:
            favorit.favorite = False
            favorit.save()
            return Response('remote to favorite product')
        else:
            favorit.favorite = True
            favorit.save()
            return Response('add to product')


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthorOrAdminPermission()]


class PostImageView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class Favoritess(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}
