from threading import Thread
from time import sleep
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup
import re

from django.contrib import messages
from django.contrib.auth import authenticate, get_user, login, logout, update_session_auth_hash
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import EditUserForm, ChangePasswordForm, UrlForm
from .models import UrlModel, ChangesInLines




def update_links():
	while True:
		listScrap = []
		for name in UrlModel.objects.all():
			soup = BeautifulSoup(requests.get(name.url).text, 'html.parser')
			for scraping in soup.prettify().split('\n'):
				listScrap.append(scraping.strip())
			sleep(name.updating_time*60)
			UrlModel.objects.filter(url=name.url).update(
					source_code='\n'.join(listScrap)
			)
			listScrap.clear()
def update_thread():
	t = Thread(target=update_links)
	t.start()
# update_thread()

def check_diffrence():
	while True:
		for scraper in UrlModel.objects.all():
			source_code 	  = scraper.source_code
			source_code_split = scraper.source_code.split('\n')
			check_code_split  = scraper.check_code.split('\n')
			
			for source, check in zip(source_code_split, check_code_split):
				if check not in source_code_split:
					if len(check) < scraper.checking_length or len(check) > scraper.checking_length:

						update = UrlModel.objects.filter(name=scraper)
						update.update(
								old_line=check,
								new_line=source,
								check_code=source_code
							)

						create = ChangesInLines.objects
						create.create(
							user=scraper.user,
							url_model=scraper,
							name=scraper,
							url=scraper.url,
							old_line=check,
							new_line=source
						)
						send_mail(
							'Diffrence in your link. '+'('+scraper.url+')',
							'THE OLD: '+check + '\nTHE NEW: '+source,
							settings.EMAIL_HOST_USER,
							[scraper.user.email],
						)
def check_thread():
	t = Thread(target=check_diffrence)
	t.start()
# check_thread()










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
				url = UrlModel.objects.get(id=id)
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

def url_view(request):
	context = {}
	list_unique_name = []
	list_unique_url  = []
	for uniqe in UrlModel.objects.filter(user=request.user):
		list_unique_name.append(uniqe.name)
		list_unique_url.append(uniqe.url)
	listScrap = []
	if request.method == 'POST':
		name 	= request.POST.get('name')
		url 	= request.POST.get('url')
		length 	= request.POST.get('length')
		time 	= request.POST.get('time')
		soup 	= BeautifulSoup(requests.get(url).text, 'html.parser')
		nameLower = name.lower()
		if nameLower in list_unique_name:
			context['errorName'] = 'You assign this name for link before.'
		elif url in list_unique_url:
			context['errorUrl'] = 'You assign this link before.'
		else:
			for scraping in soup.prettify().split('\n'):
				listScrap.append(scraping.strip())
			UrlModel.objects.create(
					user=request.user,
					name=nameLower,
					url=url,
					checking_length=length,
					updating_time=time,
					source_code='\n'.join(listScrap),
					check_code='\n'.join(listScrap),
					old_line='',
					new_line=''
			)
	return render(request, 'user_temp/url_model.html', context=context)
	

def delete_solo_url(request, id):
	url = UrlModel.objects.get(id=id)
	url.delete()
	return redirect('home-view')

def update_solo_url(request, id):
	context = {}
	list_unique_name = []
	list_unique_url  = []
	for uniqe in UrlModel.objects.filter(user=request.user):
		list_unique_name.append(uniqe.name)
		list_unique_url.append(uniqe.url)
		
	url  = UrlModel.objects.get(id=id)
	form = UrlForm(instance=url)
	context['form'] = form
	if form.instance.name in list_unique_name:
		list_unique_name.remove(form.instance.name)
	if form.instance.url in list_unique_url:
		list_unique_url.remove(form.instance.url)

	if request.method == 'POST':
		name 	  = request.POST.get('name')
		url_name  = request.POST.get('url')
		nameLower = name.lower()

		if nameLower in list_unique_name:
			context['errorName'] = 'You assign this name for link before.'
		elif url_name in list_unique_url:
			context['errorUrl'] = 'You assign this link before.'
		else:
			form = UrlForm(request.POST, instance=url)
			if form.is_valid():
				form.save()
				return redirect('home-view')
		
	return render(request, 'user_temp/edit_url.html', context=context)

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


'''def notifications(request):
	listContext = []
	url = ChangesInLines.objects.filter(user=request.user).order_by('-created_on')

	for line in url:
		oldLineRe = re.sub('[\"-<->]', "", line.old_line)
		newLineRe = re.sub('[\"-<->]', "", line.new_line)
		listContext.append(line.created_on)
		listContext.append(line.name)
		listContext.append(line.url)
		listContext.append(oldLineRe)
		listContext.append(newLineRe)
	return JsonResponse({'lines': listContext})'''


def get_response_not(request):
	if not request.user.is_authenticated:
			return redirect('login-view')
	
	url = ChangesInLines.objects.filter(user=request.user).order_by('-created_on')

	return render(request, 'user_temp/notifications.html', context={'urls': url})


'''def get_notice_changes(request):
	context   = {}
	lines 	  = ChangesInLines.objects.filter(user=request.user)
	listLines = []

	for line in lines:
		listLines.append(line.name)
	context['length'] = len(listLines)

	return JsonResponse(context)'''



def log_out_view(request):
	logout(request)
	return redirect('login-view')


