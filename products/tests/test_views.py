from rest_framework.test import APITestCase
from users.models import User
from rest_framework.authtoken.models import Token 
from products.models import Product
from faker import Faker

class ProductViewsTest(APITestCase):
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

        cls.seller_2 = {
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

        cls.user_1 = User.objects.create_user(**cls.seller)
        cls.user_2 = User.objects.create_user(**cls.not_seller)
        cls.user_3 = User.objects.create_user(**cls.seller_2)

        cls.token = Token.objects.create(user=cls.user_1)
        cls.token_2 = Token.objects.create(user=cls.user_2)
        cls.token_3 = Token.objects.create(user=cls.user_3)
        
        cls.prod = {
            "description": 'Produto 01',
            "price": 100.10,
            "quantity": 5,
        }

        cls.product = Product(**cls.prod) 

    def test_create_product_being_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.prod['seller'] = self.user_1.id

        response = self.client.post('/api/products/', self.prod, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['seller'])

    def test_create_product_not_being_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_2.key)

        self.prod['seller'] = self.user_2.id

        response = self.client.post('/api/products/', self.prod, format='json')

        message = 'You do not have permission to perform this action.'

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data['detail'])
        self.assertEqual(response.json()['detail'], message)

    def test_create_product_with_invalid_keys(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        product = {"descritpion": 'Teste errado'}

        self.prod['seller'] = self.user_1.id

        response = self.client.post('/api/products/', product, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.data['description'])
        self.assertTrue(response.data['price'])
        self.assertTrue(response.data['quantity'])

    def test_create_product_whith_nagative_quantity(self): 
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        prod = {
            "description": 'Produto 01',
            "price": 100.10,
            "quantity": -1,
        }
        prod['seller'] = self.user_1.id

        response = self.client.post('/api/products/', prod, format='json')

        message = ['Ensure this value is greater than or equal to 0.']

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.data['quantity'])
        self.assertEqual(response.json()['quantity'], message)

    def test_list_all_products(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.prod['seller'] = self.user_1.id

        self.client.post('/api/products/', self.prod, format='json')

        products = Product.objects.all()

        response = self.client.get('/api/products/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(products), len(response.data))
        
    def test_update_product_being_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.prod['seller'] = self.user_1.id

        self.client.post('/api/products/', self.prod, format='json')

        patch_data = {
            'description': "Produto 02",
            'price': "101.10",
            'quantity': 10
        }

        response = self.client.patch('/api/products/1/', patch_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['is_active'])
        self.assertEqual(response.data['description'], patch_data['description'])
        self.assertEqual(response.data['price'], patch_data['price'])
        self.assertEqual(response.data['quantity'], patch_data['quantity'])

    def test_update_product_not_being_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_2.key)

        self.prod['seller'] = self.user_1.id

        self.client.post('/api/products/', self.prod, format='json')

        patch_data = {
            'description': "Produto 02",
            'price': "101.10",
            'quantity': 10
        }

        response = self.client.patch('/api/products/1/', patch_data, format='json')

        message = 'You do not have permission to perform this action.'

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data['detail'])
        self.assertEqual(response.json()['detail'], message)

    def test_update_prodcut_not_being_owner(self): 
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.prod['seller'] = self.user_1.id

        self.client.post('/api/products/', self.prod, format='json')

        patch_data = {
            'description': "Produto 02",
            'price': "101.10",
            'quantity': 10
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_3.key)

        response = self.client.patch('/api/products/1/', patch_data, format='json')

        message = 'You do not have permission to perform this action.'

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data['detail'])
        self.assertEqual(response.json()['detail'], message)