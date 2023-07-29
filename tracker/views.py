from django.contrib.auth.models import User
import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import EditUserForm, ChangePasswordForm, UrlForm
from .models import UrlModel, ChangesStore
from django.views.generic.edit import FormView
from .utils import new_periodic_task, get_url_source_code
from tasks.utils import delete_periodic_task


class HomeView(View):
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('login-view')

		url_result = UrlModel.objects.filter(user=request.user)
		context = {
			'scraper': url_result,
		}
		return render(request, 'user_temp/home.html', context=context)

	def post(self, request):
		if request.method == 'POST':
			urls_id = request.POST.getlist('id[]')
			for id in urls_id:
				url = UrlModel.objects.select_related('user').get(id=id)
				delete_periodic_task(name=f'user_{url.user.id}_url_{url.id}')
				for task in url.url_model_task_control.all():
					task.revoke_celery_task()
				url.delete()
			return redirect('home-view')

def home_search_view(request):
	context = {}
	if request.method == 'GET':
		search = request.GET.get('search')
		
		url_search_by_name = UrlModel.objects.filter(name__contains=search, user=request.user)
		context['url_search_by_name'] = url_search_by_name

		url_search_by_url = UrlModel.objects.filter(url__contains=search, user=request.user)
		context['url_search_by_url'] = url_search_by_url

		url_search_by_source_code = UrlModel.objects.filter(source_code__contains=search, user=request.user)
		context['url_search_by_source_code'] = url_search_by_source_code

	
	return render(request, 'user_temp/search.html', context=context)


def login_view(request):
	if request.user.is_authenticated:
		return redirect('home-view')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home-view')
		else:
			messages.error(request, 'Username or Password is incorrect')

	return render(request, 'user_temp/login.html', context={})


class UrlView(FormView):
	form_class = UrlForm
	template_name = 'user_temp/url_model.html'
	success_url   ='/'

	def get_initial(self):
		initial = super().get_initial()
		initial['user'] = self.request.user
		return initial

	def form_valid(self, form):
		url = form.cleaned_data.get('url')
		every = form.cleaned_data.get('updating_time')
		form.instance.source_code = get_url_source_code(url=url)

		form.save()
		new_periodic_task(user_id=self.request.user.id, url_model_id=form.instance.id, every=every)

		return super().form_valid(form)
	

def delete_solo_url(request, id):
	url = UrlModel.objects.select_related('user').get(id=id)
	delete_periodic_task(name=f'user_{url.user.id}_url_{url.id}')
	for task in url.url_model_task_control.all():
		del_task = task.revoke_celery_task
	url.delete()
	return redirect('home-view')

class UpdateUrlView(FormView):
	form_class = UrlForm
	template_name = 'user_temp/edit_url.html'
	success_url = '/'

	def get_form(self, form_class=form_class):
		url_model = UrlModel.objects.get(id=self.kwargs.get('id'))
		return form_class(instance=url_model, **self.get_form_kwargs())

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return super().form_valid(form=form)


def edit_user_profile_view(request):
	form = EditUserForm(instance=request.user)
	if request.method == 'POST':
		form = EditUserForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('edit-my-data')
	return render(request, 'user_temp/edit_profile.html', context={'edit_user_form': form})

def change_password_view(request):
	context = {}
	form = ChangePasswordForm(request.POST or None)
	if request.method == 'POST':
		old_password  = request.POST.get('old_password')
		new_password1 = request.POST.get('new_password1')
		new_password2 = request.POST.get('new_password2')

		complexPassword = re.findall('[a-zA-Z]', new_password1)

		user = User.objects.get(id=request.user.id)

		if not user.check_password(old_password):
			context['errorOldPass'] = 'Your old password was entered incorrectly. Please enter it again.'
		elif new_password2 != new_password1:
			context['didntMatch'] 	= 'The two password fields didn\'t match'
		elif len(new_password1) < 8:
			context['lenPass']	 	= 'This password is too short. It must contain at least 8 characters.'
		elif not complexPassword:
			context['complexPass'] 	=  'Your password can\'t be entirely numeric.'
		else:
			form = ChangePasswordForm(data=request.POST, user=request.user)
			if form.is_valid():
				form.save()
				# update_session_auth_hash(request, form.user)
				return redirect('sign-out')

	context['change_password_form'] = form
	return render(request, 'user_temp/change_password.html', context=context)



def get_response_not(request):
	if not request.user.is_authenticated:
		return redirect('login-view')
	
	url = ChangesStore.objects.select_related('url_model').filter(user=request.user).order_by('-created_on')

	return render(request, 'user_temp/notifications.html', context={'urls': url})


def log_out_view(request):
	logout(request)
	return redirect('login-view')


