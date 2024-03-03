from .models import Post, Rating
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'post_id', 'rate']


class PostSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'user_rating', 'average_rating']


    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                rating = Rating.objects.get(post_id=obj, user_id=request.user)
                return RatingSerializer(rating).data
            except Rating.DoesNotExist:
                return None
        return None

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            total_score = sum(rating.rate for rating in ratings)
            return total_score / len(ratings)
        return 0  # Return 0 if no ratings yet

