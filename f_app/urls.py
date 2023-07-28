from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from django.contrib.auth import views
from .views import HomeView, get_response_not, login_view, edit_user_profile_view, log_out_view, change_password_view, UrlView, UpdateUrlView, delete_solo_url, home_search_view

urlpatterns = [

	path('', HomeView.as_view(), name='home-view'),
	path("notifications/", get_response_not, name="not-view"),

	path('search/', home_search_view, name='search-view'),
	path('login/', login_view, name='login-view'),
	path('url-fecth/', UrlView.as_view(), name='url-fecth'),
	path('delete/<id>/', delete_solo_url, name='delete-solo'),
	path('update/<id>/', UpdateUrlView.as_view() ,name='update-solo'),
	path('edit-my-data/', edit_user_profile_view,name='edit-my-data'),
	path('sign-out/', log_out_view, name='sign-out'),
	path('set-new-password/', change_password_view, name='set-new-password'),
	
	# password-reset
    path('reset_password/',
     views.PasswordResetView.as_view(template_name='user_temp/password/password_reset_form.html'),
      name='reset_password'),

    path('reset_password_sent/',
     views.PasswordResetDoneView.as_view(template_name='user_temp/password/password_reset_done.html'),
      name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
     views.PasswordResetConfirmView.as_view(template_name='user_temp/password/password_reset_confirm.html'),
      name='password_reset_confirm'),

    path('reset_password_complete/',
     views.PasswordResetCompleteView.as_view(template_name='user_temp/password/password_reset_complete.html'),
      name='password_reset_complete'),
	  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)