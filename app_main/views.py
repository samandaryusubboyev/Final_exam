from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Product, Category, Cart
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib import messages
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404

from django.core.paginator import Paginator


class CategoriesView(ListView):
    model = Category
    template_name = 'app_main/categories.html'
    paginator_class = Paginator
    context_object_name = 'categories'
    paginate_by = 3
    extra_context = {
        'is_search': True
    }

    def get_queryset(self):
        search = self.request.GET.get('q', '')

        if search:
            return Category.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        else:
            return Category.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']

        left_index = page_obj.number - 1
        right_index = page_obj.number + 1

        if left_index < 1:
            left_index = 1

        if right_index > page_obj.paginator.num_pages:
            right_index = page_obj.paginator.num_pages

        custom_range = range(left_index, right_index + 1)

        context['custom_range'] = custom_range

        return context


class ProductsView(ListView):
    model = Product
    template_name = 'app_main/index.html'
    context_object_name = 'products'
    paginator_class = Paginator
    paginate_by = 2

    def get_queryset(self):
        search = self.request.GET.get('q', '')
        category_id = self.kwargs.get('category_id')

        if search:
            return Product.objects.filter(
                Q(description__icontains=search) | Q(category__name__icontains=search)
            )
        else:
            return Product.objects.filter(category__id=category_id)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product = request.POST.get('product')

    context = {
        'product': product,
        'is_category_page': True,
    }
    return render(request, 'app_main/detail.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # `Product` modelidan obyektni olish
    cart, created = Cart.objects.get_or_create(
        user_id=request.user,
        product_id=product  # Model maydon nomiga mos
    )
    if not created:
        # Agar avvaldan mavjud bo'lsa, miqdorni oshiring
        cart.quantity += 1
        cart.save()
    return redirect('cart')



def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, product_id=product_id, user=request.user)

    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')


def change_product_cart(request, product_id, action):
    cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user)

    if action == 'increment':
        cart_item.quantity += 1

    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        elif cart_item.quantity == 1:
            cart_item.delete()
            return redirect('cart')

    else:
        raise Http404("Invalid action")
    cart_item.save()
    return redirect('cart')


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user_id=request.user.id)

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'app_main/cart.html', context)


@login_required
def update_account(request):
    user = request.user
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        password_confirmation = request.POST.get("password_confirmation", "").strip()

        # Formdagi ma'lumotlarni tekshirish
        if not first_name or not last_name or not email:
            messages.error(request, "All fields except password are required!")
            return redirect("update_account")

        if password and password != password_confirmation:
            messages.error(request, "Passwords do not match!")
            return redirect("update_account")

        try:
            # Foydalanuvchi ma'lumotlarini yangilash
            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            if password:  # Agar parol o'zgartirilayotgan bo'lsa
                user.set_password(password)

            user.save()
            messages.success(request, "Your account information has been updated successfully!")

            # Agar parol o'zgartirilgan bo'lsa, qaytadan login qilish kerak
            if password:
                return redirect("login")

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("update_account")

    # GET request uchun joriy ma'lumotlarni ko'rsatish
    context = {
        "user": user,
    }
    return render(request, "account/update_account.html", context)
