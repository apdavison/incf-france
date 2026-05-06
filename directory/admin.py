from django.contrib import admin


from .models import Text, Researcher, Team, Laboratory, Project, \
                               PositionType, ResourceType

admin.site.register(PositionType)
admin.site.register(ResourceType)
admin.site.register(Text)
admin.site.register(Researcher)
admin.site.register(Team)
admin.site.register(Laboratory)
admin.site.register(Project)