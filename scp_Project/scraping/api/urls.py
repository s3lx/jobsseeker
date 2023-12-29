from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('languages', LanguageViewSet)
router.register('vacancy', VacancyViewSet)
urlpatterns = router.urls
