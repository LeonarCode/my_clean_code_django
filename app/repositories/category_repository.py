from app.models import Category

class CategoryRepository():
    @staticmethod
    def get_all():
        return Category.objects.all().order_by("name")