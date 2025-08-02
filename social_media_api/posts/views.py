from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth import mixins
from django.dispatch import receiver
from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like
from notifications.models import Notification

class PostPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100


# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class PostListView(generics.ListAPIView):
    # queryset = Post.objects.all()
    # serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]

    def get(self, request):
        posts = Post.objects.all()
        paginated_posts = PostPagination().paginate_queryset(
            queryset=posts, request=request)
        serializer = PostSerializer(paginated_posts, many=True)
        return Response(serializer.data)


class PostCreateView(generics.CreateAPIView, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin):
    serializer_class = PostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateView(generics.UpdateAPIView, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin):
    def post(self, request):
        serializer = PostSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            post = Post.objects.get(id=request.data['id'])
            if post.author == request.user:
                serializer.update(post, serializer.validated_data)
                return Response(serializer.data)
        return Response(serializer.errors, status=400)


class PostDetailView(generics.ListAPIView):
    def get(self, request):
        # Handle GET request
        post = Post.objects.get(id=request.data['id'])
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostDeleteView(generics.DestroyAPIView, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.author == request.user:
            post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostSearchView(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self, request):
        search_term = request.GET.get('search_term')
        title_q = Q(title__icontains=search_term) if search_term else Q()
        content_q = Q(content__icontains=search_term) if search_term else Q()
        # combined_q = title_q & content_q
        results = Post.objects.filter(title_q).filter(content_q)
        return results


class CommentPagination(PageNumberPagination):
    page_size = 20  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentListView(generics.ListAPIView):
    pagination_class = CommentPagination
    filter_backends = [filters.SearchFilter]

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post)
        paginated_comments = CommentPagination().paginate_queryset(
            queryset=comments, request=request)
        serializer = CommentSerializer(paginated_comments, many=True)
        return Response(serializer.data)


class CommentCreateView(APIView, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin):
    serializer_class = CommentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateView(APIView, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin):
    def post(self, request):
        serializer = CommentSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            comment = Comment.objects.get(id=request.data['pk'])
            if self.user != request.user:
                raise PermissionDenied(
                    'Only the author can edit or delete this post')
            if comment.author == request.user:
                serializer.update(Comment, serializer.validated_data)
                return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CommentDetailView(APIView):
    def get(self, request):
        # Handle GET request
        comment = Comment.objects.get(id=request.data['id'])
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class CommentDeleteView(generics.DestroyAPIView, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class FeedView(generics.ListAPIView, mixins.LoginRequiredMixin, mixins.UserPassesTestMixin):
class FeedView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.followers.all()
        return Post.objects.filter(author__in=following_users).order_by('-creation_date')

    # (self, request):
    #     posts = Post.objects.filter(author__in=request.user.following.all())
    #     return

# class LikePostView(GenericAPIView, CreateModelMixin):


class LikePostView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

        
    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_id)
        post = generics.get_object_or_404(Post, pk=post_id)
        Like.objects.get_or_create(user=self.request.user, post=post)
        if Like.objects.filter(user=self.request.user, post=post).exists():
            # User has already liked this post, return a 400 error
            return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)
        # serializer.save(post=post)
        # return Response({'message': 'Liked successfully'}, status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(
            data={'post': post, 'user': self.request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, **kwargs):
    liker = instance.user
    post = instance.post
    
    # Create a notification
    Notification.objects.create(
        user=liker,  # recipient
        message=f"{liker.username} liked your post: {post.title}",  # notification message
        link=post.get_absolute_url()  # link to the post
    )


class UnlikePostView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        like = get_object_or_404(Like, post__pk=pk, user=request.user)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def post(self, request):
    pk = self.kwargs['pk']
    post = generics.get_object_or_404(Post, pk=pk)
    post = generics.get_object_or_404(Post, pk=post_id)
    Like.objects.get_or_create(user=request.user, post=post)
    return Response(status=status.HTTP_201_CREATED)
# Create your views here.
