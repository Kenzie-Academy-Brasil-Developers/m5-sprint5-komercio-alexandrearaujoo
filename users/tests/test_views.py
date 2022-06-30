from rest_framework.test import APITestCase
from users.models import User
from faker import Faker

class UserViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()

        cls.seller = {
	        "email": cls.fake.email(),
	        "first_name": cls.fake.first_name_male(),
	        "last_name": cls.fake.last_name_male(),
	        "password": cls.fake.password(),
	        "is_seller": True
        }

        cls.not_seller = {
	        "email": cls.fake.email(),
	        "first_name": cls.fake.first_name_male(),
	        "last_name": cls.fake.last_name_male(),
	        "password": cls.fake.password(),
	        "is_seller": False
        }

        cls.user_1 = User(**cls.seller)
        cls.user_2 = User(**cls.not_seller)

    def test_can_create_seller(self):
        response = self.client.post('/api/accounts/', self.seller, format='json')
        expected = {
            "email": self.seller['email'],
            "first_name": self.seller['first_name'],
            "last_name": self.seller['last_name'],
            "is_seller": self.seller['is_seller'],
            "date_joined": response.data["date_joined"]
        }

        self.assertEqual(response.status_code, 201)
        self.assertEquals(response.data, expected)

    def test_can_create_not_seller(self):
        response = self.client.post('/api/accounts/', self.not_seller, format='json')

        expected = {
            "email": self.not_seller['email'],
            "first_name": self.not_seller['first_name'],
            "last_name": self.not_seller['last_name'],
            "is_seller": self.not_seller['is_seller'],
            "date_joined": response.data["date_joined"]
        }
    
        self.assertEqual(response.status_code, 201)
        self.assertEquals(response.data, expected)

    def test_create_user_with_same_email(self):
        self.client.post('/api/accounts/', self.seller, format='json')

        response = self.client.post('/api/accounts/', self.seller, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.data['email'])

    def test_can_list_all_users(self):
        self.user_1.save()
        self.user_2.save()

        users = User.objects.all()

        response = self.client.get('/api/accounts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), len(response.json()['results']))

    def test_list_users_by_date_joined(self):
        self.user_1.save()
        self.user_2.save()

        users = User.objects.all()

        response = self.client.get('/api/accounts/newest/2/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(users), len(response.json()['results']))


    def test_send_invalid_keys_seller(self):
        invalid_user = {
            "email": self.fake.email(),
            "first_name": self.fake.first_name_male(),
            "last_name": self.fake.last_name_male()
        }

        response = self.client.post('/api/accounts/', invalid_user, format='json')


        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.data['password'])
        self.assertTrue(response.data['is_seller'])

    def test_login_seller(self):
        post_user = self.client.post('/api/accounts/', self.seller, format='json')

        data = {
            "email": post_user.data['email'],
            "password": self.user_1.password
        }

        response = self.client.post('/api/login/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['token'])

    def test_login_not_seller(self):
        post_user_2 = self.client.post('/api/accounts/', self.not_seller, format='json')

        data = {
            "email": post_user_2.data['email'],
            "password": self.user_2.password
        }

        response = self.client.post('/api/login/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['token'])

    def test_login_with_invalid_keys(self):
        post_user_2 = self.client.post('/api/accounts/', self.not_seller, format='json')

        data = {    
            "email": post_user_2.data['email'],
            "password": self.user_1.password
        }

        response = self.client.post('/api/login/', data, format='json')

        message = 'invalid email or password'

        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.data['detail'])
        self.assertEqual(response.json()['detail'], message)

    def test_update_user(self):
        post_user_1 = self.client.post('/api/accounts/', self.seller, format='json')

        login_data = {
            "email": post_user_1.data['email'],
            "password": self.user_1.password
        }

        login = self.client.post('/api/login/', login_data, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login.data['token'])

        patch_data = {
            "first_name": self.fake.first_name_female(),
            "last_name": self.fake.last_name_female()
        }

        response = self.client.patch('/api/accounts/1/', patch_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['first_name'], patch_data['first_name'])
        self.assertEquals(response.data['last_name'], patch_data['last_name'])

    def test_update_not_owner_user(self):
        self.client.post('/api/accounts/', self.seller, format='json')
        post_user_2 = self.client.post('/api/accounts/', self.not_seller, format='json')

        login_data = {
            "email": post_user_2.data['email'],
            "password": self.user_2.password
        }

        login = self.client.post('/api/login/', login_data, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login.data['token'])

        patch_data = {
            "first_name": self.fake.first_name_female(),
            "last_name": self.fake.last_name_female()
        }

        response = self.client.patch('/api/accounts/1/', patch_data, format='json')

        message = 'You do not have permission to perform this action.'

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data['detail'])
        self.assertEqual(response.json()['detail'], message)

    def test_update_is_active_key(self):
        post_user = self.client.post('/api/accounts/', self.not_seller, format='json')

        login_data = {
            "email": post_user.data['email'],
            "password": self.user_2.password
        }

        login = self.client.post('/api/login/', login_data, format='json')  

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login.data['token'])

        patch_data = {
            "is_active": False
        }

        response = self.client.patch('/api/accounts/1/', patch_data, format='json')

        message = 'You do not have permission to perform this action.' 

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data['detail'])
        self.assertEqual(response.json()['detail'], message)