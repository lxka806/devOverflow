from django.test import TestCase
from django.urls import reverse

from .models import Users


class UserPageTests(TestCase):
    def setUp(self):
        self.user = Users.objects.create(
            name="Profile Developer",
            email="profile@example.invalid",
            password="password",
            bio="Building useful things.",
            is_curentUser=True,
        )

    def test_authentication_and_profile_pages_render(self):
        page_names = (
            "login_user",
            "register",
            "profile",
            "edit_profile",
            "user_info",
        )

        for page_name in page_names:
            with self.subTest(page=page_name):
                if page_name == "user_info":
                    response = self.client.get(
                        reverse(page_name, args=[self.user.id])
                    )
                else:
                    response = self.client.get(reverse(page_name))

                self.assertEqual(response.status_code, 200)
