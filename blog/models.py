from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Model manager for public posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self) \
            .get_queryset() \
            .filter(status='published')


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250,
                            unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    # display_posts shows all posts for the selected tag
    def display_posts(self):
        return ', '.join(tag.title for tag in self.tag.all()[:10])

    display_posts.short_description = 'Tag'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tag = models.ManyToManyField(Tag,
                                 blank=True,
                                 related_name='tag')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # Adding a canonical address for the model
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    # display_tag shows all tags for the selected post
    def display_tag(self):
        return ', '.join(tag.name for tag in self.tag.all()[:3])

    display_tag.short_description = 'Tag'


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment added by {} for the post {}'.format(self.name, self.post)
