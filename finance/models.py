from django.db import models

class Fund(models.Model):
    FUND_TYPES = [
        ('TH1', 'جمعرات پہلا وقت'),
        ('TH2', 'جمعرات دوسرا وقت'),
        ('FR', 'جمعہ فنڈ'),
        ('MS', 'مولوی کی ماہانہ تنخواہ'),
        ('OF', 'دیگر فنڈز'),
    ]
    name = models.CharField(max_length=500, verbose_name='فنڈ کا نام')
    fund_type = models.CharField(max_length=10, choices=FUND_TYPES, verbose_name='فنڈ کی قسم')
    def get_fund_type_display_urdu(self):
        return dict(self.FUND_TYPES).get(self.fund_type, self.fund_type)

class Bazar(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    bazar = models.ForeignKey(Bazar, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    sellery_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Changed field name
    sellery_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Deposit(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, verbose_name='فنڈ')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='رقم')
    date = models.DateField(verbose_name='تاریخ')

    def __str__(self):
        return f"{self.fund.name} - {self.amount}"

class Withdrawal(models.Model):
    EXPENSE_CATEGORIES = [
        ('salary', 'مولوی کی تنخواہ'),
        ('electricity_bill', 'بجلی کا بل'),
        ('other_expense', 'دیگر اخراجات'),
    ]

    category = models.CharField(max_length=20, choices=EXPENSE_CATEGORIES, verbose_name='اخراجات کی قسم')
    expense_name = models.CharField(max_length=500, blank=True, null=True, verbose_name='اخراجات کا نام')  # Optional for other expenses
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='رقم')
    date = models.DateField(verbose_name='تاریخ')

    def __str__(self):
        return f"{self.expense_name} - {self.amount}"