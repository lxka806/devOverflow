from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from users.models import Users

from .models import Questions


class QuestionViewsTests(TestCase):
    def setUp(self):
        self.user = Users.objects.create(
            name="Question Author",
            email="author@example.invalid",
            password="test-password",
            bio="",
            is_curentUser=True,
        )

    def test_posts_page_displays_questions(self):
        Questions.objects.create(
            title="Example question",
            context="Question details",
            creator=self.user,
        )

        response = self.client.get(reverse("main_page"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Example question")
        self.assertContains(response, "Question details")
        self.assertContains(response, "Question Author")

    def test_create_question_saves_for_current_user(self):
        response = self.client.post(
            reverse("add_questions"),
            {"title": "New question", "context": "Details here"},
        )

        self.assertRedirects(response, reverse("main_page"))
        question = Questions.objects.get(title="New question")
        self.assertEqual(question.context, "Details here")
        self.assertEqual(question.creator, self.user)

    def test_create_question_requires_a_current_user(self):
        Users.objects.update(is_curentUser=False)

        response = self.client.get(reverse("add_questions"))

        self.assertRedirects(response, reverse("login_user"))
