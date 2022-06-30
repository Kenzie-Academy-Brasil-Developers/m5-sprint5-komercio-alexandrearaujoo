from django.test import TestCase
from users.models import User
from products.models import Product


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