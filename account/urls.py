from django.urls import path
from . import views
urlpatterns=[
    path('',views.register,name='reg'),
    path('login/',views.login,name='lgt'),
    path('logout/',views.logout,name='lgn'),
    path('profile/',views.Prof,name='pro'),
    path('uppro/',views.uppro,name='uppro'),
    path('RRegister/',views.RRegister,name="rreg")
]
