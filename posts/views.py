from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import postForm
from django.http import JsonResponse
from django.urls import reverse
from posts.models import Post
from django.shortcuts import get_object_or_404
# Create your views here.

@login_required(login_url = 'users:login')
def create_view(request):
    if request.method == 'POST':
        form = postForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # return redirect('web:index')
            return JsonResponse({
                'status': 'success',
                'message': 'Post created successfully!',
                'redirect': 'yes',
                'redirect_url':  reverse('web:index')
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Form is invalid!',
            })
        
    else:
        form = postForm()
    
    return render(request, 'posts/create.html', {'form':form})


@login_required(login_url = 'users:login')
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('created_at')
    return render(request,'posts/my-posts.html',{'posts':posts})



@login_required
def delete_post(request, slug):
    if request.method in ['POST','GET']:
        try:
            post = get_object_or_404(Post,slug=slug)
            post.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Post deleted successfully!',
                'title': 'Deleted',
                'redirect': 'yes',
                'redirect_url': '/my-posts/'
            })
        except Exception as e:
            print("DELETE ERROR:", e)
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request method'
        })


@login_required(login_url="/users/login/")
def draft_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Toggle draft status
    post.is_draft = not post.is_draft
    post.save()

    return JsonResponse({
        "title": "Success",
        "message": "Post draft status updated successfully",
        "status": "success",
        "redirect": "yes",
        "redirect_url" : "/",
    })

@login_required(login_url="/users/login/")
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = postForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Save form but preserve existing image if no new file uploaded
            instance = form.save(commit=False)
            if 'featured_image' in request.FILES and request.FILES.get('featured_image'):
                # new file uploaded -> use it (form will have set it already, but ensure instance gets it)
                instance.featured_image = request.FILES['featured_image']
            else:
                # no new file uploaded -> keep the current image
                instance.featured_image = post.featured_image

            # persist changes
            instance.save()
            response_data = {
                "title": "Successful",
                "message": "Post updated successfully!",
                "status": "success",
                "redirect": "yes",
                "redirect_url": "/"
            }
        else:
            response_data = {
                "title": "Error occurred",
                "message": form.errors,
                "status": "error",
                "stable": "yes"
            }
        return JsonResponse(response_data)

    else:
        form = postForm(instance=post)

    context = {
        "title": "Edit Post",
        "form": form,
        "post": post
    }
    return render(request, 'posts/create.html', context)
