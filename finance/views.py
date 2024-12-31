from django.shortcuts import render
from django.db.models import Sum, F
from .forms import WithdrawalForm 
from .models import Fund, Deposit, Withdrawal, Salary, Person
from django.shortcuts import render, redirect
from .forms import PersonForm, FilterForm
from .models import Person, Bazar
import pandas as pd
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Person, Bazar
from .forms import CreatePersonListForm, UploadExcelForm, DepositForm

def upload_person_list(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']  # Get the uploaded file

            try:
                # Read the Excel file directly from the uploaded file
                data = pd.read_excel(excel_file, engine='openpyxl')

                # Validate column names
                required_columns = ['Person Name', 'Bazar Name', 'month', 'year']
                if not all(col in data.columns for col in required_columns):
                    return render(request, 'finance/upload_person_list.html', {
                        'form': form,
                        'error': 'Invalid Excel format. Ensure columns: Person Name, Bazar Name, month, year.'
                    })

                # Process each row and save to the database
                for _, row in data.iterrows():
                    bazar_name = row['Bazar Name']
                    person_name = row['Person Name']
                    month = row['month']
                    year = row['year']

                    # Fetch Bazar object
                    try:
                        bazar = Bazar.objects.get(name=bazar_name)
                    except Bazar.DoesNotExist:
                        return render(request, 'finance/upload_person_list.html', {
                            'form': form,
                            'error': f"Bazar '{bazar_name}' does not exist."
                        })

                    # Save Person object
                    Person.objects.create(
                        name=person_name,
                        bazar=bazar,
                        month=month,
                        year=year
                    )

                # Redirect or show success message
                return redirect('upload_person_list')
            except Exception as e:
                return render(request, 'finance/upload_person_list.html', {
                    'form': form,
                    'error': f'Error processing file: {e}'
                })
    else:
        form = UploadExcelForm()

    return render(request, 'finance/upload_person_list.html', {'form': form})

def create_person_list(request):
    if request.method == 'POST':
        form = CreatePersonListForm(request.POST)
        if form.is_valid():
            bazar = form.cleaned_data['bazar']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            person_name = form.cleaned_data['person_name']

            Person.objects.create(
                bazar=bazar,
                month=month,
                year=year,
                name=person_name
            )
            return redirect('create_person_list')  # Stay on the same page
    else:
        form = CreatePersonListForm()

    return render(request, 'finance/create_person_list.html', {'form': form})

def deposit_sellery(request):
    filter_form = FilterForm(request.GET or None)
    persons = []  # Initialize as an empty list to avoid 'NoneType' error

    if request.method == 'GET' and filter_form.is_valid():
        bazar = filter_form.cleaned_data['bazar']
        month = filter_form.cleaned_data['month']
        year = filter_form.cleaned_data['year']

        # Get all persons matching the filter
        persons = Person.objects.filter(
            bazar=bazar, month=month, year=year, sellery_amount__isnull=True
        )

    if request.method == 'POST':
        person_id = request.POST.get('person_id')  # Get the person ID from the button clicked
        
        if person_id:
            try:
                person = Person.objects.get(id=person_id)  # Get the selected person
                amount_field = f"sellery_amount_{person.id}"  # Dynamically build the field name for amount
                amount = request.POST.get(amount_field)  # Get the entered amount for that person
                
                if amount:
                    # Update the person's sellery amount
                    person.sellery_amount = amount
                    person.sellery_date = timezone.now()  # You can set the date here as well
                    person.save()  # Save the updated amount
                    return redirect('deposit_sellery')  # Adjust URL name as needed

            except Person.DoesNotExist:
                pass  # Handle the case if the person does not exist (though it shouldn't happen)
        
    context = {
        'filter_form': filter_form,
        'persons': persons,
    }
    return render(request, 'finance/deposit_sellery.html', context)

def view_person_list(request):
    filter_form = FilterForm(request.GET or None)
    persons = None  # Default to None to prevent showing all records initially

    if request.method == 'GET' and filter_form.is_valid():
        bazar = filter_form.cleaned_data['bazar']
        month = filter_form.cleaned_data['month']
        year = filter_form.cleaned_data['year']

        persons = Person.objects.filter(bazar=bazar, month=month, year=year)

    context = {
        'filter_form': filter_form,
        'persons': persons,
    }
    return render(request, 'finance/view_person_list.html', context)


def dashboard(request):
    return render(request, 'finance/dashboard.html')


def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            fund_type = form.cleaned_data['fund']
            amount = form.cleaned_data['amount']
            fund_name = form.cleaned_data.get('fund_name') if fund_type == 'OF' else None
            date = form.cleaned_data.get('date')
            # Handle deposit logic
            Deposit.objects.create(
                fund=Fund.objects.get_or_create(name=fund_name if fund_name else fund_type)[0],
                amount=amount,
                date= date
            )
            return render(request, 'finance/dashboard.html')  # Success page
    else:
        form = DepositForm()

    return render(request, 'finance/deposit.html', {'form': form})

def withdraw(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        
        if form.is_valid():
            category = form.cleaned_data['category']
            
            # Use the entered expense_name for "other_expense", otherwise use the category name
            if category == 'other_expense':
                expense_name = form.cleaned_data['expense_name']  # Use user-entered name
            else:
                # Get the human-readable category name for non-'other_expense'
                expense_name = dict(Withdrawal.EXPENSE_CATEGORIES).get(category, category)
            
            amount = form.cleaned_data['amount']
            date = form.cleaned_data.get('date')

            # Check if the withdrawal amount exceeds the available balance
            available_balance = get_available_balance()  # You need to define this function based on your model
            if amount > available_balance:
                form.add_error('amount', 'رقم دستیاب بیلنس سے زیادہ نہیں ہو سکتی۔')
                return render(request, 'finance/withdraw.html', {'form': form})

            # Create the withdrawal record
            Withdrawal.objects.create(
                category=category,
                expense_name=expense_name,  # Save the correct name here
                amount=amount,
                date = date
            )
            return render(request, 'finance/dashboard.html')  # Success page
    else:
        form = WithdrawalForm()

    return render(request, 'finance/withdraw.html', {'form': form})


from django.shortcuts import render
from django.db.models import Sum
from .models import Deposit, Withdrawal
from datetime import datetime

from datetime import datetime
from django.db.models import Sum

def check_balance(request):
    balance_type = request.GET.get('balance_type', 'deposit')  # Default to deposit
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    records = []
    deposit_total = None
    withdraw_total = None
    available_balance = None

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if balance_type == 'deposit':
                records = Deposit.objects.filter(date__range=(start_date, end_date))
                deposit_total = records.aggregate(Sum('amount'))['amount__sum'] or 0
            elif balance_type == 'withdraw':
                records = Withdrawal.objects.filter(date__range=(start_date, end_date))
                withdraw_total = records.aggregate(Sum('amount'))['amount__sum'] or 0
            elif balance_type == 'available_balance':
                deposits = Deposit.objects.filter(date__range=(start_date, end_date))
                withdrawals = Withdrawal.objects.filter(date__range=(start_date, end_date))
                deposit_total = deposits.aggregate(Sum('amount'))['amount__sum'] or 0
                withdraw_total = withdrawals.aggregate(Sum('amount'))['amount__sum'] or 0
                available_balance = deposit_total - withdraw_total

        except ValueError:
            records = []
            deposit_total = None
            withdraw_total = None
            available_balance = None

    # Map fund names to their Urdu equivalents
    FUND_TYPES_MAP = {
        'TH1': 'جمعرات پہلا وقت',
        'TH2': 'جمعرات دوسرا وقت',
        'FR': 'جمعہ فنڈ',
        'MS': 'مولوی کی ماہانہ تنخواہ',
    }
    for record in records:
        if hasattr(record, 'fund') and record.fund.name in FUND_TYPES_MAP:
            if balance_type == 'deposit':
                record.fund.urdu_name = FUND_TYPES_MAP[record.fund.name]
            elif balance_type == 'withdraw':
                record.expense_name = FUND_TYPES_MAP[record.expense_name]
        else:
            if balance_type == 'deposit':
                record.fund.urdu_name = record.fund.name  # Fallback to the original name
            elif balance_type == 'withdraw':
                record.expense_name = record.expense_name  # Fallback to the original name

    context = {
        'balance_type': balance_type,
        'start_date': start_date,
        'end_date': end_date,
        'records': records,
        'deposit_total': deposit_total,
        'withdraw_total': withdraw_total,
        'available_balance': available_balance,
    }
    return render(request, 'finance/check_balance.html', context)

def get_available_balance():
    total_deposit = Deposit.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_withdraw = Withdrawal.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    available_balance = total_deposit - total_withdraw
    return available_balance
