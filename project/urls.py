from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
                  path(settings.ADMIN_URL, admin.site.urls),
                  path('', RedirectView.as_view(pattern_name='blog:list', permanent=True)),
                  path('blog/', include('blog.urls', namespace='blog')),
                  path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/', include('rest_api.urls')),
                  path('accounts/', include('accounts.urls', namespace='accounts')),
                  path('tools/', include('tools.urls', namespace='tools')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Third party URLs -----------------------------------------------------------------------------------------------------
urlpatterns += [
    path(r'markdownx/', include('markdownx.urls')),
]

# Add django debug-toolbar to the URLs
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
