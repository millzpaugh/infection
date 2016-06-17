from django import forms


class FullInfectionForm(forms.Form):
    pool_size = forms.IntegerField(required=True, label="User Pool Size (50 max)", widget=forms.TextInput(attrs={'placeholder': 'Enter Pool Size'})
    )

    def clean(self):
        cleaned_data = super(FullInfectionForm, self).clean()
        pool_size = cleaned_data.get("pool_size")

        if pool_size > 50:
            msg = "You cannot have more than 50 users."
            self.add_error("pool_size", msg)

class LimitedInfectionForm(forms.Form):
    pool_size = forms.IntegerField(required=True, label="User Pool Size (50 max)", widget=forms.TextInput(attrs={'placeholder': 'Enter Pool Size'})
    )
    infection_size = forms.IntegerField(required=True, label="Number of Users to Infect (Must be less than Pool Size)", widget=forms.TextInput(attrs={'placeholder': 'Enter Pool Size'})
    )

    def clean(self):
        cleaned_data = super(LimitedInfectionForm, self).clean()
        pool_size = cleaned_data.get("pool_size")
        infection_size = cleaned_data.get("infection_size")

        if pool_size > 50:
            msg = "You cannot have more than 50 users."
            self.add_error("pool_size", msg)
        elif infection_size >= pool_size:
            msg = "Your infection size must be smaller than your pool size."
            self.add_error("infection_size", msg)


