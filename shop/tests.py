from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Plan, PlanFeature, Cart, CartItem, Order, OrderItem


def make_plan(name='Starter', price=799, featured=False, order=1):
    p = Plan.objects.create(name=name, slug=name.lower(), plan_type='starter',
                            price=price, is_featured=featured, order=order)
    PlanFeature.objects.create(plan=p, text='Feature 1', order=1)
    return p


class PlansViewTest(TestCase):
    def test_plans_200(self):
        make_plan()
        r = self.client.get(reverse('plans'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Starter')

    def test_plans_empty(self):
        r = self.client.get(reverse('plans'))
        self.assertEqual(r.status_code, 200)


class CartTest(TestCase):
    def setUp(self):
        self.plan = make_plan()
        self.user = User.objects.create_user('cartuser', password='pass99!')

    def test_cart_empty(self):
        r = self.client.get(reverse('cart'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'empty')

    def test_add_to_cart_ajax(self):
        self.client.login(username='cartuser', password='pass99!')
        r = self.client.post(
            reverse('add_to_cart', args=[self.plan.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 1)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_add_same_plan_increments_quantity(self):
        self.client.login(username='cartuser', password='pass99!')
        url = reverse('add_to_cart', args=[self.plan.id])
        self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        item = CartItem.objects.get(plan=self.plan)
        self.assertEqual(item.quantity, 2)

    def test_remove_from_cart(self):
        self.client.login(username='cartuser', password='pass99!')
        self.client.post(reverse('add_to_cart', args=[self.plan.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        item = CartItem.objects.first()
        r = self.client.post(reverse('remove_from_cart', args=[item.id]))
        self.assertRedirects(r, reverse('cart'))
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_total(self):
        self.client.login(username='cartuser', password='pass99!')
        self.client.post(reverse('add_to_cart', args=[self.plan.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.get_total(), 799)


class CheckoutTest(TestCase):
    def setUp(self):
        self.plan = make_plan()
        self.user = User.objects.create_user('checkoutuser', password='pass99!')

    def test_checkout_empty_cart_redirects(self):
        self.client.login(username='checkoutuser', password='pass99!')
        r = self.client.get(reverse('checkout'))
        self.assertRedirects(r, reverse('plans'))

    def test_checkout_with_items(self):
        self.client.login(username='checkoutuser', password='pass99!')
        self.client.post(reverse('add_to_cart', args=[self.plan.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        r = self.client.get(reverse('checkout'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Place Order')


class OrderTest(TestCase):
    def setUp(self):
        self.plan = make_plan()
        self.user = User.objects.create_user('orderuser', password='pass99!')

    def test_place_order_creates_order(self):
        self.client.login(username='orderuser', password='pass99!')
        self.client.post(reverse('add_to_cart', args=[self.plan.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        r = self.client.post(reverse('place_order'))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.status, 'paid')
        self.assertEqual(order.user, self.user)
        self.assertEqual(OrderItem.objects.count(), 1)
        # Cart cleared
        self.assertEqual(CartItem.objects.count(), 0)

    def test_place_order_empty_cart(self):
        self.client.login(username='orderuser', password='pass99!')
        r = self.client.post(reverse('place_order'))
        self.assertRedirects(r, reverse('plans'))
        self.assertEqual(Order.objects.count(), 0)

    def test_order_success_page(self):
        self.client.login(username='orderuser', password='pass99!')
        self.client.post(reverse('add_to_cart', args=[self.plan.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        r = self.client.post(reverse('place_order'), follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Order Confirmed')

    def test_guest_can_place_order(self):
        # Guest (no login)
        self.client.post(reverse('add_to_cart', args=[self.plan.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        r = self.client.post(reverse('place_order'))
        self.assertEqual(r.status_code, 302)
        order = Order.objects.first()
        self.assertIsNone(order.user)
        self.assertEqual(order.status, 'paid')
