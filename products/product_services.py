from .models import Product, Comment
from .forms import CommentForm
from profiles.models import Profile


def add_comment_to_product(user: Profile, form: CommentForm, obj: Product) -> Comment:
    comment = form.save(commit=False)
    comment.product = obj
    comment.author = user
    comment.save()
    return comment
