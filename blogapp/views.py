from django.shortcuts import render, get_object_or_404, redirect,Http404
from .models import author,category, article, comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import createForm, registerUser,createauthor,commentform,categoryForm
from django.contrib import messages


# Create your views here.

def index(request):
    post = article.objects.all()
    search=request.GET.get('q')
    if search:
        post=post.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)|
            Q(posted_on__icontains=search)
            
        )
    paginator = Paginator(post, 8) # Show 8 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        "post": total_article
    }
    return render(request, "index.html", context)

def getauthor(request, name):
    post_author=get_object_or_404(User, username=name)
    auth=get_object_or_404(author, name=post_author.id)
    post=article.objects.filter(article_author=auth.id)
    paginator = Paginator(post, 8)
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        "auth":auth,
        "post":total_article,
    }
    return render(request, "profile.html", context)

def getsingle(request, id):
    post = get_object_or_404(article, pk=id)
    first = article.objects.first()
    last = article.objects.last()
    getComment=comment.objects.filter(post=id)
    related = article.objects.filter(category=post.category).exclude(id=id)[:4]
    form=commentform(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.post=post
        instance.save()
    context = {
        "post":post,
        "first":first,
        "last":last,
        "related": related,
        "form":form,
        "comment":getComment,
    }
    return render(request, "single.html", context)

def gettopic(request, name):
    cat = get_object_or_404(category, name=name)
    post = article.objects.filter(category=cat.id)
    paginator = Paginator(post, 8) # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        "post":total_article,
        "cat":cat,
    }
    return render(request, "category.html", context)

def getlogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            user=request.POST.get('user')
            password=request.POST.get('pass')
            auth=authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Your password and username incorrect!')
    return render(request, "login.html")

def getlogout(request):
    logout(request)
    return redirect('index')

def getcreate(request):
    if request.user.is_authenticated:
        u=get_object_or_404(author, name=request.user.id)
        form=createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            inistance=form.save(commit=False)
            inistance.article_author=u
            inistance.save()
            messages.success(request, 'New Post create successfully!')
            return redirect('profile')
        context ={
            "form":form
        }
        return render(request, 'create.html', context)
    else:
        return redirect('login')

def getUpdate(request, pid):
    if request.user.is_authenticated:
        u=get_object_or_404(author, name=request.user.id)
        post=get_object_or_404(article, id=pid)
        form=createForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.article_author=u
            instance.save()
            messages.success(request, 'Update successfully!')
            return redirect('profile')
        return render(request, 'create.html', {"form":form})
    else:
        return redirect('login')
    
def getdelete(request, pid):
    if request.user.is_authenticated:
        post=get_object_or_404(article, id=pid)
        post.delete()
        messages.warning(request, 'Deleted successfully!')
        return redirect('profile')
    else:
        return redirect('login')

def getprofile(request):
    if request.user.is_authenticated:
        user=get_object_or_404(User, id=request.user.id)
        author_profile=author.objects.filter(name=user.id)
        if author_profile:
            authorUser=get_object_or_404(author, name=request.user.id)
            post=article.objects.filter(article_author=authorUser.id)
            return render(request, 'log_in_profile.html', {"post":post, "user":authorUser})
        else:
            form=createauthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.name=user
                instance.save()
                return redirect('profile')
            return render(request, 'createauthor.html', {'form':form})
    else:
        return redirect('login')

def getregister(request):
    form = registerUser(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request, 'Registration successfull compelete ')
        return redirect('login')
    return render(request, 'register.html', {"form":form})

def getcategory(request):
    quary=category.objects.all()
    return render(request, 'topics.html', {"topic": quary})

def createTopic(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form=categoryForm(request.POST or None)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.save()
                return redirect('category')
            return render(request, 'create_topics.html', {"form":form})
        else:
            raise Http404("You are not to authorized to access this page")
    else:
        return redirect('login')

def cdelete(request, pid):
    if request.user.is_authenticated:
        c=get_object_or_404(category, id=pid)
        c.delete()
        messages.warning(request, 'Deleted successfully!')
        return redirect('category')
    else:
        return redirect('category')

def cUpdate(request, pid):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:

            #u=get_object_or_404(category, name=request.id)
            post=get_object_or_404(category, id=pid)
            form=categoryForm(request.POST or None, instance=post)
            if form.is_valid():
                instance=form.save(commit=False)
                #instance.category=u
                instance.save()
                messages.success(request, 'Update successfully!')
                return redirect('category')
            return render(request, 'create_topics.html', {"form":form})
        else:
            raise Http404("You are not to authorized to access this page")
    else:
        return redirect('topics')
