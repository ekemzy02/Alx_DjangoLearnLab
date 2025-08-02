from rest_framework import serializers

from .models import Post, Comment, Like
from accounts.serializers import CustomUserSerializer # type: ignore


class PostSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['id', 'author', 'title',
        #           'content', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    # nested serializer for the related BlogPost
    post = PostSerializer(read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'content',
                  'created_at', 'updated_at', 'post']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


    def create(self, validated_data):
        user = validated_data['user']
        post = validated_data['post']

        existing_instance = Like.objects.filter(post=post, user=user).first()
        if existing_instance:
            return existing_instance  # return the existing instance
        return super().create(validated_data) 