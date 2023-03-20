from django.test import TestCase
from django.contrib.auth.models import User

# internal imports
from blog.models import Article
from prose.models import Document


class ArticleModelTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.su = User.objects.create_superuser(
            "admin", "fake@adminmail.com", "superpass"
        )
        assert User.objects.count() == 1

    def create_article(self, title: str, excerpt: str | None, body: str) -> Article:
        """Create a Article with the given informations."""
        body = Document.objects.create(content="test body")
        return Article.objects.create(
            title=title, author=self.su, excerpt=excerpt, body=body
        )

    def test_article_is_in_db_with_none(self):
        """Article is in database and excerpt field is None."""
        excerpt = None
        article = self.create_article(title="Test", excerpt=excerpt, body="Test body.")
        assert isinstance(article, Article)
        assert article.excerpt == excerpt
        article_in_db = Article.objects.all()[0]
        assert Article.objects.count() == 1
        self.assertQuerysetEqual([article_in_db], [article])

    def test_article_is_in_db_with_empty_string(self):
        """Article is in database and excerpt field is empty string => ''."""
        excerpt = ""
        article = self.create_article(title="Test", excerpt=excerpt, body="Test body")
        assert isinstance(article, Article)
        assert article.excerpt == excerpt
        article_in_db = Article.objects.all()[0]
        assert Article.objects.count() == 1
        self.assertQuerysetEqual([article_in_db], [article])

    def test_article_is_in_db_with_string(self):
        """Article is in database and excerpt field is string => 'string'."""
        excerpt = "string"
        article = self.create_article(title="Test", excerpt=excerpt, body="Test body")
        assert isinstance(article, Article)
        assert article.excerpt == excerpt
        article_in_db = Article.objects.all()[0]
        assert Article.objects.count() == 1
        self.assertQuerysetEqual([article_in_db], [article])

    def test_article_is_in_db_correctly(self):
        """We test whether it is possible to have a string, empty string or None in RichTextField. RichTextField is an excerpt field in the Article model."""
        excerpt_list = ["string", "", None]
        for nr, excerpt in enumerate(excerpt_list, start=1):
            title = f"Test {nr}"
            body = f"Test body {nr}"
            article = self.create_article(title=title, excerpt=excerpt, body=body)
            assert isinstance(article, Article)
            assert article.excerpt == excerpt
            article_in_db = Article.objects.get(title=title)
            assert Article.objects.count() == nr
            self.assertQuerysetEqual([article_in_db], [article])
