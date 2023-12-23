from django.test import TestCase
from django.urls import reverse
from .models import CustomUser
from .forms import UserLoginForm


class CustomUserModelTest(TestCase):

    def test_email_label(self):
        user = CustomUser.objects.create(EMAIL="test@example.com")
        field_label = user._meta.get_field('EMAIL').verbose_name
        self.assertEqual(field_label, 'EMAIL')


class HomePageViewTest(TestCase):

    def setUp(self):
        CustomUser.objects.create(EMAIL="test@sdfi.dk")

    def test_home_page_view_status_code(self):
        response = self.client.get(reverse('home_page_view'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_uses_correct_template(self):
        response = self.client.get(reverse('home_page_view'))
        self.assertTemplateUsed(response, 'homepage.html')

    def test_home_page_user_login_redirect(self):
        form_data = {'email': 'test@sdfi.dk', 'user_login': True}
        response = self.client.post(reverse('home_page_view'), form_data, follow=True)
        self.assertRedirects(response, reverse('personal_page_view'))


class UserLoginFormTest(TestCase):

    def test_valid_email(self):
        form = UserLoginForm(data={'email': 'user@sdfi.dk'})
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = UserLoginForm(data={'email': 'user@example.com'})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Email must end with \'@sdfi.dk\''])

    def test_empty_email(self):
        form = UserLoginForm(data={'email': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


