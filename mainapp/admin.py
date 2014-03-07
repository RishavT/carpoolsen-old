from django.contrib import admin
from mainapp.models import Rider,Post


#class ChoiceInline(admin.StackedInline):
    #model = Choice
    #extra = 3

#class PollAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None,               {'fields': ['question']}),
        #('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    #]
    #inlines = [ChoiceInline]

admin.site.register(Rider)
admin.site.register(Post)
