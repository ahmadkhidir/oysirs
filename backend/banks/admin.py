import nested_admin
from django.contrib import admin
from . import models
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from . import models
from .forms import RecordMappingForm
from .tasks import upload_records_task
from django.db.models import Sum
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.utils.timezone import now


class TransactionDateFilter(admin.SimpleListFilter):
    title = _('Transaction Date')
    parameter_name = 'transaction_date'

    def lookups(self, request, model_admin):
        return [
            ('custom', _('Custom Range')),
        ]

    def queryset(self, request, queryset):
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        if from_date and to_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
                return queryset.filter(transactions__date__range=(from_date, to_date))
            except ValueError:
                pass
        return queryset


admin.site.register([
    models.CustomerName,
    models.CustomerAddress,
    models.CustomerNUBAN,
    models.CustomerMobile,
    models.CustomerBVN,
    models.CustomerEmail,
    models.CustomerTIN,
    models.CustomerPassport,
    models.Bank,
])


class CustomerNameInline(nested_admin.NestedTabularInline):
    model = models.CustomerName
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return super().has_add_permission(request, obj)
        return False  # Disable adding new records

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False  # Disable editing existing records


class CustomerAddressInline(nested_admin.NestedTabularInline):
    model = models.CustomerAddress
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return super().has_add_permission(request, obj)
        return False  # Disable adding new records

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False  # Disable editing existing records


class CustomerNUBANInline(nested_admin.NestedTabularInline):
    model = models.CustomerNUBAN
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return super().has_add_permission(request, obj)
        return False  # Disable adding new records

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False  # Disable editing existing records


class CustomerMobileInline(nested_admin.NestedTabularInline):
    model = models.CustomerMobile
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return super().has_add_permission(request, obj)
        return False  # Disable adding new records

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False  # Disable editing existing records


class CustomerBVNInline(nested_admin.NestedTabularInline):
    model = models.CustomerBVN
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return super().has_add_permission(request, obj)
        return False  # Disable adding new records

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False  # Disable editing existing records


class CustomerEmailInline(nested_admin.NestedTabularInline):
    model = models.CustomerEmail
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return super().has_add_permission(request, obj)
        return False  # Disable adding new records

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False  # Disable editing existing records


class CustomerTINInline(nested_admin.NestedTabularInline):
    model = models.CustomerTIN
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return super().has_add_permission(request, obj)
        return False  # Disable adding new records

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False  # Disable editing existing records


class CustomerPassportInline(nested_admin.NestedTabularInline):
    model = models.CustomerPassport
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return super().has_add_permission(request, obj)
        return False  # Disable adding new records

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return False  # Disable editing existing records


class BankTransactionInline(nested_admin.NestedTabularInline):
    model = models.BankTransaction
    extra = 0
    fieldsets = (
        (None, {
            "fields": (
                "transaction_type",
                "amount",
                "date",
                "narration",
                "bank",
            ),
        }),
    )


@admin.register(models.BankTransaction)
class BankTransactionAdmin(nested_admin.NestedModelAdmin):
    list_display = ("amount", "date", "bank", "transaction_type")
    list_filter = ("transaction_type", "bank__name")
    search_fields = ("narration", "bank__name")
    fieldsets = (
        (None, {
            "fields": (
                "customer",
                "transaction_type",
                "amount",
                "date",
                "narration",
                "bank",
            ),
        }),
    )


@admin.register(models.Customer)
class CustomerAdmin(nested_admin.NestedModelAdmin, admin.ModelAdmin):
    add_form_template = "banks/customer/add_form.html"
    change_form_template = "banks/customer/change_form.html"
    fieldsets = (
        ("Summary", {"fields": ("customer_total_transactions", "customer_total_amount", "bank_transaction_summary")}),
    )
    readonly_fields = ["customer_total_transactions", "customer_total_amount", "bank_transaction_summary"]
    list_per_page = 20
    list_max_show_all = 100
    inlines = [
        CustomerNameInline,
        CustomerMobileInline,
        CustomerEmailInline,
        CustomerAddressInline,
        CustomerBVNInline,
        CustomerNUBANInline,
        CustomerTINInline,
        CustomerPassportInline,
        # BankTransactionInline,
    ]

    def get_fieldsets(self, request, obj = ...):
        if obj is None:
            return ()
        return super().get_fieldsets(request, obj)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Add from_date and to_date filters to the change view context.
        """
        extra_context = extra_context or {}
        extra_context['from_date'] = request.GET.get('from_date', '')
        extra_context['to_date'] = request.GET.get('to_date', now().strftime('%Y-%m-%d'))
        self.request = request  # Store the request object for use in other methods
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
    
    def get_search_fields(self, request):
        """
        Dynamically set search_fields based on user permissions.
        """
        search_fields = ["names__name", "emails__email", "mobiles__mobile"]
        if request.user.has_perm("banks.view_customerbvn"):
            search_fields.append("bvns__bvn")
        if request.user.has_perm("banks.view_customernuban"):
            search_fields.append("nubans__nuban")
        if request.user.has_perm("banks.view_customertin"):
            search_fields.append("tins__tin")
        return search_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('names', 'bvns', 'nubans', 'emails', 'mobiles', 'tins')

    def get_list_display(self, request):
        """
        Dynamically set list_display based on user permissions.
        """
        list_display = ["__str__", "name", "email", "mobile"]
        if request.user.has_perm("banks.view_customerbvn"):
            list_display.append("bvn")
        if request.user.has_perm("banks.view_customernuban"):
            list_display.append("nuban")
        if request.user.has_perm("banks.view_customertin"):
            list_display.append("tin")
        return list_display

    def customer_total_transactions(self, obj):
        print(dir(obj))
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        transactions = obj.transactions.all()
        print("transactions", transactions)
        print("from_date", from_date)
        print("to_date", to_date)
        if from_date and to_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
                transactions = transactions.filter(date__range=(from_date, to_date))
            except ValueError:
                pass

        return transactions.count()
    customer_total_transactions.short_description = "Total Transactions"


    def customer_total_amount(self, obj):
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')

        transactions = obj.transactions.all()
        if from_date and to_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
                transactions = transactions.filter(date__range=(from_date, to_date))
            except ValueError:
                pass

        amount = transactions.aggregate(Sum('amount'))['amount__sum']
        return "₦{:,.2f}".format(amount) if amount else "₦0.00"
    customer_total_amount.short_description = "Total Amount"


    def bank_transaction_summary(self, obj):
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')

        transactions = obj.transactions.all()
        if from_date and to_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
                transactions = transactions.filter(date__range=(from_date, to_date))
            except ValueError:
                pass

        summary = "<div>"
        for transaction in transactions.values('bank__name').annotate(total_amount=Sum('amount')):
            summary += f"<p>{transaction['bank__name']}: ₦{transaction['total_amount']:,.2f}</p>"
        summary += "</div>"
        return format_html(summary)
    bank_transaction_summary.short_description = "Transaction Summary by Bank"

    # def add_view(self, request, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['mapping_form'] = RecordMappingForm()
    #     return super().add_view(request, form_url, extra_context=extra_context)

    # Add a custom view for file upload
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-file/', self.admin_site.admin_view(self.upload_file),
                 name='upload_records'),
        ]
        return custom_urls + urls

    def upload_file(self, request):
        if request.method == "POST":
            uploaded_form = RecordMappingForm(request.POST, request.FILES)
            if uploaded_form.is_valid():
                # Process the uploaded file
                # Example: Save the file, parse it, and create records
                # You can access the cleaned data using uploaded_form.cleaned_data
                # Example:
                # bank_name = uploaded_form.cleaned_data['bank_name']
                # file = uploaded_form.cleaned_data['file']
                # Perform your logic here
                cleaned_data = uploaded_form.cleaned_data
                file_object = {
                    "name": cleaned_data["file"].name,
                    "content": cleaned_data["file"].read(),
                    "type": cleaned_data["file"].content_type,
                }
                cleaned_data["file"] = file_object
                cleaned_data["bank_name"] = cleaned_data["bank_name"].name
                upload_records_task.delay_on_commit(cleaned_data)
                messages.success(request, "Task uploading started. Check the Task results section for updates.")
            else:
                messages.error(request, "Error in form submission.")
            return HttpResponseRedirect(request.path)
        context = {
            "title": "Upload Records",
            "subtitle": "Upload customers transactions records",
            "admin_site": self.admin_site,
            "admin_form": None,
            "form_url": request.path,
            "is_popup": False,
            "is_popup_var": None,
            "add": True,
            "change": False,
            "has_delete_permission": False,
            "has_change_permission": True,
            "has_absolute_url": False,
            "opts": self.opts,
            "original": None,
            "save_as": False,
            "show_save": True,
            **self.admin_site.each_context(request)
        }
        context['mapping_form'] = RecordMappingForm()
        return render(request, "banks/customer/upload_records.html", context=context)
