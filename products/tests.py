from itertools import product
from django.test import TestCase
from products.models import Product
from users.models import User

class ProductRelationTest(TestCase):
    @classmethod    
    def setUpTestData(cls):
        cls.user = {
            'email': 'alexandre@mail.com',
            'first_name':'Alexandre',
            'last_name':'Araujo',
            'password': '12345',
            'is_seller': True
        }
        cls.seller = User.objects.create_user(**cls.user)

        cls.data = {
            'description': f'Teste {range(20)}',
            'price': 100.00,
            'quantity': 2,
            'seller': cls.seller
        }

        cls.products = [Product.objects.create(**cls.data) for _ in range(20)]


    def test_seller_contain_multiple_products(self):

        for product in self.products:
            product.seller = self.seller
            product.save()

        self.assertEquals(
            len(self.products),
            self.seller.products.count()
        )

        for product in self.products:
            self.assertIs(product.seller, self.seller)

    def test_product_cannot_belong_to_more_than_one_seller(self):
        for product in self.products:
            product.seller = self.seller
            product.save()

        user_2 = {
            'email': 'alexandra@mail.com',
            'first_name':'Alexandre',
            'last_name':'Araujo',
            'password': '12345',
            'is_seller': True
        }

        seller_two = User.objects.create_user(**user_2)

        for product in self.products:
            product.seller = seller_two
            product.save()

        for product in self.products:
            self.assertNotIn(product, self.seller.products.all())
            self.assertIn(product, seller_two.products.all())

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = {
            'email': 'alexandre@mail.com',
            'first_name':'Alexandre',
            'last_name':'Araujo',
            'password': '12345',
            'is_seller': True
        }

        cls.seller = User.objects.create_user(**cls.user)

        cls.data = {
            'description': 'Teste 1',
            'price': 100.00,
            'quantity': 2,
            'seller': cls.seller
        }

        cls.products = Product.objects.create(**cls.data)

    def test_description(self):
        product = Product.objects.get(pk=1)

        self.assertEquals(product.description, self.data["description"])

    def test_price(self):
        product = Product.objects.get(pk=1)

        decimal_places = product._meta.get_field('price').decimal_places
        max_digits = product._meta.get_field('price').max_digits

        self.assertEquals(decimal_places, 2)
        self.assertEquals(max_digits, 10)

    def test_quantity(self):
        product = Product.objects.get(pk=1)

        self.assertEquals(product.quantity, self.data["quantity"])

    def test_seller(self): 
        product = Product.objects.get(pk=1)

        self.assertEquals(product.seller, self.seller)
