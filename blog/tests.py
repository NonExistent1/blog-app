from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post

class BlogTests(TestCase):
    """BlogTest"""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )

        cls.post = Post.objects.create(
            title ="test title",
            body="test body content",
            author = cls.user,
        )

    def test_post_model(self):
        """Test post model"""
        self.assertEqual(self.post.title, "test title")
        self.assertEqual(self.post.body, "test body content")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "test title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location_listview(self):
        """test url exists at correct location listview"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        """test url exists at correct location detailview"""
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):
        """test post list view"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test body content")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):
        """test post detail view"""
        response = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        noresponse = self.client.get("/post/1000000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(noresponse.status_code, 404)
        self.assertContains(response, "test title")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_createview(self):
        """test post create view"""
        response = self.client.post(
            reverse("post_new"),
            {
                "title":"New Title",
                "body":"New Text",
                "author":self.user.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "New Title")
        self.assertEqual(Post.objects.last().body, "New Text")

    def test_post_updateview(self):
        """test post update view"""
        response = self.client.post(
            reverse("post_edit", args="1"),
            {
                "title":"Updated Title",
                "body":"Updated Text",
                "author":self.user.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "Updated Title")
        self.assertEqual(Post.objects.last().body, "Updated Text")

    def test_post_deleteview(self):
        """test post delete view"""
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)

    