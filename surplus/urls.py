from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views  # <-- MOVED TO THE TOP
from marketplace import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    path('signup/', views.signup, name='signup'),
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('profile/', views.profile, name='profile'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('claim/<int:item_id>/', views.mark_claimed, name='mark_claimed'),
    
    path('inbox/', views.inbox, name='inbox'),
    path('chat/start/<int:item_id>/', views.start_chat, name='start_chat'),
    path('chat/<int:convo_id>/', views.chat_room, name='chat_room'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)