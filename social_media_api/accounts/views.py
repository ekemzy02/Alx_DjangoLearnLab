# Create your views here.
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .serializers import CustomUserSerializer, LoginSerializer, UserProfileSerializer
from .models import CustomUser, UserProfile

"CustomUser.objects.all()"

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


# class UserProfileUpdateView(APIView):
class UserProfileUpdateView(generics.GenericAPIView):
    def put(self, request, pk):
        user_profile = UserProfile.objects.get(pk=pk)
        serializer = UserProfileSerializer(
            user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def follow_user(request, pk):
    user_to_follow = get_object_or_404(CustomUser, id=pk)
    if not request.user.following.filter(id=pk).exists():
        request.user.following.add(user_to_follow)
        user_to_follow.followers.add(request.user)
    return redirect('profile')


class FollowView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = get_object_or_404(CustomUser, id=pk)
        if not request.user.following.filter(id=pk).exists():
            request.user.following.add(user_to_follow)
            user_to_follow.followers.add(request.user)
        return redirect('profile')


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    request.user.following.remove(user_to_unfollow)
    user_to_unfollow.followers.remove(request.user)
    return redirect('profile')


class UnfollowView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        request.user.following.remove(user_to_unfollow)
        user_to_unfollow.followers.remove(request.user)
        return redirect('profile')