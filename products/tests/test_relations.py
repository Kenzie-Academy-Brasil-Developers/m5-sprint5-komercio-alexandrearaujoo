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