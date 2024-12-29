from django import forms
from .models import Fund, Deposit, Withdrawal, Person, Bazar

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['year', 'month', 'bazar', 'name', 'sellery_amount']
        widgets = {
            'year': forms.NumberInput(attrs={'placeholder': 'سال درج کریں'}),
            'month': forms.NumberInput(attrs={'placeholder': 'مہینہ درج کریں'}),
            'name': forms.TextInput(attrs={'placeholder': 'شخص کا نام درج کریں'}),
            'sellery_amount': forms.NumberInput(attrs={'placeholder': 'رقم درج کریں'}),
        }
class UploadExcelForm(forms.Form):
    file = forms.FileField(label='Upload Excel File')

class CreatePersonListForm(forms.Form):
    bazar = forms.ModelChoiceField(
        queryset=Bazar.objects.all(), 
        label="بازار", 
        initial=Bazar.objects.first()  # Set the default bazar (first item)
    )
    month = forms.IntegerField(min_value=1, max_value=12, label="مہینہ", initial=1)  # Set a default month
    year = forms.IntegerField(label="سال", initial=2025)  # Set a default year
    person_name = forms.CharField(max_length=255, label="شخص کا نام")


class FilterForm(forms.Form):
    bazar = forms.ModelChoiceField(queryset=Bazar.objects.all(), label="بازار")
    month = forms.IntegerField(min_value=1, max_value=12, label="مہینہ")
    year = forms.IntegerField(label="سال")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default values for fields if needed
        self.fields['bazar'].initial = Bazar.objects.first()  # Default first Bazar choice
        self.fields['month'].initial = 1  # Default month (January)
        self.fields['year'].initial = 2025  # Default year

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['category', 'expense_name', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default category
        self.fields['category'].initial = 'other_expense'
        self.fields['category'].empty_label = None

        # Customize labels
        self.fields['category'].label = 'اخراجات کی قسم'
        self.fields['expense_name'].label = 'اخراجات کا نام'
        self.fields['amount'].label = 'رقم'

        # Add placeholders
        self.fields['expense_name'].widget.attrs.update({'placeholder': 'اخراجات کا نام درج کریں'})
        self.fields['amount'].widget.attrs.update({'placeholder': 'رقم درج کریں'})

        # Style fields
        for field in self.fields.values():
            field.widget.attrs.update({'style': 'font-size: 24px; padding: 10px; font-family: "Jameel Noori Nastaleeq", sans-serif; text-align: right;'})

class DepositSelleryForm(forms.Form):
    sellery_amount = forms.DecimalField(max_digits=10, decimal_places=2, label="تنخواہ")


class DepositForm(forms.Form):
    FUND_CHOICES = [
        ('TH1', 'جمعرات پہلا وقت'),
        ('TH2', 'جمعرات دوسرا وقت'),
        ('FR', 'جمعہ کا فنڈ'),
        ('MS', 'ماہانہ مولوی کی تنخواہ'),
        ('OF', 'دیگر فنڈز'),
    ]
    fund = forms.ChoiceField(
        choices=FUND_CHOICES, 
        label="فنڈ کی قسم", 
        widget=forms.Select(attrs={
            'style': 'font-size: 18px; padding: 18px; font-weight: bold; font-family: "Jameel Noori Nastaleeq", sans-serif; direction: rtl;'
        })
    )
    fund_name = forms.CharField(
        max_length=255, 
        required=False, 
        label="فنڈ کا نام",
        widget=forms.TextInput(attrs={'placeholder': 'دیگر فنڈ کا نام', 'style': 'font-size: 18px; padding: 28px;  font-family: "Jameel Noori Nastaleeq", sans-serif; direction: rtl;'})
    )
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="رقم",
        widget=forms.NumberInput(attrs={'placeholder': 'رقم درج کریں', 'style': 'font-size: 18px; padding: 28px; font-family: "Jameel Noori Nastaleeq", sans-serif; direction: rtl;'})
    )

