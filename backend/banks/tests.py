import os
from django.test import TestCase
from .helper import upload_records
from .forms import RecordMappingForm
from django.core.files.uploadedfile import SimpleUploadedFile


class BankTestCase(TestCase):
    def setUp(self):
        # Set up any initial data or state for the tests
        pass

    def test_bank_creation(self):
        # Test bank creation
        pass

    def test_customer_creation(self):
        # Test customer creation
        pass

    def test_customer_name_creation(self):
        # Test customer name creation
        pass

    def test_customer_address_creation(self):
        # Test customer address creation
        pass

    def test_customer_nuban_creation(self):
        # Test customer NUBAN creation
        pass

    def test_records_upload(self):
        # Test records upload
        file_path = os.path.join(
            os.path.dirname(__file__), 'test.xlsx'
        )

        with open(file_path, 'rb') as file:
            file_content = file.read()
            file_name = os.path.basename(file_path)
            file_type = "application/vnd.ms-excel"
        
        file = SimpleUploadedFile(
            name=file_name,
            content=file_content,
            content_type=file_type
        )

        mapping_form = {
            'file': file,
            'bank_name': 'Test Bank',
            'customer_bvn': 'BVN',
            'customer_nuban': 'NUBAN',
            'customer_email': 'E_MAIL',
            'customer_mobile': 'MOBILE_NO',
            'customer_tin': 'TIN',
            'customer_passport': 'PASSPORT_NO',
            'customer_name': 'CUSTOMER_NAME',
            'customer_address': 'CUSTOMER_ADDRESS',
            'customer_dob': 'DATE_OF_BIRTH',
            'amount': 'TRXN_AMT',
            'narration': 'NARRATION',
            'date': 'TRN_DT',
            'transaction_type': '',
        }

        form = RecordMappingForm(data=mapping_form, files=mapping_form)
        print(form.data)
        self.assertTrue(form.is_valid(), f"Form Error: {form.errors}")
        self.assertIsInstance(upload_records(form.cleaned_data), str | int)
