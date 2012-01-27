from django.contrib import admin
from op_associazione.models import Membership, Address, Associate, Citizen, Organization, Politician

class ExpAddressInline(admin.TabularInline):
	model = Address
#	fk_name = 'expedition_address'
	
class LegalAddressInline(admin.TabularInline):
	model = Address
#	fk_name = 'legal_address'
	
class MembershipInline(admin.TabularInline):
	model = Membership
	extra = 1 
	
class AssociateAdmin(admin.ModelAdmin):
	inlines = [MembershipInline,LegalAddressInline,]
	
class MembershipAdmin(admin.ModelAdmin):
	fields = ['type_of_membership']

admin.site.register(Address) 
admin.site.register(Membership)
admin.site.register(Associate, AssociateAdmin)
admin.site.register(Citizen) 
admin.site.register(Organization) 
admin.site.register(Politician) 
