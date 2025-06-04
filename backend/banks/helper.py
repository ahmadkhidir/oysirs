import pandas as pd
import io
from .forms import RecordMappingForm
from . import models
from django.db.models import Q
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
import dateparser
from django.utils import timezone


def get_cell_value(row: pd.Series, column: str | None):
    if not column or not column.strip():
        return None
    r = row.get(column)
    if pd.isna(r) or pd.isnull(r):
        return None
    return str(r).strip().lower()


def upload_records(
        mapping: dict
):
    # task = BackgroundTaskRepository.create_task(
    #     session,
    #     BackgroundTaskCreate(
    #         name=file["name"],
    #         status=BackgroundTaskStatus.pending,
    #         description=f"Create transactions from uploaded file ({file['name']})",
    #     )
    # )
    file = mapping["file"]

    try:
        # f_content = io.BytesIO(file["content"])
        f_content = io.BytesIO(file['content'])
        accepted_types = {
            "text/csv": lambda: pd.read_csv(f_content),
            "application/vnd.ms-excel": lambda: pd.read_excel(f_content, engine="openpyxl"),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": lambda: pd.read_excel(f_content, engine="openpyxl"),
        }
        # if file["type"] not in accepted_types.keys():
            # raise Exception(f"Unsupported file type: {file['type']}")
        # df = accepted_types[file["type"]]()
        if file['type'] not in accepted_types.keys():
            raise Exception(f"Unsupported file type: {file['type']}")
        df = accepted_types[file['type']]()
        # df = df.astype(str)
        # df = df.where(pd.notna(df), None)
        count = 0

        # bank = BankServices.get_or_create(
        #     session, banks.BankCreate(name=mapping.bank_name)
        # )
        bank = models.Bank.objects.get_or_create(name=mapping['bank_name'])[0]
        # task.status = BackgroundTaskStatus.in_progress
        # task.description = f"Create transactions from uploaded file ({file['name']}) for ({bank.name}) bank"
        # task.result = f"0|{count}/{len(df)}"
        # session.commit()
        for index, row in df.iterrows():
            bvn = get_cell_value(row, mapping['customer_bvn'])
            nuban = get_cell_value(row, mapping['customer_nuban'])
            email = get_cell_value(row, mapping['customer_email'])
            mobile = get_cell_value(row, mapping['customer_mobile'])
            tin = get_cell_value(row, mapping['customer_tin'])
            passport = get_cell_value(row, mapping['customer_passport'])
            name = get_cell_value(row, mapping['customer_name'])
            address = get_cell_value(row, mapping['customer_address'])
            amount = get_cell_value(row, mapping['amount'])
            narration = get_cell_value(row, mapping['narration'])
            date = get_cell_value(row, mapping['date'])
            if date:
                date = dateparser.parse(date)
                if timezone.is_naive(date):
                    date = timezone.make_aware(date)
            transaction_type = get_cell_value(row, mapping['transaction_type'])

            filters = Q()  # Start with an empty Q object

            if bvn:
                filters |= Q(bvns__bvn=bvn)
            if nuban:
                filters |= Q(nubans__nuban=nuban)
            if email:
                filters |= Q(emails__email=email)
            if mobile:
                filters |= Q(mobiles__mobile=mobile)
            if tin:
                filters |= Q(tins__tin=tin)
            if passport:
                filters |= Q(passports__passport=passport)

            customer = models.Customer.objects.filter(filters).distinct()[:1]
            # Check if customer exists
            if not customer:
                # Create new customer
                customer = models.Customer.objects.create()
            else:
                customer = customer[0]
            # Add new details to customer
            # BVN
            if bvn:
                bvns = [models.CustomerBVN.objects.get_or_create(bvn=x, customer=customer)
                        for x in bvn.split(",")]
            # NUBAN
            if nuban:
                nubans = [models.CustomerNUBAN.objects.get_or_create(nuban=x, customer=customer)
                            for x in nuban.split(",")]
            # Email
            if email:
                emails = [models.CustomerEmail.objects.get_or_create(email=x, customer=customer)
                            for x in email.split(",")]
            # Mobile
            if mobile:
                mobiles = [models.CustomerMobile.objects.get_or_create(mobile=x, customer=customer)
                            for x in mobile.split(",")]
            # TIN
            if tin:
                tins = [models.CustomerTIN.objects.get_or_create(tin=x, customer=customer)
                        for x in tin.split(",")]
            # Passport
            if passport:
                passports = [models.CustomerPassport.objects.get_or_create(passport=x, customer=customer)
                                for x in passport.split(",")]
            # Name
            if name:
                names = [models.CustomerName.objects.get_or_create(name=x, customer=customer)
                        for x in name.split(",")]
            # Address
            if address:
                address = models.CustomerAddress.objects.get_or_create(address=address, customer=customer)
            try:
                with transaction.atomic():
                    models.BankTransaction.objects.create(
                        amount=amount,
                        transaction_type=transaction_type if transaction_type in {'debit', 'credit'} else None,
                        narration=narration,
                        date=date,
                        bank=bank,
                        customer=customer
                    )
                count += 1
            except Exception as e:
                pass
            #     logger.error(f"{file['name']}: {date} -> {e}")
            #     task.error = f"{task.error}\n\n{e}: {str(row)}".strip()
            #     session.commit()
            # task.result = f"{count}|{index+1}/{len(df)}"
            # session.commit()
    except Exception as e:
        # logger.error(f"{e}")
        # task.error = f"{task.error}\n\n{e}".strip()
        # task.status = BackgroundTaskStatus.failed
        # session.commit()
        raise e
    # task.status = BackgroundTaskStatus.completed
    # session.commit()
    return count
