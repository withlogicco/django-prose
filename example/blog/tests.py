from django.test import TestCase
from django.contrib.auth.models import User
# internal imports
from blog.models import Article
from prose.models import Document


class ArticleModelTests(TestCase):
    def create_article(self, title: str, excerpt: str, body: str) -> Article:
        """Create a Article with the given informations."""
        body = Document.objects.create(content="test")
        return Article.objects.create(
            title=title, author=self.su, excerpt=excerpt, body=body)
    
    def test_article_is_in_db(self):
        """Article is in database and excerpt field is None."""
        # create fake superuser
        self.su = User.objects.create_superuser('admin',
                                                'fake@adminmail.com',
                                                'superpass')
        assert User.objects.count() == 1
        article = self.create_article(title="Test",
                                 excerpt=None,
                                 body="Test body.")
        assert isinstance(article, Article)
        article_in_db = Article.objects.all()[0]
        assert Article.objects.count() == 1
        self.assertQuerysetEqual([article_in_db], [article])
