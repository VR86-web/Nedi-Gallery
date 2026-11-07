from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Your Name"}),
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"placeholder": "Your Mail"}),
    )
    message = forms.CharField(
        max_length=5000,
        widget=forms.Textarea(attrs={"placeholder": "Message"}),
    )
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "tabindex": "-1",
                "aria-hidden": "true",
                "style": "position:absolute;left:-10000px;",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError(
                "Unable to submit your message. Please try again."
            )
        return cleaned_data
