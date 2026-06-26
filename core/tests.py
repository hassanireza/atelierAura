import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import ContactMessage, NewsletterSubscriber


class HomeViewTest(TestCase):
    def test_home_200(self):
        r = self.client.get(reverse('home'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Atelier Aura')

    def test_home_contains_plans_link(self):
        r = self.client.get(reverse('home'))
        self.assertContains(r, reverse('plans'))


class ContactViewTest(TestCase):
    def test_contact_get_200(self):
        r = self.client.get(reverse('contact'))
        self.assertEqual(r.status_code, 200)

    def test_contact_post_ajax_success(self):
        r = self.client.post(reverse('contact'), {
            'name': 'Alice', 'email': 'alice@test.com', 'message': 'Hello!'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['success'], True)
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Alice')
        self.assertEqual(msg.email, 'alice@test.com')

    def test_contact_post_missing_fields(self):
        r = self.client.post(reverse('contact'), {
            'name': '', 'email': 'a@b.com', 'message': ''
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.json()['success'], False)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_post_redirects_normal(self):
        r = self.client.post(reverse('contact'), {
            'name': 'Bob', 'email': 'bob@test.com', 'message': 'Hi there'
        })
        self.assertRedirects(r, reverse('contact'))


class NewsletterTest(TestCase):
    def test_subscribe_success(self):
        r = self.client.post(
            reverse('newsletter_subscribe'),
            json.dumps({'email': 'sub@test.com'}),
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()['success'])
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)

    def test_subscribe_duplicate(self):
        NewsletterSubscriber.objects.create(email='dup@test.com')
        r = self.client.post(
            reverse('newsletter_subscribe'),
            json.dumps({'email': 'dup@test.com'}),
            content_type='application/json'
        )
        self.assertTrue(r.json()['success'])
        self.assertIn('already', r.json()['message'])

    def test_subscribe_missing_email(self):
        r = self.client.post(
            reverse('newsletter_subscribe'),
            json.dumps({'email': ''}),
            content_type='application/json'
        )
        self.assertFalse(r.json()['success'])
