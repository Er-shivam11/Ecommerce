from django.urls import path

from . import views
from luxmart import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("home/", views.home, name="home"),
    path("index/", views.index, name="index"),
    path("", views.sign_up, name="signup"),
    path("login/", views.sign_in, name="login"),
    path("detail/", views.det, name="det"),
    path("card/", views.car, name="car"),
    path("delete-car/<id>/", views.delete_car, name="delete"),
    path("update-car/<id>/", views.update_car, name="update"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
