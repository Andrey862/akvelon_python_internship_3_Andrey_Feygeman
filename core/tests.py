import json
from datetime import date
from django.conf.urls import url

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import response
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.urls import reverse

from .models import Transaction
from .utils import fibonacci


class TransactionTestCase(APITestCase):

    def setUp(self):
        self.username1 = "john"
        self.username2 = "Anton"
        self.email1 = "john@snow.com"
        self.email2 = "Anton@snow.com"
        self.password = "you_know_nothing"

        self.user1 = User.objects.create_user(
            self.username1, self.email1, self.password)
        self.user2 = User.objects.create_user(
            self.username2, self.email2, self.password)

        self.transaction1 = Transaction.objects.create(
            date=date(2021, 6, 1), amount=100.55, owner=self.user1)
        self.transaction2 = Transaction.objects.create(
            date=date(2021, 6, 1), amount=-50.55, owner=self.user1)

        self.transaction3 = Transaction.objects.create(
            date=date(2021, 6, 1), amount=100.55, owner=self.user2)
        self.transaction4 = Transaction.objects.create(
            date=date(2021, 6, 1), amount=-50.55, owner=self.user2)

        self.client.login(username=self.username1, password=self.password)

        self.list_url = reverse('transaction-list')
        self.detail_url = reverse(
            'transaction-detail', args=[self.transaction1.pk])
        self.other_user_detail_url = reverse(
            'transaction-detail', args=[self.transaction3.pk])
        self.group_url = reverse('transaction-group-by-day')
        self.content = {'date': date(2021, 6, 1), 'amount': -50.55}
        self.bad_content = {'defenetly not existing field': 'bad value'}

    def test_type_is_correct(self):
        self.assertEqual(self.transaction1.type,  'income')
        self.assertEqual(self.transaction2.type,  'outcome')

    def test_transactions_get_accessable(self):
        response = self.client.get(self.list_url)
        self.assertEqual(200, response.status_code)
        response = self.client.get(self.detail_url)
        self.assertEqual(200, response.status_code)

    def test_transactions_post_accessable(self):
        response = self.client.post(self.list_url, self.content)
        self.assertEqual(201, response.status_code)

    def test_transactions_put_patch_accessable(self):
        response = self.client.put(
            self.detail_url, self.content)
        self.assertEqual(200, response.status_code)
        response = self.client.patch(
            self.detail_url, self.content)
        self.assertEqual(200, response.status_code)

    def test_transactions_delete_accessable(self):
        response = self.client.delete(self.detail_url, self.content)
        self.assertEqual(204, response.status_code)

    def test_transactions_post_wrong_argument(self):
        response = self.client.post(self.list_url, self.bad_content)
        self.assertEqual(400, response.status_code)

    def test_transactions_access_access_others_transactions(self):
        response = self.client.get(self.other_user_detail_url)
        self.assertEqual(404, response.status_code)

    def test_group_transactions_accessable_and_correct(self):
        response = self.client.get(self.group_url)
        self.assertEqual(200, response.status_code)

        the_date = str(date(2021, 6, 1))
        sum = 100.55 + -50.55
        data = json.loads(response.content)
        # found content.date == the_date and extract amoiunt
        data_amount = float([e['sum']
                            for e in data if e['date'] == the_date][0])
        self.assertEqual(data_amount, sum)

    def test_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.list_url)
        self.assertEqual(403, response.status_code)


class FibonachiTransactionTestCase(APITestCase):
    url = reverse('fibonacci')

    def test_accesable(self):
        response = self.client.put(
            self.url, data={'n': 1000})
        self.assertEqual(200, response.status_code)

    def test_n_less_than_0(self):
        response = self.client.put(
            self.url, data={'n': -3})
        self.assertEqual(400, response.status_code)


class MiscellanyTest(TestCase):
    def test_fibonachi_less_than_0(self):
        self.assertRaises(ValueError, fibonacci, -1)
        self.assertRaises(ValueError, fibonacci, -2)

    def dumb_fibonachi(self, n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        return self.dumb_fibonachi(n-1) + self.dumb_fibonachi(n-2)

    def test_fibonachi_is_correct(self):
        self.assertEqual(fibonacci(3), self.dumb_fibonachi(3))
        self.assertEqual(fibonacci(5), self.dumb_fibonachi(5))
        self.assertEqual(fibonacci(8), self.dumb_fibonachi(8))
