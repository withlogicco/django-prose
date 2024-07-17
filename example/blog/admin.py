from django.contrib import admin

from blog.models import Article, Comment


class CommentAdminInline(admin.StackedInline):
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentAdminInline]


admin.site.register(Article, ArticleAdmin)
