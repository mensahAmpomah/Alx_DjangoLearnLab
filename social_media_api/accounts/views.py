from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SimpleUserSerializer, FollowActionSerializer

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user, context={'request': request}).data
        return Response({'token': token.key, 'user': data}, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user, context={'request': request}).data
        return Response({'token': token.key, 'user': data}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    


User = get_user_model()

class FollowUserView(APIView):
    """
    POST   /api/accounts/follow/<int:user_id>/    -> follow the user
    DELETE /api/accounts/follow/<int:user_id>/    -> unfollow the user
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, format=None):
        target = get_object_or_404(User, id=user_id)
        if target.id == request.user.id:
            return Response({'detail': "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # add to following
        request.user.following.add(target)
        request.user.save()

        data = {
            'target_user_id': target.id,
            'following': True,
            'followers_count': target.followers.count(),
            'following_count': request.user.following.count()
        }
        return Response(FollowActionSerializer(data).data, status=status.HTTP_200_OK)

    def delete(self, request, user_id, format=None):
        target = get_object_or_404(User, id=user_id)
        if target.id == request.user.id:
            return Response({'detail': "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # remove from following
        request.user.following.remove(target)
        request.user.save()

        data = {
            'target_user_id': target.id,
            'following': False,
            'followers_count': target.followers.count(),
            'following_count': request.user.following.count()
        }
        return Response(FollowActionSerializer(data).data, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    """
    GET /api/accounts/following/ -> list of users current user follows
    """
    serializer_class = SimpleUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return QuerySet of users this user follows
        return self.request.user.following.all()
