from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentAddForm, QuestionForm
from catalogue.models import Product
from .models import Comment


@login_required
def comment_add(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        form = CommentAddForm(request.POST)
        if form.is_valid():
            form.save(request.user, product)
            return redirect('catalogue:product_detail', product.slug)
    else:
        product = get_object_or_404(Product, id=product_id)
        form = CommentAddForm()
    return render(request, 'comment/add_comment.html', {"form": form, "product": product})


# def question_add(request, product_id):
#     if request.method == 'POST':
#         pass
#     else:
#         form = QuestionForm()
#     return render(request, 'comment/add_question.html', {"form": form})
