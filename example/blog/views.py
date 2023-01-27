from django.shortcuts import render

from blog.models import Article


def blog_index(request):
    articles = Article.objects.all()
    context = {
        "articles": articles,
    }
    return render(request, "blog/index.html", context)


def blog_article(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        "article": article,
    }
    return render(request, "blog/article.html", context)
