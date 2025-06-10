import pandas as pd
import io
from .forms import RecordMappingForm
from . import models
from django.db.models import Q
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
import dateparser
from django.utils import timezone


# def get_cell_value(row: pd.Series, column: str | None):
#     if not column or not column.strip():
#         return None
#     r = row.get(column)
#     if pd.isna(r) or pd.isnull(r):
#         return None
#     return str(r).strip().lower()


# def upload_records(
#         mapping: dict,
#         task=None,  # Optional: task for tracking progress
# ):
#     # task = BackgroundTaskRepository.create_task(
#     #     session,
#     #     BackgroundTaskCreate(
#     #         name=file["name"],
#     #         status=BackgroundTaskStatus.pending,
#     #         description=f"Create transactions from uploaded file ({file['name']})",
#     #     )
#     # )
#     errors = []
#     file = mapping["file"]

#     try:
#         # f_content = io.BytesIO(file["content"])
#         f_content = io.BytesIO(file['content'])
#         accepted_types = {
#             "text/csv": lambda: pd.read_csv(f_content),
#             "application/vnd.ms-excel": lambda: pd.read_excel(f_content, engine="openpyxl"),
#             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": lambda: pd.read_excel(f_content, engine="openpyxl"),
#         }
#         # if file["type"] not in accepted_types.keys():
#             # raise Exception(f"Unsupported file type: {file['type']}")
#         # df = accepted_types[file["type"]]()
#         if file['type'] not in accepted_types.keys():
#             raise Exception(f"Unsupported file type: {file['type']}")
#         df = accepted_types[file['type']]()
#         # df = df.astype(str)
#         # df = df.where(pd.notna(df), None)
#         count = 0

#         # bank = BankServices.get_or_create(
#         #     session, banks.BankCreate(name=mapping.bank_name)
#         # )
#         bank = models.Bank.objects.get_or_create(name=mapping['bank_name'])[0]
#         # task.status = BackgroundTaskStatus.in_progress
#         # task.description = f"Create transactions from uploaded file ({file['name']}) for ({bank.name}) bank"
#         # task.result = f"0|{count}/{len(df)}"
#         # session.commit()
#         if task:
#             task.update_state(
#                 state='STARTED',
#                 meta={
#                     'processed': count,
#                     'current': 0,
#                     'total': len(df),
#                     'status': f"Processing {file['name']} for {bank.name} bank (0)%",
#                     'errors': errors,
#                 }
#             )
#         for index, row in df.iterrows():
#             bvn = get_cell_value(row, mapping['customer_bvn'])
#             nuban = get_cell_value(row, mapping['customer_nuban'])
#             email = get_cell_value(row, mapping['customer_email'])
#             mobile = get_cell_value(row, mapping['customer_mobile'])
#             tin = get_cell_value(row, mapping['customer_tin'])
#             passport = get_cell_value(row, mapping['customer_passport'])
#             name = get_cell_value(row, mapping['customer_name'])
#             address = get_cell_value(row, mapping['customer_address'])
#             amount = get_cell_value(row, mapping['amount'])
#             narration = get_cell_value(row, mapping['narration'])
#             date = get_cell_value(row, mapping['date'])
#             if date:
#                 date = dateparser.parse(date)
#                 if timezone.is_naive(date):
#                     date = timezone.make_aware(date)
#             transaction_type = get_cell_value(row, mapping['transaction_type'])

#             filters = Q()  # Start with an empty Q object

#             if bvn:
#                 filters |= Q(bvns__bvn=bvn)
#             if nuban:
#                 filters |= Q(nubans__nuban=nuban)
#             if email:
#                 filters |= Q(emails__email=email)
#             if mobile:
#                 filters |= Q(mobiles__mobile=mobile)
#             if tin:
#                 filters |= Q(tins__tin=tin)
#             if passport:
#                 filters |= Q(passports__passport=passport)

#             customer = models.Customer.objects.filter(filters).distinct()[:1]
#             # Check if customer exists
#             if not customer:
#                 # Create new customer
#                 customer = models.Customer.objects.create()
#             else:
#                 customer = customer[0]
#             # Add new details to customer
#             # BVN
#             if bvn:
#                 bvns = [models.CustomerBVN.objects.get_or_create(bvn=x, customer=customer)
#                         for x in bvn.split(",")]
#             # NUBAN
#             if nuban:
#                 nubans = [models.CustomerNUBAN.objects.get_or_create(nuban=x, customer=customer)
#                             for x in nuban.split(",")]
#             # Email
#             if email:
#                 emails = [models.CustomerEmail.objects.get_or_create(email=x, customer=customer)
#                             for x in email.split(",")]
#             # Mobile
#             if mobile:
#                 mobiles = [models.CustomerMobile.objects.get_or_create(mobile=x, customer=customer)
#                             for x in mobile.split(",")]
#             # TIN
#             if tin:
#                 tins = [models.CustomerTIN.objects.get_or_create(tin=x, customer=customer)
#                         for x in tin.split(",")]
#             # Passport
#             if passport:
#                 passports = [models.CustomerPassport.objects.get_or_create(passport=x, customer=customer)
#                                 for x in passport.split(",")]
#             # Name
#             if name:
#                 names = [models.CustomerName.objects.get_or_create(name=x, customer=customer)
#                         for x in name.split(",")]
#             # Address
#             if address:
#                 address = models.CustomerAddress.objects.get_or_create(address=address, customer=customer)
#             try:
#                 with transaction.atomic():
#                     models.BankTransaction.objects.create(
#                         amount=amount,
#                         transaction_type=transaction_type if transaction_type in {'debit', 'credit'} else None,
#                         narration=narration,
#                         date=date,
#                         bank=bank,
#                         customer=customer
#                     )
#                 count += 1
#             except Exception as e:
#                 errors.append({
#                     'row': index + 1,
#                     'error': str(e),
#                 })
#             #     logger.error(f"{file['name']}: {date} -> {e}")
#             #     task.error = f"{task.error}\n\n{e}: {str(row)}".strip()
#             #     session.commit()
#             # task.result = f"{count}|{index+1}/{len(df)}"
#             # session.commit()
#             if task:
#                 task.update_state(
#                     state='STARTED',
#                     meta={
#                         'processed': count,
#                         'current': index + 1,
#                         'total': len(df),
#                         'status': f"Processing {file['name']} for {bank.name} bank ({(index + 1) * 100 // len(df)}%)",
#                         'errors': errors,
#                     }
#                 )
#     except Exception as e:
#         # logger.error(f"{e}")
#         # task.error = f"{task.error}\n\n{e}".strip()
#         # task.status = BackgroundTaskStatus.failed
#         # session.commit()
#         raise e
#     # task.status = BackgroundTaskStatus.completed
#     # session.commit()
#     if task:
#         task.update_state(
#             state='SUCCESS',
#             meta={
#                 'processed': count,
#                 'current': len(df),
#                 'total': len(df),
#                 'status': f"Completed processing {file['name']} for {bank.name} bank ({100}%)",
#                 'errors': errors,
#             }
#         )
#     return count


def get_cell_values(row: pd.Series, column: list[str] | None):
    if not column or not column.strip():
        return None
    r = row.get(column)
    if pd.isna(r) or pd.isnull(r):
        return None
    return str(r).strip().lower().split(",") if isinstance(r, str) else [str(r)]


def upload_records(
        mapping: dict,
        task=None,  # Optional: task for tracking progress
):
    # task = BackgroundTaskRepository.create_task(
    #     session,
    #     BackgroundTaskCreate(
    #         name=file["name"],
    #         status=BackgroundTaskStatus.pending,
    #         description=f"Create transactions from uploaded file ({file['name']})",
    #     )
    # )
    errors = []
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
        if task:
            task.update_state(
                state='STARTED',
                meta={
                    'processed': count,
                    'current': 0,
                    'total': len(df),
                    'status': f"Processing {file['name']} for {bank.name} bank (0)%",
                    'errors': errors,
                }
            )
        for index, row in df.iterrows():
            bvn = get_cell_values(row, mapping['customer_bvn'])
            nuban = get_cell_values(row, mapping['customer_nuban'])
            email = get_cell_values(row, mapping['customer_email'])
            mobile = get_cell_values(row, mapping['customer_mobile'])
            tin = get_cell_values(row, mapping['customer_tin'])
            passport = get_cell_values(row, mapping['customer_passport'])
            name = get_cell_values(row, mapping['customer_name'])
            address = get_cell_values(row, mapping['customer_address'])
            if address:
                # Join multiple addresses with a comma
                address = ','.join(address)
            amount = get_cell_values(row, mapping['amount'])
            if amount:
                amount = ''.join(amount)
            narration = get_cell_values(row, mapping['narration'])
            if narration:
                # Join multiple narrations with a comma
                narration = ','.join(narration)
            date = get_cell_values(row, mapping['date'])
            if date:
                # Assuming date is a list with one element
                date = dateparser.parse(date[0])
                if timezone.is_naive(date):
                    date = timezone.make_aware(date)
            transaction_type = get_cell_values(
                row, mapping['transaction_type'])
            if transaction_type and transaction_type[0] in {'debit', 'credit'}:
                transaction_type = transaction_type[0]
            else:
                transaction_type = None

            # filters = Q()  # Start with an empty Q object

            # if bvn:
            #     filters |= Q(bvns__bvn=bvn)
            # if nuban:
            #     filters |= Q(nubans__nuban=nuban)
            # if email:
            #     filters |= Q(emails__email=email)
            # if mobile:
            #     filters |= Q(mobiles__mobile=mobile)
            # if tin:
            #     filters |= Q(tins__tin=tin)
            # if passport:
            #     filters |= Q(passports__passport=passport)

            # customer = models.Customer.objects.filter(filters).distinct()[:1]
            # # Check if customer exists
            # if not customer:
            #     # Create new customer
            #     customer = models.Customer.objects.create()
            # else:
            #     customer = customer[0]
            # # Add new details to customer
            # # BVN
            # if bvn:
            #     bvns = [models.CustomerBVN.objects.get_or_create(bvn=x, customer=customer)
            #             for x in bvn.split(",")]
            # # NUBAN
            # if nuban:
            #     nubans = [models.CustomerNUBAN.objects.get_or_create(nuban=x, customer=customer)
            #                 for x in nuban.split(",")]
            # # Email
            # if email:
            #     emails = [models.CustomerEmail.objects.get_or_create(email=x, customer=customer)
            #                 for x in email.split(",")]
            # # Mobile
            # if mobile:
            #     mobiles = [models.CustomerMobile.objects.get_or_create(mobile=x, customer=customer)
            #                 for x in mobile.split(",")]
            # # TIN
            # if tin:
            #     tins = [models.CustomerTIN.objects.get_or_create(tin=x, customer=customer)
            #             for x in tin.split(",")]
            # # Passport
            # if passport:
            #     passports = [models.CustomerPassport.objects.get_or_create(passport=x, customer=customer)
            #                     for x in passport.split(",")]
            # # Name
            # if name:
            #     names = [models.CustomerName.objects.get_or_create(name=x, customer=customer)
            #             for x in name.split(",")]
            # # Address
            # if address:
            #     address = models.CustomerAddress.objects.get_or_create(address=address, customer=customer)

            def update_all(customer: models.Customer):
                if bvn:
                    models.CustomerBVN.objects.bulk_create(
                        [models.CustomerBVN(bvn=x, customer=customer)
                        for x in bvn if x],
                        ignore_conflicts=True
                    )
                if nuban:
                    models.CustomerNUBAN.objects.bulk_create(
                        [models.CustomerNUBAN(nuban=x, customer=customer)
                        for x in nuban if x],
                        ignore_conflicts=True
                    )
                if email:
                    models.CustomerEmail.objects.bulk_create(
                        [models.CustomerEmail(email=x, customer=customer)
                        for x in email if x],
                        ignore_conflicts=True
                    )
                if mobile:
                    models.CustomerMobile.objects.bulk_create(
                        [models.CustomerMobile(
                            mobile=x, customer=customer) for x in mobile if x],
                        ignore_conflicts=True
                    )
                if tin:
                    models.CustomerTIN.objects.bulk_create(
                        [models.CustomerTIN(tin=x, customer=customer)
                        for x in tin if x],
                        ignore_conflicts=True
                    )
                if passport:
                    models.CustomerPassport.objects.bulk_create(
                        [models.CustomerPassport(
                            passport=x, customer=customer) for x in passport if x],
                        ignore_conflicts=True
                    )
                if name:
                    models.CustomerName.objects.bulk_create(
                        [models.CustomerName(name=x, customer=customer)
                        for x in name if x],
                        ignore_conflicts=True
                    )
                if address:
                    try:
                        models.CustomerAddress.objects.create(
                            address=address, customer=customer)
                    except:
                        pass

            customer = None
            try:
                # Identities to populate customer
                db_email = models.CustomerEmail.objects.filter(
                    email__in=email).first() if email else None
                if db_email:
                    customer = db_email.customer
                    update_all(customer)
                    raise
                
                db_mobile = models.CustomerMobile.objects.filter(
                    mobile__in=mobile).first() if mobile else None
                if db_mobile:
                    customer = db_mobile.customer
                    update_all(customer)
                    raise

                db_bvn = models.CustomerBVN.objects.filter(
                    bvn__in=bvn).first() if bvn else None
                if db_bvn:
                    customer = db_bvn.customer
                    update_all(customer)
                    raise
                
                db_nuban = models.CustomerNUBAN.objects.filter(
                    nuban__in=nuban).first() if nuban else None
                if db_nuban:
                    customer = db_nuban.customer
                    update_all(customer)
                    raise
                
                # There has been issue with TINs (not stable), so we are not using it for now
                # db_tin = models.CustomerTIN.objects.filter(
                #     tin__in=tin).first() if tin else None
                # if db_tin:
                #     customer = db_tin.customer
                #     update_all(customer)
                #     raise
                
                db_passport = models.CustomerPassport.objects.filter(
                    passport__in=passport).first() if passport else None
                if db_passport:
                    customer = db_passport.customer
                    update_all(customer)
                    raise

            except:
                pass
            else:
                if not customer:
                    customer = models.Customer.objects.create()
                    if email or mobile or bvn or nuban or passport: # Add `tin` when stable
                        update_all(customer)
                    else:
                        # If no identities, write to a log file
                        pass

            try:
                with transaction.atomic():
                    models.BankTransaction.objects.create(
                        amount=amount,
                        transaction_type=transaction_type,
                        narration=narration,
                        date=date,
                        bank=bank,
                        customer=customer
                    )
                count += 1
            except Exception as e:
                errors.append({
                    'row': index + 1,
                    'error': str(e),
                })
            #     logger.error(f"{file['name']}: {date} -> {e}")
            #     task.error = f"{task.error}\n\n{e}: {str(row)}".strip()
            #     session.commit()
            # task.result = f"{count}|{index+1}/{len(df)}"
            # session.commit()
            if task:
                task.update_state(
                    state='STARTED',
                    meta={
                        'processed': count,
                        'current': index + 1,
                        'total': len(df),
                        'status': f"Processing {file['name']} for {bank.name} bank ({(index + 1) * 100 // len(df)}%)",
                        'errors': errors,
                    }
                )
    except Exception as e:
        # logger.error(f"{e}")
        # task.error = f"{task.error}\n\n{e}".strip()
        # task.status = BackgroundTaskStatus.failed
        # session.commit()
        raise e
    # task.status = BackgroundTaskStatus.completed
    # session.commit()
    if task:
        task.update_state(
            state='SUCCESS',
            meta={
                'processed': count,
                'current': len(df),
                'total': len(df),
                'status': f"Completed processing {file['name']} for {bank.name} bank ({100}%)",
                'errors': errors,
            }
        )
    return count
