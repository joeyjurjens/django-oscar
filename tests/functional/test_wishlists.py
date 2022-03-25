from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from oscar.apps.wishlists.models import WishList, WishListSharedEmail
from oscar.test.factories import WishListFactory

User = get_user_model()


class WishListPrivateTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email="test@example.com", password="testpassword")
        self.wishlist = WishListFactory(owner=self.user, visibility=WishList.PRIVATE)

    def test_private_wishlist_detail_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(response.status_code, 200)

    def test_private_wishlist_detail_logged_out_user(self):
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(response.status_code, 404)

    def test_private_wishlist_detail_shared_email(self):
        WishListSharedEmail.objects.create(wishlist=self.wishlist, email="test2@example.com")
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(
            response.status_code,
            404,
            "The response should be 404 because the visibility is set to private."
        )


class WishListPublicTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email="test@example.com", password="testpassword")
        self.wishlist = WishListFactory(owner=self.user, visibility=WishList.PUBLIC)

    def test_public_wishlist_detail_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(response.status_code, 200)

    def test_public_wishlist_detail_logged_out_user(self):
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(response.status_code, 200)

    def test_public_wishlist_detail_shared_email(self):
        WishListSharedEmail.objects.create(wishlist=self.wishlist, email="test2@example.com")
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(response.status_code, 200)


class WishListSharedTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email="test@example.com", password="testpassword")
        self.wishlist = WishListFactory(owner=self.user, visibility=WishList.SHARED)

    def test_shared_wishlist_detail_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(response.status_code, 200)

    def test_shared_wishlist_detail_logged_out_user(self):
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(response.status_code, 404)

    def test_shared_wishlist_detail_shared_email(self):
        WishListSharedEmail.objects.create(wishlist=self.wishlist, email="test2@example.com")
        user = User.objects.create(email="test2@example.com", password="testpassword", username="test2")
        self.client.force_login(user)
        response = self.client.get(reverse("wishlists:detail", kwargs={'key': self.wishlist.key}))
        self.assertEqual(response.status_code, 200)
