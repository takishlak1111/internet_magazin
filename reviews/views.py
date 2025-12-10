
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, не оставлял ли пользователь уже отзыв
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.error(request, 'Вы уже оставили отзыв на этот товар')
        return redirect('catalog:product_detail', slug=product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв добавлен!')
            return redirect('catalog:product_detail', slug=product.slug)
        else:
            # Если форма не валидна, показываем ошибку
            messages.error(request, 'Пожалуйста, выберите оценку (от 1 до 5 звезд)')
            return redirect('catalog:product_detail', slug=product.slug)
    
    # Если GET-запрос (кто-то перешел по ссылке), просто перенаправляем на товар
    return redirect('catalog:product_detail', slug=product.slug)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Отзыв удален!')
    return redirect('catalog:product_detail', slug=product_slug)