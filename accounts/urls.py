from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('terms/',views.terms,name='terms'),
    path('bienvenido-usuario/<slug:slug_new>', views.register_success, name='register_success'),
    path('validate-email/<slug:hash_validation>/passe-app/<slug:slug>',views.verificar_email,name='verificar_email'),
    path('validate-email/success',views.verification_success,name='verification_success'),
    path('validate-email/used',views.used_verification,name='used_verification'),
    path('restore-password/<slug:slug_customer>',views.restore_password,name='restore_password'),
    path('success-restore-password/',views.success_reset_password,name='success_reset_password'),
    path('auth_pusher',views.auth_pusher, name='auth_pusher'),    
    path('not-found', views.custom_404, name='not_found'),
]
handler404 = views.handlerError404
handler500 = views.handlerError500
