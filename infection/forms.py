from django import forms


class FullInfectionForm(forms.Form):
    pool_size = forms.IntegerField(required=True, label="User Pool Size (50 max)", widget=forms.TextInput(attrs={'placeholder': 'Enter Pool Size'})
    )

