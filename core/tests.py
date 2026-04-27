from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Booking, DailyMessage, Review, Service


class HomeViewTests(TestCase):
    def test_home_page_renders_successfully(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        self.assertContains(response, "Today's Sacred Message")

    def test_home_displays_active_admin_daily_message(self):
        DailyMessage.objects.create(text='Be encouraged today.', active=True)
        DailyMessage.objects.create(text='Inactive message', active=False)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Be encouraged today.')
        self.assertEqual(response.context['daily_message'], 'Be encouraged today.')

    def test_home_falls_back_when_no_admin_message(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['daily_message'])


class PageViewTests(TestCase):
    def test_about_page_renders_successfully(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')

    def test_services_page_renders_successfully(self):
        Service.objects.create(name='Bones Reading', description='Deep ancestral insight.')
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/services.html')
        self.assertContains(response, 'Bones Reading')

    def test_book_page_renders_successfully(self):
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/book.html')

    def test_contact_page_renders_successfully(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_location_page_renders_successfully(self):
        response = self.client.get(reverse('location'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/location.html')

    def test_register_page_renders_successfully(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/register.html')
        self.assertContains(response, 'Begin Your Journey')

    def test_login_page_renders_successfully(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertContains(response, 'Sign in to access your bookings and daily messages.')

    def test_missing_page_returns_404(self):
        response = self.client.get('/does-not-exist/')
        self.assertEqual(response.status_code, 404)


class ReviewViewTests(TestCase):
    def test_review_page_renders_successfully(self):
        response = self.client.get(reverse('review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/review.html')
        self.assertContains(response, 'Write Your Review')

    def test_review_form_submission_creates_review(self):
        response = self.client.post(reverse('review'), {
            'name': 'Test Client',
            'message': 'This is a helpful review.',
            'rating': 5,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you for your review!')
        self.assertEqual(Review.objects.count(), 1)


class BookingViewTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(name='Spiritual Reading', description='A private session with the ancestors.')

    def test_booking_form_submission_creates_booking(self):
        tomorrow = date.today() + timedelta(days=1)
        response = self.client.post(reverse('book'), {
            'name': 'Client Name',
            'email': 'client@example.com',
            'service': self.service.id,
            'date': tomorrow.isoformat(),
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your appointment has been booked successfully!')
        self.assertEqual(Booking.objects.count(), 1)


class ContactViewTests(TestCase):
    def test_contact_form_submission_sends_message(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Visitor',
            'email': 'visitor@example.com',
            'message': 'I would like to book a healing session.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your message has been sent. We will be in touch soon.')


class AuthViewTests(TestCase):
    def test_register_form_submission_creates_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPassw0rd!',
            'password2': 'StrongPassw0rd!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.email, 'newuser@example.com')

    def test_register_accepts_non_gmail_email_domains(self):
        response = self.client.post(reverse('register'), {
            'username': 'otheruser',
            'email': 'otheruser@outlook.co.za',
            'password1': 'StrongPassw0rd!',
            'password2': 'StrongPassw0rd!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(username='otheruser').count(), 1)
        user = User.objects.get(username='otheruser')
        self.assertEqual(user.email, 'otheruser@outlook.co.za')

    def test_login_with_valid_credentials_redirects_home(self):
        User.objects.create_user(username='user1', password='Secret123!')
        response = self.client.post(reverse('login'), {
            'username': 'user1',
            'password': 'Secret123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    def test_login_with_invalid_credentials_shows_error(self):
        response = self.client.post(reverse('login'), {
            'username': 'wrong',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials. Please try again.')
