from django.contrib import admin
from .models import Category, Page
# Register your models here.

#To customize the Category model on the /admin site
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "views", "likes", "slug"]
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Category, CategoryAdmin) #Important to register both the model and adminmodel class


#To customize the Page model on the /admin site
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "url", "views"]

admin.site.register(Page, PageAdmin)
