from .models import  Category

def category_renderer(request):
   category=Category.objects.all()
   return {
       'category':category
    }