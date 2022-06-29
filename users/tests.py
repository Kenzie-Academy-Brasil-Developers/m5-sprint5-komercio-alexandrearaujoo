from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.data = {
            'email': 'alexandre@mail.com',
            'first_name':'Alexandre',
            'last_name':'Araujo',
            'password': '12345',
            'is_seller': True
        }

        cls.user = User.objects.create_user(**cls.data)

    def test_email_unique(self):
        user = User.objects.get(pk=1)

        unique = user._meta.get_field('email').unique

        self.assertEqual(unique, True)

    def test_is_seller(self):
        user = User.objects.get(pk=1)

        self.assertEqual(user.is_seller, True)

    def test_first_name_max_length(self):
        user = User.objects.get(pk=1)

        max_length = user._meta.get_field('first_name').max_length

        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        user = User.objects.get(pk=1)

        max_length = user._meta.get_field('last_name').max_length

        self.assertEqual(max_length, 50)

    def test_object_name_is_first_name_comma_last_name(self):
        user = User.objects.get(pk=1)

        expected_object_name = f'{user.first_name} {user.last_name} - {user.is_seller}'

        self.assertEquals(expected_object_name, str(user))

    def test_actor_has_information_fields(self):

        self.assertEqual(self.user.email, self.data["email"])
        self.assertEqual(self.user.first_name, self.data["first_name"])
        self.assertEqual(self.user.last_name, self.data["last_name"])
        self.assertEqual(self.user.is_seller, self.data["is_seller"])
        self.assertEqual(self.user.is_active, True)

        