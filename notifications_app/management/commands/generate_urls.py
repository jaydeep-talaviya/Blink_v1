from django.conf import settings
from django.urls import URLPattern, URLResolver
from django.core.management.base import BaseCommand

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

class Command(BaseCommand):
    help = 'Genarate total list of urls'


    def list_urls(self, patterns, path=None):
        """ recursive """
        if not path:
            path = []
        result = []
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                result.append(''.join(path) + str(pattern.pattern))
            elif isinstance(pattern, URLResolver):
                result += self.list_urls(pattern.url_patterns, path + [str(pattern.pattern)])
        return result

    def handle(self, *args, **options):
        print("total urls:",self.list_urls(urlconf.urlpatterns))