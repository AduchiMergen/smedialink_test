import os

from django.core import mail
from django.core.files import File
from django.test import TestCase, Client
from django.conf import settings

from partymaker.models import User, Order


class PartyMakerTests(TestCase):
    def setUp(self):
        self.file_path = os.path.join(settings.BASE_DIR,
                                      'partymaker', 'tests', 'files', 'test_pic.png')


    def test_auth_redirect(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/?next=/')
        response = client.get('/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/?next=/delete/')
        response = client.get('/list/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/?next=/list/')

    def test_empty_fields_auth(self):
        client = Client()
        response = client.post('/auth/?next=/', {'name': 'sdd'})
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertIn('photo', response.context_data['form'].errors)
        with open(self.file_path, 'rb') as fp:
            response = client.post('/auth/?next=/', {'photo': fp})
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertIn('name', response.context_data['form'].errors)
        response = client.post('/auth/?next=/', {})
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertIn('name', response.context_data['form'].errors)
        self.assertIn('photo', response.context_data['form'].errors)

    def test_new_user(self):
        client = Client()
        name = 'Test User'
        with open(self.file_path, 'rb') as fp:
            response = client.post('/auth/?next=/', {'name': name, 'photo': fp})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        User.objects.get(name=name)
        self.assertEqual(User.objects.count(), 1)

    def test_exists_user(self):
        name = 'Test User 2'
        User.objects.create(name=name)

        client = Client()
        with open(self.file_path, 'rb') as fp:
            response = client.post('/auth/?next=/', {'name': name, 'photo': fp})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        User.objects.get(name=name)
        self.assertEqual(User.objects.count(), 1)

    def test_empty_fields_order(self):
        client = Client()

        name = 'Test User'
        User.objects.create(name=name)
        client.login(name=name)

        response = client.post('/', {})
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertIn('is_member', response.context_data['form'].errors)
        self.assertIn('drink', response.context_data['form'].errors)

        response = client.post('/', {'is_member': 'True'})
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertIn('drink', response.context_data['form'].errors)

        response = client.post('/', {'drink': 1})
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertIn('is_member', response.context_data['form'].errors)

    def test_create_order(self):
        client = Client()

        name = 'Test User'
        User.objects.create(name=name)
        client.login(name=name)

        response = client.post('/', {'is_member': 'True', 'drink': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/delete/')
        self.assertEqual(Order.objects.count(), 1)
        response = client.post('/', {'is_member': 'False', 'drink': 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/delete/')
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.filter(is_member=True).count(), 1)

        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, '[Django] Пользователь создал приглашение')

    def test_delete_order(self):
        name = 'Test User'
        user = User.objects.create(name=name)
        Order.objects.create(user=user, is_member=True, drink=1)
        del mail.outbox[0]
        self.assertEqual(Order.objects.count(), 1)
        client = Client()
        client.login(name=name)
        client.post('/delete/', {})
        self.assertEqual(Order.objects.count(), 0)

        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, '[Django] Пользователь удалил приглашение')

    def test_admin_access(self):
        name = 'Test User'
        client = Client(REMOTE_ADDR='123.123.123.132')
        client.login(name=name)
        response = client.get('/list/')
        self.assertEqual(response.status_code, 401)
        client = Client(REMOTE_ADDR=settings.ADMIN_IP)
        client.login(name=name)
        response = client.get('/list/')
        self.assertEqual(response.status_code, 200)
