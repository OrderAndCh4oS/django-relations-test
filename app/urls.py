from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from app.views import PersonViewSet, RecipientViewSet, ScheduledMailViewSet, EmailViewSet

router = routers.DefaultRouter()
router.register(r'person', PersonViewSet)
router.register(r'email', EmailViewSet)
router.register(r'recipient', RecipientViewSet)
router.register(r'scheduled-mail', ScheduledMailViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
