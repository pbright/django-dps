from django.contrib.admin import SimpleListFilter
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Transaction, TransactionResult


class TransactionResultInline(admin.TabularInline):
    readonly_fields = ('result', )
    model = TransactionResult

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ContentTypeFilter(SimpleListFilter):
    title = 'purchase type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        ctypes = Transaction.objects.values_list(
            'content_type__id', 'content_type__app_label',
            'content_type__model') \
            .order_by('content_type__id').distinct()
        return [(c[0], (u"%s: %s" % c[1:]).title()) for c in ctypes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(content_type__id__exact=self.value())
        else:
            return queryset


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'status', 'transaction_type',
                    'content_object', 'created',)
    inlines = (TransactionResultInline, )
    search_fields = ('secret', )
    list_filter = (ContentTypeFilter, )


class TransactionInlineAdmin(GenericTabularInline):
    model = Transaction
    fields = ('created', 'transaction_type', 'status', 'amount',
              'transaction_result')
    readonly_fields = ('created', 'transaction_type', 'status', 'amount',
                       'transaction_result')
    extra = 0

    def transaction_result(self, obj=None):
        """
        Support both old and new style result.
        """
        if obj:
            trans_result = getattr(obj, 'trans_result', None)
            if trans_result:
                return trans_result.result
            else:
                return obj.result
        return ''

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Transaction, TransactionAdmin)
