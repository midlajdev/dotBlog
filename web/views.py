from django.shortcuts import get_object_or_404,render
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.core.paginator import Paginator
from django.http import Http404


def index(request):
    #added this line for getting data from posts/model and show in index.html
    posts = Post.objects.filter(is_draft=False).order_by('-created_at')
    
    # Paginate — 5 posts per page (you can change this)
    paginator = Paginator(posts, 6)
    
     # Get current page number from URL ?page=2
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'web/index.html', {'page_obj': page_obj})


def post_detail(request,slug):
    post_obj = get_object_or_404(Post,slug = slug)
    return render(request, 'web/post.html',{'post':post_obj})



def custom_404(request, exception=None):
    """
    Custom 404 handler
    """
    return render(request, '404.html', status=404)

def test_404(request):
    """
    View to test 404 page - visit /test-404/ to see your custom page
    """
    raise Http404("This is a test 404 page")