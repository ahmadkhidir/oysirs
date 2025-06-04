from django.contrib import admin
from django.urls import path, include, reverse, reverse_lazy
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="OYSIRS API",
        default_version='v1',
        description="""""",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="khidirahmad05@gmail.com",
                                name="Ahmad Khidir",
                                url="https://linkedin.com/in/ahmadkhidir/"),
        license=openapi.License(name="OYSIRS License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("admin:index"))),
    # path("accounts/", include('accounts.urls'), name="accounts"),
    # path("api-auth/", include('api_auth.urls'), name="api-auth"),
    # path("auth/", include('rest_framework.urls'), name="auth"),
    # path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
