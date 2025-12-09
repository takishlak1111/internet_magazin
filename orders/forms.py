from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'payment']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' not in kwargs and 'instance' not in kwargs:
            user = self.user if hasattr(self, 'user') else None
            if user and user.is_authenticated:
                self.fields['email'].initial = user.email