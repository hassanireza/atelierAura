from django.contrib import admin
from .models import Plan, PlanFeature, Cart, CartItem, Order, OrderItem


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 3


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'price', 'is_featured', 'is_active', 'order')
    list_editable = ('is_featured', 'is_active', 'order', 'price')
    inlines = [PlanFeatureInline]
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('plan_name', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'stripe_payment_intent')
    inlines = [OrderItemInline]
    readonly_fields = ('order_id', 'created_at', 'updated_at')
