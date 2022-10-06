from unittest import TestCase

from django.test.client import Client

from shorterapp.views import *


class Test(TestCase):
    def test_not_duplicated_combination(self):
        # value 111fff555 doesnt exist in database
        boolean1 = duplicated_combination('111fff555')
        self.assertFalse(boolean1, False)

    def test_duplicated_combination(self):
        # value gBjDrHC exists in database
        boolean2 = duplicated_combination('gBjDrHC')
        self.assertTrue(boolean2, True)

    def test_long_url_not_exist(self):
        # url 'just random string' doesnt exist in database
        boolean1 = long_url_exist_in_db('just random string')
        self.assertFalse(boolean1, False)

    def test_long_url_exist(self):
        boolean2 = long_url_exist_in_db('https://www.w3schools.com/django/django_models.php')
        # url https://www.w3schools.com/django/django_models.php exists in database
        self.assertTrue(boolean2, True)

    def test_success_redirection(self):
        client = Client()
        # url http://localhost:8000/gBjDrHC exists in database
        # and redirect to https://www.w3schools.com/django/django_models.php
        response = client.post('http://localhost:8000/gBjDrHC')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertEqual(response.get('location'), 'https://www.w3schools.com/django/django_models.php')

    def test_fail_redirection(self):
        client = Client()
        # url http://localhost:8000/jkjkjkjk doesnt exist in database
        # and service returns Not found 404
        response = client.post('http://localhost:8000/jkjkjkjk')

        self.assertEqual(response.status_code, 404)



