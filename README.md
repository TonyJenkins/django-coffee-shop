# Coffee Shop Django Application

A Django web application for managing a small coffee shop, built with Bulma CSS framework for modern and responsive styling.

## Features

- 🏠 **Home Page**: Welcoming landing page with featured products and categories
- ☕ **Product Management**: Organized catalog with categories (Coffee, Pastries, Sandwiches)
- 🛒 **Shopping Cart**: Session-based cart functionality
- 📋 **Order Management**: Complete order processing system
- 💳 **Checkout Process**: Customer information and order confirmation
- 📱 **Responsive Design**: Mobile-friendly interface using Bulma CSS
- 🎨 **Modern UI**: Clean, professional design with coffee shop theming
- 👨‍💼 **Admin Interface**: Django admin for managing products, orders, and categories

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bulma CSS Framework
- **Database**: SQLite (development)
- **Icons**: Font Awesome
- **Images**: Unsplash (demo images)

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TonyJenkins/fictional-potato.git
   cd fictional-potato
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create sample data** (optional):
   ```bash
   python manage.py shell < /tmp/create_sample_data.py
   ```

5. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### Customer Features

- **Browse Menu**: View all products or filter by category
- **Product Details**: Detailed view of each product with pricing
- **Shopping Cart**: Add/remove items, adjust quantities
- **Checkout**: Place orders with customer information
- **Order Confirmation**: View order details and status

### Admin Features

- **Product Management**: Add, edit, and manage products
- **Category Management**: Organize products into categories
- **Order Management**: View and update order statuses
- **Customer Management**: View order history and customer details

## Project Structure

```
fictional-potato/
├── coffeeshop/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/                # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL patterns
│   ├── admin.py         # Admin configuration
│   ├── tests.py         # Test cases
│   └── templates/       # HTML templates
│       └── shop/
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## Models

### Category
- Organizes products into logical groups
- Fields: name, description, created_at

### Product
- Represents coffee shop items
- Fields: name, description, price, category, image, is_available

### Order
- Customer orders with status tracking
- Fields: customer_name, customer_email, status, total_amount

### OrderItem
- Individual items within an order
- Fields: order, product, quantity, price

## API Endpoints

- `/` - Home page
- `/products/` - Product catalog
- `/product/<id>/` - Product detail
- `/cart/` - Shopping cart
- `/checkout/` - Checkout process
- `/add-to-cart/` - Add item to cart (AJAX)
- `/remove-from-cart/` - Remove item from cart (AJAX)
- `/update-cart/` - Update cart quantities (AJAX)

## Testing

Run the test suite:

```bash
python manage.py test shop
```

The test suite includes:
- Model validation tests
- View response tests
- Shopping cart functionality tests
- Order processing tests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## License

This project is developed for demonstration purposes.

## Screenshots

The application features:
- Responsive home page with hero section and product cards
- Filterable product catalog with category navigation
- Shopping cart with quantity management
- Clean checkout process with order confirmation
- Mobile-friendly design throughout

---

Built with ❤️ using Django and Bulma CSS