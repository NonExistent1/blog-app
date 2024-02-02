from django.views.generic import ListView
from .models import Post
class BlogListView(ListView):
    """Blog list view"""

    model = Post
    template_name = "home.html"
