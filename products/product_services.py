from django.db.models import QuerySet

from .models import Product, Comment
from .forms import CommentForm
from profiles.models import Profile
from django.core.cache import cache


def add_comment_to_product(user: Profile, form: CommentForm, obj: QuerySet) -> Comment:
    comment = form.save(commit=False)
    comment.product = obj
    comment.author = user
    comment.save()
    return comment


def get_cashed_products(key: str, queryset: QuerySet) -> QuerySet:
    cached_queryset = cache.get(key)
    if cached_queryset is not None:
        return cached_queryset
    cache.set(key, queryset)
    return queryset
