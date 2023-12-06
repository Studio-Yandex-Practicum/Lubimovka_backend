from django.contrib import admin
from django.contrib.sites.models import Site

from apps.afisha.admin.events import EventAdmin
from apps.afisha.admin.performance import PerformanceAdmin
from apps.afisha.admin.performance_media_review import PerformanceMediaReviewAdmin
from apps.afisha.admin.performance_review import PerformanceReviewAdmin
from apps.afisha.admin.reading import Reading

admin.site.unregister(Site)
