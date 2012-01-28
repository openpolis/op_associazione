# -*- coding: utf-8 -*-
from django import forms
from op_associazione.models import Address, Membership, Citizen, Politician, Organization, Associate

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        widgets = {
            'civic_nb': forms.TextInput(attrs={'size': 10}),
            'zip_code': forms.TextInput(attrs={'size': 10})
        }

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('fee', 'public_subscription', 'type_of_membership')
        
    def clean(self):
        cleaned_data = self.cleaned_data
        fee = cleaned_data.get("fee")
        member_type = cleaned_data.get("type_of_membership")
        minimum_fee = Membership.get_minimum_fee(member_type)
        
        if fee and member_type :
            if fee < minimum_fee:
                msg = u"L'importo minimo come %s è di %d euro" % (Membership.get_typename(member_type), minimum_fee)
                self._errors["fee"] = self.error_class([msg])
                del cleaned_data["fee"]
        return cleaned_data  

# generic Associates form
class AssociateForm(forms.ModelForm):
    accept_policy = forms.BooleanField(help_text='Approvazione statuto')
    accept_privacy_policy = forms.BooleanField(help_text='Approvazione trattamento dati personali')
    
    def clean_fiscal_code(self):
        import re
        cc = self.cleaned_data.get('fiscal_code').upper().replace(' ', '')
        pattern = r'^[A-Z]{6}[\d]{2}[A-Z][\d]{2}[A-Z][\d]{3}[A-Z]$'
        
        if not re.match(pattern, cc):
            raise forms.ValidationError("Il codice fiscale inserito non è valido")
        self.cleaned_data['fiscal_code'] = cc
        return cc
    
    
    class Meta():
        widgets = {
            'gender': forms.RadioSelect(),
            'notes': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
            'charge': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
            'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'class':'datepicker', 'readonly':'true'}),
        }
        exclude = ('legal_address', 'expedition_address', 'hash_key')

class CitizenForm(AssociateForm):
    class Meta(AssociateForm.Meta):
        model = Citizen

class PoliticianForm(AssociateForm):
    class Meta(AssociateForm.Meta):
        model = Politician

class OrganizationForm(AssociateForm):
    class Meta(AssociateForm.Meta):
        model = Organization

# Form per la richiesta di rinnovo
class RenewalRequestForm(forms.Form):
    email = forms.EmailField()
    def clean_email(self):
        email = self.cleaned_data['email']
        try :
            self.associate = Associate.objects.get(email=email)
        except Associate.DoesNotExist:
            raise forms.ValidationError("Email non associata a nessun utente.")
        return email