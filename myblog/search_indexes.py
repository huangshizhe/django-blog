from haystack import indexes
from .models import Blogpost

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Blogpost

    def index_queryset(self, using=None):
        return self.get_model().objects.all()