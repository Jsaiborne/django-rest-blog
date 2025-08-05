
from django.urls import path


from home.views import BlogView, PublicBlog
urlpatterns = [
    path('blog/', BlogView.as_view()),
    path('public_blog/', PublicBlog.as_view()),
    
]
