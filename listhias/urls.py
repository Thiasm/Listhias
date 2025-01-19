from django.contrib import admin
from django.urls import path, include

handler404 = 'app.views.custom_page_not_found_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
]
