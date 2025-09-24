from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from .models import Category, Product, Order, OrderItem


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        """Test category model creation."""
        category = Category.objects.create(
            name="Test Coffee",
            description="Test coffee description"
        )
        self.assertEqual(str(category), "Test Coffee")
        self.assertEqual(category.name, "Test Coffee")
        self.assertTrue(category.created_at)


class ProductModelTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Coffee",
            description="Coffee beverages"
        )
        
    def test_product_creation(self):
        """Test product model creation."""
        product = Product.objects.create(
            name="Test Espresso",
            description="Test espresso description",
            price=Decimal('2.50'),
            category=self.category,
            is_available=True
        )
        self.assertEqual(str(product), "Test Espresso - $2.50")
        self.assertTrue(product.is_available)
        self.assertEqual(product.category, self.category)


class OrderModelTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Coffee")
        self.product = Product.objects.create(
            name="Espresso",
            description="Strong coffee",
            price=Decimal('2.50'),
            category=self.category
        )
        
    def test_order_creation(self):
        """Test order model creation."""
        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com"
        )
        self.assertEqual(str(order), f"Order #{order.id} - John Doe - $0.00")
        self.assertEqual(order.status, 'pending')
        
    def test_order_with_items(self):
        """Test order with items calculation."""
        order = Order.objects.create(customer_name="Jane Doe")
        
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )
        
        self.assertEqual(order_item.get_total_price(), Decimal('5.00'))
        self.assertEqual(order.get_total_amount(), Decimal('5.00'))


class ViewsTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Coffee",
            description="Coffee beverages"
        )
        self.product = Product.objects.create(
            name="Espresso",
            description="Strong coffee",
            price=Decimal('2.50'),
            category=self.category,
            is_available=True
        )
        
    def test_home_view(self):
        """Test home page view."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Coffee Shop")
        self.assertContains(response, self.product.name)
        
    def test_product_list_view(self):
        """Test product list view."""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Our Menu")
        self.assertContains(response, self.product.name)
        
    def test_product_list_filtered_view(self):
        """Test product list view with category filter."""
        response = self.client.get(reverse('product_list'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.product.name)
        
    def test_product_detail_view(self):
        """Test product detail view."""
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        
    def test_cart_view(self):
        """Test cart view."""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shopping Cart")
        
    def test_checkout_view_empty_cart(self):
        """Test checkout view with empty cart redirects."""
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to cart
        
    def test_add_to_cart(self):
        """Test adding item to cart."""
        response = self.client.post(reverse('add_to_cart'), {
            'product_id': self.product.id,
            'quantity': 1
        })
        self.assertEqual(response.status_code, 200)
        
        # Check if item was added to session cart
        session = self.client.session
        cart = session.get('cart', {})
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)], 1)
