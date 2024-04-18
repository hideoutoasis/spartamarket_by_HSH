# 임포트 확실히 설정해주고 가야함.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods


def index(request):
    return render(request, "index.html")


def products(request):
    products = Product.objects.all().order_by("-pk") 
    context = {
        "products":products,
    }
    return render(request, "products.html",context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comment_form = CommentForm()
    comments = product.comments.all().order_by("-pk") #최신순 정렬 잊지마
    context = {
        "product": product,
        "comment_form": comment_form,
        "comments": comments,
        }
    return render(request, "product_detail.html", context)


@login_required
def create(request):
    if request.method =="POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect("product_detail", product.pk)
    else:
        form = ProductForm()
        
    context = {"form": form}
        
    return render(request, "create.html", context)


@login_required
@require_http_methods(["GET","POST"])
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.author == request.user:
        if request.method == "POST":
            form = ProductForm(request.POST, instance = product)
            if form.is_valid():
                product = form.save()
                return redirect("product_detail", product.pk)
            
        else:
            form = ProductForm(instance = product)
    else:
        return redirect("products")
        
    context = {
        "form":form,
        "product":product,
        }
    return render(request, "update.html", context)


@require_POST
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk) # 이거 안빼주면 에러남
    if request.user.is_authenticated:
        if product.author == request.user:
            product = get_object_or_404(Product, pk=pk)
            product.delete()
    return redirect("products") # 삭제하면 어차피 목록으로 간다.
# 삭제 및 수정 시에는 메소드별 분기가 반드시 필요함.

@require_POST #댓글은 GET요청을 처리할 일이 없음.
def comment_create(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            return redirect("product_detail", product.pk)


@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect("product_detail", pk)


# 좋아요 기능
@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
        else:
            product.like_users.add(request.user)
        return redirect("products")
    return redirect("accounts:login")
