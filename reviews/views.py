from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product
from .models import Review
from .forms import ReviewForm


@login_required  # проверка на то, авторин ли польз
def add_review(request, product_id):
    """
    Добавляет отзыв на товар.

    Проверяет:
        - Авторизацию пользователя.
        - Не оставлял ли пользователь уже отзыв на этот товар.
        - Валидность данных формы.

    Args:
        request (HttpRequest): Объект запроса.
        product_id (int): ID товара для отзыва.

    Returns:
        HttpResponseRedirect: Редирект на страницу товара с сообщением.
    """
    product = get_object_or_404(Product, id=product_id)

    existing_review = Review.objects.filter(
        # проверка на вторичнсть отзыва
        product=product, user=request.user).first()
    if existing_review:
        messages.error(request, 'Вы уже оставили отзыв на этот товар')
        return redirect('catalog:product_detail', slug=product.slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # тут не сохраняем сразу тк не знаем сам продук и эзера из бд
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв добавлен!')
            return redirect('catalog:product_detail', slug=product.slug)
        else:
            messages.error(
                request, 'Пожалуйста, выберите оценку (от 1 до 5 звезд)')
            return redirect('catalog:product_detail', slug=product.slug)

    return redirect('catalog:product_detail', slug=product.slug)


@login_required
def delete_review(request, review_id):
    """
    Удаляет отзыв пользователя.

    Проверяет, что пользователь удаляет только свой собственный отзыв.

    Args:
        request (HttpRequest): Объект запроса.
        review_id (int): ID отзыва для удаления.

    Returns:
        HttpResponseRedirect: Редирект на страницу товара с сообщением.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'Отзыв удален!')
    return redirect('catalog:product_detail', slug=product_slug)
