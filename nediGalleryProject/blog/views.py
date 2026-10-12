from django.db.models import Q
from django.views.generic import ListView, DetailView
from nediGalleryProject.blog.models import Blog

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog-list.html'
    context_object_name = 'blogs'
    paginate_by = 6 

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog-single.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.object

        older_posts = Blog.objects.filter(
            Q(published__lt=blog.published)
            | Q(published=blog.published, pk__lt=blog.pk)
        )
        newer_posts = Blog.objects.filter(
            Q(published__gt=blog.published)
            | Q(published=blog.published, pk__gt=blog.pk)
        )

        context['previous_blog'] = older_posts.order_by(
            '-published', '-pk'
        ).first()
        context['next_blog'] = newer_posts.order_by(
            'published', 'pk'
        ).first()
        context['latest_blogs'] = Blog.objects.order_by(
            '-published', '-pk'
        )[:3]
        return context

    def get_queryset(self):
        return super().get_queryset().filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )