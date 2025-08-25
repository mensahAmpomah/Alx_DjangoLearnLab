from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class FollowTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass123')
        self.bob = User.objects.create_user(username='bob', password='pass123')
        self.token = Token.objects.create(user=self.alice)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_follow_unfollow_flow(self):
        url = reverse('follow-user', kwargs={'user_id': self.bob.id})
        # follow
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(self.bob, self.alice.following.all())
        # unfollow (DELETE)
        resp2 = self.client.delete(url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.bob, self.alice.following.all())

    def test_cannot_follow_self(self):
        url = reverse('follow-user', kwargs={'user_id': self.alice.id})
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
