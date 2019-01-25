from .models import Category

def list_categories(request):
    """
    List categories in menu
    """
    return {"menu_categories":Category.objects.all()}
