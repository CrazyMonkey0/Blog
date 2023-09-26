from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


# News feed for blog posts
class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = '/blog/'
    description = 'New posts in my blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
