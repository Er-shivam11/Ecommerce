from django.urls import path

from . import views
from luxmart import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("home/", views.home, name="home"),
    path("index/", views.index, name="index"),
    path("", views.sign_up, name="signup"),
    path("login/", views.sign_in, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("profile_view_upd/", views.profile_view_update, name="profile_view_upd"),
    path("view_profile/", views.view_profile, name="view_profile"),
    path("userlist/", views.userlist, name="userlist"),


    path("detail/", views.det, name="det"),
    path("add-product/", views.addproduct, name="addproduct"),
    path("menproductlist/", views.men_pro_list, name="menproductlist"),
    path("womenproductlist/", views.women_pro_list, name="womenproductlist"),
    path("cosandaccess/", views.cos_and_access, name="cosaccess"),
    path("delete-car/<id>/", views.delete_product, name="delete"),
    path("update-car/<id>/", views.update_product, name="update"),
    path("view_cart/", views.view_cart, name="view_cart"),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("orderform/", views.order, name="order"),
    path("decrease_quantity/<int:cart_item_id>", views.decrease_quantity, name="decrease_quantity"),
    path("increase_quantity/<int:cart_item_id>", views.increase_quantity, name="increase_quantity"),

    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
