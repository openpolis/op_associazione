from django.contrib import admin
from op_associazione.models import Membership, Associate, Citizen, Organization, Politician

class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    
class AssociateAdmin(admin.ModelAdmin):
    inlines = [MembershipInline,]
    
class MembershipAdmin(admin.ModelAdmin):
    fields = ['type_of_membership']

admin.site.register(Membership)
admin.site.register(Associate, AssociateAdmin)
admin.site.register(Citizen) 
admin.site.register(Organization) 
admin.site.register(Politician) 
