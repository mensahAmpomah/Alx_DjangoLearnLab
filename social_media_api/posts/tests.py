from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Post, Comment

User = get_user_model()

class PostsCommentsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='alice', email='alice@example.com', password='StrongPass123!'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.other = User.objects.create_user(
            username='bob', email='bob@example.com', password='StrongPass123!'
        )

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'Hello', 'content': 'World'}
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)

    def test_update_post_only_by_author(self):
        post = Post.objects.create(author=self.other, title='t', content='c')
        url = reverse('post-detail', args=[post.id])
        res = self.client.patch(url, {'title': 'new'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_flow(self):
        post = Post.objects.create(author=self.user, title='A', content='B')
        # create comment
        url = reverse('comment-list')
        res = self.client.post(url, {'post': post.id, 'content': 'Nice!'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.filter(post=post).count(), 1)
        # list comments by post filter
        res2 = self.client.get(url, {'post': post.id})
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(res2.data.get('count', 0), 1)
# Create your tests here.
