from django import forms


class BasketAddProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(min_value=1, max_value=20, initial=1,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
