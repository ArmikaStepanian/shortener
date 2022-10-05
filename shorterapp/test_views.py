from unittest import TestCase

from django.test.client import Client

from shorterapp.views import *


class Test(TestCase):
    def test_not_duplicated_combination(self):
        boolean1 = duplicated_combination('111fff555')
        self.assertFalse(boolean1, False)

    def test_duplicated_combination(self):
        boolean2 = duplicated_combination('gBjDrHC')
        self.assertTrue(boolean2, True)

    def test_long_url_not_exist(self):
        boolean1 = long_url_exist_in_db('just random string')
        self.assertFalse(boolean1, False)

    def test_long_url_exist(self):
        boolean2 = long_url_exist_in_db('https://www.w3schools.com/django/django_models.php')
        self.assertTrue(boolean2, True)

    def test_success_redirect(self):
        client = Client()
        response = client.post('http://localhost:8000/gBjDrHC')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.get('location'), 'https://www.w3schools.com/django/django_models.php')

    def test_fail_redirect(self):
        client = Client()
        response = client.post('http://localhost:8000/jkjkjkjk')

        self.assertEqual(response.status_code, 404)
