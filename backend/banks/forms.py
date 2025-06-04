from django import forms
from . import models


class RecordMappingForm(forms.Form):
    file = forms.FileField(required=True, label="File (The bank records)", help_text="Upload a CSV or Excel file", allow_empty_file=False)
    bank_name = forms.ModelChoiceField(queryset=models.Bank.objects.all(), required=True, label="Bank Name", help_text="Select the bank name from the list", empty_label="Select a bank")
    customer_bvn = forms.CharField(max_length=255, required=False, label="Customer BVN Column", help_text="Enter the column name for customer BVN")
    customer_nuban = forms.CharField(max_length=255, required=False, label="Customer NUBAN Column", help_text="Enter the column name for customer NUBAN")
    customer_email = forms.CharField(max_length=255, required=False, label="Customer Email Column", help_text="Enter the column name for customer email")
    customer_mobile = forms.CharField(max_length=255, required=False, label="Customer Mobile Column", help_text="Enter the column name for customer mobile")
    customer_tin = forms.CharField(max_length=255, required=False, label="Customer TIN Column", help_text="Enter the column name for customer TIN")
    customer_passport = forms.CharField(max_length=255, required=False, label="Customer Passport Column", help_text="Enter the column name for customer passport")
    customer_name = forms.CharField(max_length=255, required=False, label="Customer Name Column", help_text="Enter the column name for customer name")
    customer_address = forms.CharField(max_length=255, required=False, label="Customer Address Column", help_text="Enter the column name for customer address")
    customer_dob = forms.CharField(max_length=255, required=False, label="Customer DOB Column", help_text="Enter the column name for customer date of birth")
    amount = forms.CharField(max_length=255, required=True, label="Amount Column", help_text="Enter the column name for transaction amount")
    narration = forms.CharField(max_length=255, required=False, label="Narration Column", help_text="Enter the column name for transaction narration")
    date = forms.CharField(max_length=255, required=True, label="Date Column", help_text="Enter the column name for transaction date")
    transaction_type = forms.CharField(max_length=255, required=False, label="Transaction Type Column", help_text="Enter the column name for transaction type")