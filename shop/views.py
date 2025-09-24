from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Category, Product, Order, OrderItem


def home(request):
    """Home page view displaying featured products."""
    featured_products = Product.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'shop/home.html', context)


def product_list(request):
    """Display all available products by category."""
    category_id = request.GET.get('category')
    products = Product.objects.filter(is_available=True)
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    categories = Category.objects.all()
    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """Display detailed view of a single product."""
    product = get_object_or_404(Product, pk=pk, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)


def cart_view(request):
    """Display shopping cart contents."""
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_available=True)
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
            total += item_total
        except Product.DoesNotExist:
            continue
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)


@require_POST
def add_to_cart(request):
    """Add a product to the shopping cart."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not product_id:
        return JsonResponse({'error': 'Product ID required'}, status=400)
    
    try:
        product = Product.objects.get(id=product_id, is_available=True)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart
    
    return JsonResponse({
        'success': True,
        'message': f'{product.name} added to cart',
        'cart_count': sum(cart.values())
    })


@require_POST
def remove_from_cart(request):
    """Remove a product from the shopping cart."""
    product_id = request.POST.get('product_id')
    
    if not product_id:
        return JsonResponse({'error': 'Product ID required'}, status=400)
    
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
    
    return JsonResponse({
        'success': True,
        'message': 'Item removed from cart',
        'cart_count': sum(cart.values())
    })


@require_POST
def update_cart(request):
    """Update quantity of a product in the cart."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 0))
    
    if not product_id:
        return JsonResponse({'error': 'Product ID required'}, status=400)
    
    cart = request.session.get('cart', {})
    
    if quantity <= 0:
        if product_id in cart:
            del cart[product_id]
    else:
        cart[product_id] = quantity
    
    request.session['cart'] = cart
    
    return JsonResponse({
        'success': True,
        'cart_count': sum(cart.values())
    })


def checkout(request):
    """Checkout page for placing an order."""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_available=True)
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total,
            })
            total += item_total
        except Product.DoesNotExist:
            continue
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email', '')
        
        if not customer_name:
            messages.error(request, 'Customer name is required.')
        else:
            # Create order
            order = Order.objects.create(
                customer_name=customer_name,
                customer_email=customer_email,
                total_amount=total
            )
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )
            
            # Clear cart
            request.session['cart'] = {}
            messages.success(request, f'Order #{order.id} placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'shop/checkout.html', context)


def order_confirmation(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'shop/order_confirmation.html', context)
