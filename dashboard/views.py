import os
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count
from django.contrib import messages

from products.models import Product, ProductImage
from orders.models import Order, OrderItem

from .forms import ProductForm


# ============================================================
# IMGBB UPLOAD
# ============================================================

def upload_to_imgbb(uploaded_file):
    """
    Upload an image to ImgBB and return the public image URL.
    """

    api_key = os.getenv("IMGBB_API_KEY")

    if not api_key:
        raise ValueError(
            "IMGBB_API_KEY is missing. "
            "Add it to your environment variables."
        )

    try:
        uploaded_file.seek(0)

        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={
                "key": api_key,
            },
            files={
                "image": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.content_type,
                )
            },
            timeout=60,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        raise ValueError(
            f"Could not connect to ImgBB: {exc}"
        )

    try:
        data = response.json()
    except ValueError:
        raise ValueError(
            "ImgBB returned an invalid response."
        )

    if not data.get("success"):
        error_message = (
            data.get("error", {})
            .get("message", "ImgBB upload failed.")
        )

        raise ValueError(error_message)

    image_data = data.get("data", {})

    # Direct image URL
    image_url = image_data.get("url")

    if not image_url:
        # Fallback
        image_url = image_data.get("display_url")

    if not image_url:
        raise ValueError(
            "ImgBB uploaded the image but did not return an image URL."
        )

    return image_url


# ============================================================
# OWNER LOGIN
# ============================================================

def owner_login(request):

    if request.user.is_authenticated:
        return redirect("dashboard:dashboard_home")

    form = AuthenticationForm()

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect(
                "dashboard:dashboard_home"
            )

    return render(
        request,
        "dashboard/login.html",
        {
            "form": form
        }
    )


@login_required
def owner_logout(request):

    logout(request)

    return redirect(
        "dashboard:owner_login"
    )


# ============================================================
# DASHBOARD HOME
# ============================================================

@login_required
def dashboard_home(request):

    completed_orders = Order.objects.filter(
        payment_status=Order.PAYMENT_COMPLETED
    )

    total_revenue = (
        completed_orders.aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        or 0
    )

    total_orders = Order.objects.count()

    total_products = Product.objects.count()

    pending_orders_count = Order.objects.filter(
        order_status=Order.STATUS_PENDING
    ).count()

    recent_orders = (
        Order.objects
        .select_related()
        .order_by("-created_at")[:8]
    )

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


# ============================================================
# PRODUCT LIST
# ============================================================

@login_required
def product_list(request):

    products = (
        Product.objects
        .prefetch_related("images")
        .order_by("-created_at")
    )

    return render(
        request,
        "dashboard/products.html",
        {
            "products": products
        }
    )


# ============================================================
# ADD PRODUCT
# ============================================================

@login_required
def product_add(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            uploaded_image = request.FILES.get("image")

            # ------------------------------------------------
            # Upload image FIRST
            # ------------------------------------------------

            image_url = None

            if uploaded_image:

                try:

                    image_url = upload_to_imgbb(
                        uploaded_image
                    )

                except Exception as exc:

                    form.add_error(
                        "image",
                        f"Image upload failed: {exc}"
                    )

                    return render(
                        request,
                        "dashboard/product_form.html",
                        {
                            "form": form,
                            "title": "Add Product",
                        }
                    )

            # ------------------------------------------------
            # Save product
            # ------------------------------------------------

            product = form.save()

            # ------------------------------------------------
            # Save ImgBB URL
            # ------------------------------------------------

            if image_url:

                ProductImage.objects.create(
                    product=product,
                    image=image_url,
                    display_order=1
                )

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect(
                "dashboard:product_list"
            )

    else:

        form = ProductForm()

    return render(
        request,
        "dashboard/product_form.html",
        {
            "form": form,
            "title": "Add Product",
        }
    )


# ============================================================
# EDIT PRODUCT
# ============================================================

@login_required
def product_edit(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            uploaded_image = request.FILES.get("image")

            # ------------------------------------------------
            # Upload new image if provided
            # ------------------------------------------------

            if uploaded_image:

                try:

                    image_url = upload_to_imgbb(
                        uploaded_image
                    )

                except Exception as exc:

                    form.add_error(
                        "image",
                        f"Image upload failed: {exc}"
                    )

                    return render(
                        request,
                        "dashboard/product_form.html",
                        {
                            "form": form,
                            "product": product,
                            "title": "Edit Product",
                        }
                    )

                # Save product changes
                form.save()

                # ------------------------------------------------
                # Add new image
                # ------------------------------------------------

                ProductImage.objects.create(
                    product=product,
                    image=image_url,
                    display_order=1
                )

            else:

                # Save normal product changes
                form.save()

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect(
                "dashboard:product_list"
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "dashboard/product_form.html",
        {
            "form": form,
            "product": product,
            "title": "Edit Product",
        }
    )


# ============================================================
# DELETE PRODUCT
# ============================================================

@require_POST
@login_required
def product_delete(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    product.delete()

    messages.success(
        request,
        "Product deleted successfully."
    )

    return redirect(
        "dashboard:product_list"
    )


# ============================================================
# ORDERS
# ============================================================

@login_required
def order_list(request):

    orders = (
        Order.objects
        .order_by("-created_at")
    )

    return render(
        request,
        "dashboard/orders.html",
        {
            "orders": orders
        }
    )


# ============================================================
# UPDATE ORDER STATUS
# ============================================================

@require_POST
@login_required
def order_status_update(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk
    )

    new_status = request.POST.get("status")

    valid_statuses = [
        Order.STATUS_PENDING,
        Order.STATUS_PACKED,
        Order.STATUS_SHIPPED,
        Order.STATUS_DELIVERED,
    ]

    if new_status in valid_statuses:

        order.order_status = new_status

        order.save()

        messages.success(
            request,
            "Order status updated."
        )

    return redirect(
        "dashboard:order_list"
    )


# ============================================================
# ANALYTICS
# ============================================================

@login_required
def analytics_view(request):

    completed_orders = Order.objects.filter(
        payment_status=Order.PAYMENT_COMPLETED
    )

    total_revenue = (
        completed_orders.aggregate(
            Sum("total_amount")
        )["total_amount__sum"]
        or 0
    )

    completed_count = completed_orders.count()

    if completed_count > 0:
        average_order_value = (
            total_revenue / completed_count
        )
    else:
        average_order_value = 0

    orders_by_status = (
        Order.objects
        .values("order_status")
        .annotate(
            count=Count("id")
        )
        .order_by("order_status")
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