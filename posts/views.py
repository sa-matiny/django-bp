from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Post, Rating
from .serializers import UserSerializer, PostSerializer, RatingSerializer

from rest_framework import permissions, viewsets
from rest_framework.response import Response


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'head']


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):

        existing_rating = Rating.objects.get(
                user_id=self.request.user,
                post_id=self.request.data.get('post_id'))
        if existing_rating:
            serializer = RatingSerializer(existing_rating, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)  # Return status 200 for update
            return Response(serializer.errors, status=400)

        # Perform creation
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # Return status 201 for creation
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        try:
            book = Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)

        serializer = RatingSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

