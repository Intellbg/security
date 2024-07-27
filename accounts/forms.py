from django import forms
from api.models import (
    Person,
)


class ResetPasswordPersonForm(forms.Form):
    new_password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput,
        error_messages={"required": "Este campo es requerido"},
    )
    new_password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput,
        error_messages={"required": "Este campo es requerido"},
    )

    def __init__(self, *args, **kwargs):
        super(ResetPasswordPersonForm, self).__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ingrese nueva contraseña"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirme nueva contraseña"}
        )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1")
        if len(password1) < 6:
            raise forms.ValidationError(
                "La contraseña debe tener al menos 6 caracteres y tiene %i"
                % len(password1)
            )
        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas deben ser iguales")
        return password2
