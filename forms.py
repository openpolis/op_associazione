from django import forms
from op_associazione.models import Address, Membership, Citizen, Politician, Organization, Associate

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address

class MembershipForm(forms.ModelForm):
	class Meta:
		model = Membership
		fields = ('fee', 'public_subscription', 'type_of_membership')	

# generic META for Associates form
class AssociateForm(forms.ModelForm):
#	formfield_callback = make_custom_datefield
	accept_policy = forms.BooleanField(help_text='Approvazione statuto')
	accept_privacy_policy = forms.BooleanField(help_text='Approvazione trattamento dati personali')
#	membership_type = forms.IntegerField(widget=forms.Select(choices=Membership.MEMBER_TYPE[1:3]))
	class Meta():
		widgets = {
				'gender': forms.RadioSelect(),
				'notes': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
				'charge': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
				'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'class':'datepicker', 'readonly':'true'}),
			}
		exclude = ('legal_address', 'expedition_address')
	
class CitizenForm(AssociateForm):
	class Meta(AssociateForm.Meta):
		model = Citizen
#		exclude = ('phone_number', 'email', 'wants_newsletter', 'legal_address', 'expedition_address')
		
class PoliticianForm(AssociateForm):
	class Meta(AssociateForm.Meta):
		model = Politician
	
class OrganizationForm(AssociateForm):
	class Meta(AssociateForm.Meta):
		model = Organization

class RenewalForm(forms.Form):
	email = forms.EmailField()
	def clean_email(self):
		email = self.cleaned_data['email']
		try :
			self.associate = Associate.objects.get(email=email)
		except Associate.DoesNotExist:
			raise forms.ValidationError("Email non associata a nessun utente.")
		return email

class ContactForm(forms.Form):
	email = forms.EmailField()
	email_login = forms.BooleanField(help_text='Uso questo indirizzo per effettuare il login nei siti openpolis.it e openparlamento.it', required=False)
	phone_number = forms.CharField(max_length=100,min_length=3)
	wants_newsletter = forms.BooleanField(required=False, help_text='Voglio ricevere la newsletter via email')
	policy_accept = forms.BooleanField(help_text='Approvo i principi e le regole dello statuto dell\'Associazione Openpolis')
	privacy_accept = forms.BooleanField(help_text='Autorizzo l\'Associazione Openpolis al trattamento dei miei dati personali per gli scopi indicati nell\'apposita informativa')
