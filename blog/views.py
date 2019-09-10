from .forms import PostForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from blog.models import Post, Author, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


def index(request):
    """ View function for home page of site."""
    num_posts = Post.objects.all().count()
    num_bloggers = Author.objects.all().count()
    num_comments = Comment.objects.all().count()

    context = {
        'num_posts': num_posts,
        'num_bloggers': num_bloggers,
        'num_comments': num_comments
    }
    return render(request, 'index.html', context=context)


class PostListView(generic.ListView):
    model = Post


class PostDetailView(generic.DetailView):
    model = Post

    # def get_context_data(self, **kwargs):
    #     """
    #     Add Comment to the context so they can be displayed in the template.
    #     """
    #     context = super(PostDetailView, self).get_context_data(**kwargs)
    #     context['comment'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
    #     return context


class AuthorListView(generic.ListView):
    model = Author


class PostListbyAuthorView(generic.ListView):
    model = Post
    template_name = 'blog/author_detail.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_author = get_object_or_404(Author, pk=id)
        return Post.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        """
        Add Author to the context so they can be displayed in the template
        """
        context = super(PostListbyAuthorView, self).get_context_data(**kwargs)
        context['author'] = get_object_or_404(Author, pk=self.kwargs['pk'])
        return context


class CommentCreate(PermissionRequiredMixin, CreateView):
    model = Comment
    fields = ['comment']
    permission_required = 'blog.can_write_comment'

    def get_context_data(self, **kwargs):
        """ Add associated post to form template so can discplay its title in HTML """
        context = super(CommentCreate, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """ Add author and associated blog to form data before setting it as valid (so it is saved to model) """
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk'], })


@permission_required('blog.can_write_post')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.post_date = timezone.now()
            post.author = Author.objects.get(user=request.user)
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})


# def comment_new(request):
#     # post_instance = get_object_or_404(Post, pk=pk)
#     # print(post_instance)
#     if request.method == "POST":
#         form = CommentForm(request.POST)

#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.comment_date = timezone.now()
#             comment.author = Author.objects.get(user=request.user)
#             comment.save()

#     else:
#         form = CommentForm()

#     return render(request, 'blog/comment_form.html', {'form': form})
