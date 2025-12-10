from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв добавлен!')
            return redirect('product_detail', product_id=product.id)

    form = ReviewForm()
    return render(request, 'reviews/add_review.html', {
        'product': product,
        'form': form
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Отзыв удален!')
    return redirect('product_detail', product_id=product_id)