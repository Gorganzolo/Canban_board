from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Category, Reply
from .forms import PostForm
from .utils import send_new_reply_email, send_reply_accepted_email

class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author', 'category')
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_has_replied'] = Reply.objects.filter(post=self.object, author=self.request.user).exists()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'
    success_url = reverse_lazy('board:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'board/post_form.html'

    def get_success_url(self):
        return reverse_lazy('board:post_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("Вы можете редактировать только свои объявления.")
        return super().dispatch(request, *args, **kwargs)

class ReplyCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        text = request.POST.get('text')

        if post.author == request.user:
            messages.error(request, "Вы не можете оставлять отклик на свое собственное объявление.")
            return redirect('board:post_detail', pk=post.pk)

        if Reply.objects.filter(post=post, author=request.user).exists():
            messages.error(request, "Вы уже оставили отклик на это объявление.")
            return redirect('board:post_detail', pk=post.pk)

        if text:
            reply = Reply.objects.create(
                post=post,
                author=request.user,
                text=text
            )
            send_new_reply_email(reply)
            messages.success(request, "Ваш отклик успешно отправлен!")
        else:
            messages.error(request, "Текст отклика не может быть пустым.")

        return redirect('board:post_detail', pk=post.pk)

class UserRepliesListView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'board/user_replies.html'
    context_object_name = 'replies'

    def get_queryset(self):
        queryset = Reply.objects.filter(post__author=self.request.user).select_related('author', 'post').order_by('-created_at')
        post_id = self.request.GET.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_posts'] = Post.objects.filter(author=self.request.user).order_by('-created_at')
        return context

class ReplyAcceptView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk, post__author=request.user)
        if not reply.is_accepted:
            reply.is_accepted = True
            reply.save()
            send_reply_accepted_email(reply)
            messages.success(request, f"Отклик от {reply.author.email} принят.")
        return redirect('board:user_replies')

class ReplyDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reply = get_object_or_404(Reply, pk=pk, post__author=request.user)
        reply.delete()
        messages.success(request, "Отклик удален.")
        return redirect('board:user_replies')

class MySentRepliesListView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'board/my_sent_replies.html'
    context_object_name = 'replies'

    def get_queryset(self):
        return Reply.objects.filter(author=self.request.user).select_related('post').order_by('-created_at')
