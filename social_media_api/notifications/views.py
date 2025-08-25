from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from .serializers import NotificationSerializer

class NotificationPagination(PageNumberPagination):
    page_size = 20

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotificationPagination

    def get_queryset(self):
        return self.request.user.notifications.all()

class MarkNotificationReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notif.unread = False
        notif.save()
        return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)

class MarkAllReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        qs = request.user.notifications.filter(unread=True)
        updated = qs.update(unread=False)
        return Response({'detail': f'{updated} notifications marked as read.'}, status=status.HTTP_200_OK)
