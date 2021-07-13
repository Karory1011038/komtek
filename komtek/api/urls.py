from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views
from api.views import HandbookViewSet, ItemViewSet

router = routers.DefaultRouter()
router.register('handbooks', HandbookViewSet)
router.register('items', ItemViewSet)

urlpatterns = [
    # http://localhost:8000/api/admin/
    path('admin/', admin.site.urls),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),
    url(r'^.*$', views.gui, name='gui'),

]
