from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count

from products.models import Product, Category, ProductImage
from orders.models import Order, OrderItem
from payments.models import Payment

from .forms import ProductForm
from products.imgbb import upload_to_imgbb


# =========================================================
# OWNER LOGIN
# =========================================================

def owner_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard_home")

    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("dashboard:dashboard_home")

    return render(
        request,
        "dashboard/login.html",
        {"form": form}
    )


# =========================================================
# OWNER LOGOUT
# =========================================================

@login_required
def owner_logout(request):
    logout(request)

    return redirect("dashboard:owner_login")


# =========================================================
# DASHBOARD HOME
# =========================================================

@login_required
def dashboard_home(request):

    completed_orders = Order.objects.filter(
        payment_status=Order.PAYMENT_COMPLETED
    )

    total_revenue = (
        completed_orders.aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        or 0.00
    )

    total_orders = Order.objects.count()

    total_products = Product.objects.count()

    pending_orders_count = Order.objects.filter(
        order_status=Order.STATUS_PENDING
    ).count()

    recent_orders = Order.objects.order_by(
        "-created_at"
    )[:8]

    context = {
        "total_revenue": int(total_revenue),
        "total_orders": total_orders,
        "total_products": total_products,
        "pending_orders_count": pending_orders_count,
        "recent_orders": recent_orders,
    }

    return render(
        request,
        "dashboard/home.html",
        context
    )


# =========================================================
# PRODUCT LIST
# =========================================================

@login_required
def product_list(request):

    products = Product.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "dashboard/products.html",
        {
            "products": products
        }
    )


# =========================================================
# ADD PRODUCT
# =========================================================

@login_required
def product_add(request):

    form = ProductForm()

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            # Save product information
            product = form.save()

            # Get uploaded image
            uploaded_image = request.FILES.get("image")

            if uploaded_image:

                try:

                    # Upload image to ImgBB
                    image_url = upload_to_imgbb(
                        uploaded_image
                    )

                    # Find next display order
                    last_image = (
                        ProductImage.objects
                        .filter(product=product)
                        .order_by("-display_order")
                        .first()
                    )

                    if last_image:
                        display_order = (
                            last_image.display_order + 1
                        )
                    else:
                        display_order = 1

                    # Save ImgBB URL in PostgreSQL
                    ProductImage.objects.create(
                        product=product,
                        image=image_url,
                        display_order=display_order
                    )

                except Exception as e:

                    # If ImgBB upload fails,
                    # remove the newly created product
                    product.delete()

                    form.add_error(
                        "image",
                        f"Image upload failed: {e}"
                    )

                    return render(
                        request,
                        "dashboard/product_form.html",
                        {
                            "form": form,
                            "title": "Add Product"
                        }
                    )

            return redirect(
                "dashboard:product_list"
            )

    return render(
        request,
        "dashboard/product_form.html",
        {
            "form": form,
            "title": "Add Product"
        }
    )


# =========================================================
# EDIT PRODUCT
# =========================================================

@login_required
def product_edit(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    form = ProductForm(
        instance=product
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            product = form.save()

            uploaded_image = request.FILES.get(
                "image"
            )

            if uploaded_image:

                try:

                    # Upload new image to ImgBB
                    image_url = upload_to_imgbb(
                        uploaded_image
                    )

                    # Find next display order
                    last_image = (
                        ProductImage.objects
                        .filter(product=product)
                        .order_by("-display_order")
                        .first()
                    )

                    if last_image:
                        display_order = (
                            last_image.display_order + 1
                        )
                    else:
                        display_order = 1

                    ProductImage.objects.create(
                        product=product,
                        image=image_url,
                        display_order=display_order
                    )

                except Exception as e:

                    form.add_error(
                        "image",
                        f"Image upload failed: {e}"
                    )

                    return render(
                        request,
                        "dashboard/product_form.html",
                        {
                            "form": form,
                            "product": product,
                            "title": "Edit Product"
                        }
                    )

            return redirect(
                "dashboard:product_list"
            )

    return render(
        request,
        "dashboard/product_form.html",
        {
            "form": form,
            "product": product,
            "title": "Edit Product"
        }
    )


# =========================================================
# DELETE PRODUCT
# =========================================================

@require_POST
@login_required
def product_delete(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    product.delete()

    return redirect(
        "dashboard:product_list"
    )


# =========================================================
# ORDER LIST
# =========================================================

@login_required
def order_list(request):

    orders = Order.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "dashboard/orders.html",
        {
            "orders": orders
        }
    )


# =========================================================
# ORDER STATUS UPDATE
# =========================================================

@require_POST
@login_required
def order_status_update(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk
    )

    new_status = request.POST.get(
        "status"
    )

    allowed_statuses = [
        Order.STATUS_PENDING,
        Order.STATUS_PACKED,
        Order.STATUS_SHIPPED,
        Order.STATUS_DELIVERED,
    ]

    if new_status in allowed_statuses:

        order.order_status = new_status

        order.save()

    return redirect(
        "dashboard:order_list"
    )


# =========================================================
# ANALYTICS
# =========================================================

@login_required
def analytics_view(request):

    completed_orders = Order.objects.filter(
        payment_status=Order.PAYMENT_COMPLETED
    )

    total_revenue = (
        completed_orders.aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        or 0.00
    )

    completed_count = completed_orders.count()

    average_order_value = (
        total_revenue / completed_count
        if completed_count > 0
        else 0
    )

    orders_by_status = (
        Order.objects
        .values("order_status")
        .annotate(count=Count("id"))
    )

    best_sellers = (
        OrderItem.objects
        .values(
            "product__name",
            "product__emoji",
            "product__category__name"
        )
        .annotate(
            units_sold=Sum("quantity"),
            sales=Sum("price")
        )
        .order_by("-units_sold")[:5]
    )

    context = {
        "total_revenue": int(total_revenue),
        "average_order_value": int(
            average_order_value
        ),
        "total_orders": Order.objects.count(),
        "orders_by_status": orders_by_status,
        "best_sellers": best_sellers,
    }

    return render(
        request,
        "dashboard/analytics.html",
        context
    )