# -*- coding: utf-8 -*-
from os import sys
from django import forms
from op_associazione.models import Membership, Citizen, Politician, Organization, Associate


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ('fee', 'public_subscription', 'type_of_membership')
        widgets = {
                    'fee': forms.TextInput(attrs={'class': 'span1'}),
                }
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
    exp_address_provided = forms.BooleanField(required=False)
    exp_street = forms.CharField(label='Via, viale, ecc', required=False)
    exp_civic_nb = forms.CharField(label='Numero civico', required=False)
    exp_zip_code = forms.CharField(label='CAP', required=False)
    exp_location = forms.CharField(label='Città', required=False)
    exp_province = forms.CharField(label='Provincia', required=False)
    exp_country = forms.CharField(label='Nazione', required=False)
    
            
    def clean(self):
        """custom validation for expedition address, only if different from main address"""
        cleaned_data = super(AssociateForm, self).clean()
        exp_address_provided = cleaned_data.get('exp_address_provided')
        if exp_address_provided:
            for f in ['street', 'civic_nb', 'zip_code', 'location', 'province', 'country']:
                field = "exp_%s" % (f,)
                if cleaned_data.get(field) == '':
                    self._errors[field] = self.error_class(["Questo campo è obbligatorio."])
                    del cleaned_data[field]
        
        return cleaned_data
        
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
            'gender': forms.Select(attrs={'class': 'span1'}),
            'notes': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
            'charge': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
            'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'class':'datepicker span2'}),
            'civic_nb': forms.TextInput(attrs={'class': 'span1'}),
            'zip_code': forms.TextInput(attrs={'class': 'span1'}),
            'city': forms.TextInput(attrs={'class': 'span2'}),
            'province': forms.TextInput(attrs={'class': 'span2'}),
            'country': forms.TextInput(attrs={'class': 'span2'}),
            'exp_civic_nb': forms.TextInput(attrs={'class': 'span1'}),
            'exp_zip_code': forms.TextInput(attrs={'class': 'span1'}),
            'exp_city': forms.TextInput(attrs={'class': 'span2'}),
            'exp_province': forms.TextInput(attrs={'class': 'span2'}),
            'exp_country': forms.TextInput(attrs={'class': 'span2'}),
            'denomination': forms.TextInput(attrs={'class': 'span4'}),
        }
        exclude = ('hash_key',)

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
    email = forms.EmailField(help_text="Inserisci l'email con la quale ti sei registrato/a all'associazione")
    def clean_email(self):
        email = self.cleaned_data['email']
        try :
            self.associate = Associate.objects.get(email=email)
        except Associate.DoesNotExist:
            raise forms.ValidationError("Email non associata a nessun utente.")
        return email