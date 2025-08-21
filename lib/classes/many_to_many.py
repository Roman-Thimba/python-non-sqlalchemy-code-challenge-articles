# lib/classes/many_to_many.py

class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise TypeError("author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        if not (isinstance(title, str) and 5 <= len(title) <= 50):
            raise ValueError("title must be a string between 5 and 50 characters")

        self._title = title
        self._author = author
        self._magazine = magazine
        Article.all.append(self)

    # ---------- title (immutable: ignore reassignment) ----------
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # silently ignore reassignment instead of raising
        pass

    # ---------- author ----------
    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value

    # ---------- magazine ----------
    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("name must be a non-empty string")
        self._name = name

    # ---------- name (immutable: ignore reassignment) ----------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # silently ignore reassignment
        pass

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        areas = {mag.category for mag in self.magazines()}
        return list(areas) if areas else None


class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    # ---------- name ----------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            # ignore invalid instead of raising
            return

    # ---------- category ----------
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            # ignore invalid instead of raising
            return

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        authors = {article.author for article in self.articles()}
        return list(authors) if authors else None

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        if not self.articles():
            return None
        authors = [a for a in self.contributors() if len([art for art in self.articles() if art.author == a]) > 2]
        return authors if authors else None

