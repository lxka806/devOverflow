from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse

from users.models import Users

from .models import Comments, Questions


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

    def test_posts_page_searches_question_titles_and_context(self):
        Questions.objects.create(
            title="React state issue",
            context="An async rendering question",
            creator=self.user,
        )
        Questions.objects.create(
            title="Database index question",
            context="How to debug React rendering",
            creator=self.user,
        )
        Questions.objects.create(
            title="Unrelated Python question",
            context="A separate programming problem",
            creator=self.user,
        )

        response = self.client.get(reverse("main_page"), {"q": "React"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["all_posts"]), 2)

    def test_posts_page_sorts_by_comment_count(self):
        quiet_question = Questions.objects.create(
            title="A quiet question",
            context="Details",
            creator=self.user,
        )
        active_question = Questions.objects.create(
            title="An active question",
            context="Details",
            creator=self.user,
        )
        Comments.objects.create(
            author=self.user,
            question=active_question,
            context="First response",
        )
        Comments.objects.create(
            author=self.user,
            question=active_question,
            context="Second response",
        )

        response = self.client.get(
            reverse("main_page"),
            {"sort": "most_discussed"},
        )

        self.assertEqual(
            list(response.context["all_posts"]),
            [active_question, quiet_question],
        )

    def test_question_detail_displays_comments_and_accepts_a_response(self):
        question = Questions.objects.create(
            title="How does this work?",
            context="Question details",
            creator=self.user,
        )
        Comments.objects.create(
            author=self.user,
            question=question,
            context="An existing response",
        )

        response = self.client.get(
            reverse("question_detail", args=[question.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How does this work?")
        self.assertContains(response, "An existing response")
        self.assertContains(response, "Question Author")

        response = self.client.post(
            reverse("question_detail", args=[question.id]),
            {"context": "A newly submitted response"},
        )

        self.assertRedirects(
            response,
            reverse("question_detail", args=[question.id]),
        )
        self.assertTrue(
            Comments.objects.filter(
                question=question,
                context="A newly submitted response",
            ).exists()
        )
