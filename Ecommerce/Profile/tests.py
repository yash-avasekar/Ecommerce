from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        Profile.objects.create(
            user=user,
            username='testuser',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
            address='123 Main St',
            state='CA',
            city='Los Angeles',
            zipcode='90001',
            landmark='Near the park',
            contact_no='1234567890'
        )

    def test_username_label(self):
        profile = Profile.objects.get(username='testuser')
        field_label = profile._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    # Add more test methods for other fields if needed
