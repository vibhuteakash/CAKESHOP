from  . import views
from django.urls import path

urlpatterns = [
     path('',views.Homepage),  #here we left the quotes blank so when server runs it directly open the Homepage without typing in url.
     path('Showcake/<cid>',views.Showcake),
     path('Viewdetails/<id>',views.Viewdetails),
     path('Login',views.Login),
     path('Signup',views.Signup),
     path('Logout',views.Logout),
     path('addTocart',views.addTocart),
     path('ShowAllCartItems',views.ShowAllCartItems),
     path('Makepayment',views.Makepayment),
]
