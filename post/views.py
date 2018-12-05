from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.views.generic.edit import ModelFormMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from django.http import JsonResponse
from .models import Post

"""class AjaxableResponseMixin:
    
    #Mixin to add AJAX support to a form.
    #Must be used with an object-based FormView (e.g. CreateView)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
        	tag_list = form[tags]
        	data = {'posts': tag_list}
        	return JsonResponse(data)
        else:
            return response"""

class FilteredPostListView(ListView):
	model = Post #.objects.filter(tags__name__in=["black&white", "red"]).distinct()
	template_name = 'post/search.html'	# <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 20

	def get_queryset(self):
		tag_list = list()
		web_input = self.request.GET.get('tags')
		if ',' not in web_input:
			tag_list.append(web_input)
		else:
			tag_list = self.request.GET.get('tags').split(', ')
		print(tag_list)
		return Post.objects.filter(tags__name__in=tag_list).annotate(num_tags=Count('tags')).filter(num_tags__gte=len(tag_list)).order_by('-date_posted').distinct()

class PostListView(ListView):
	model = Post #.objects.filter(tags__name__in=["black&white", "red"]).distinct()
	template_name = 'post/home.html'	# <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 10

	#def get_queryset(self):
		#tag_list = ['japanese', 'back']
		#return Post.objects.filter(tags__name__in=tag_list).annotate(num_tags=Count('tags')).filter(num_tags__gte=len(tag_list)).order_by('-date_posted').distinct()


class TattooerPostListView(ListView):
	model = Post #.objects.filter(tags__name__in=["black&white", "red"]).distinct()
	template_name = 'post/tattooers_tattoos.html'	# <app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	paginate_by = 10

	def get_queryset(self):
		user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Post
	fields = ['title', 'content', 'image', 'tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		if self.request.user.tattooer:
			return True
		return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content', 'image', 'tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/ '

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def about(request):
    return render(request, 'post/about.html', {'title': 'About'})