from django.contrib import admin

# Register your models here.

from .models import MembershipPlan, Transaction

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_months', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'amount', 'status', 'timestamp')
    search_fields = ('user__username', 'razorpay_order_id', 'razorpay_payment_id')
    list_filter = ('status', 'timestamp')
