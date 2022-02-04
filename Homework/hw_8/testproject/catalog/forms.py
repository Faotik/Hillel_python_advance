from django import forms


class AddAuthorForm(forms.Form):
    name = forms.Field()
    date_of_birth = forms.DateField()
    date_of_death = forms.DateField()

    def clean_data(self):
        name = self.cleaned_data["name"]
        date_of_birth = self.cleaned_data["date_of_birth"]
        date_of_death = self.cleaned_data["date_of_death"]

        if(name is None or date_of_birth is None or date_of_death is None):
            raise forms.ValidationError("Field is empty")

        return (name, date_of_birth, date_of_death)


class EditAuthorForm(forms.Form):
    name = forms.Field()
    date_of_birth = forms.DateField()
    date_of_death = forms.DateField()

    def clean_data(self):
        name = self.cleaned_data["name"]
        date_of_birth = self.cleaned_data["date_of_birth"]
        date_of_death = self.cleaned_data["date_of_death"]

        if(name is None or date_of_birth is None or date_of_death is None):
            raise forms.ValidationError("Field is empty")

        return (name, date_of_birth, date_of_death)

