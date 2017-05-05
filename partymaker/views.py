from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView, CreateView, ListView

from partymaker.forms import AuthForm, OrderForm
from partymaker.models import Order


class AuthView(FormView):
    template_name = 'auth_form.html'
    form_class = AuthForm

    def form_valid(self, form):
        user = authenticate(**form.cleaned_data)
        login(self.request, user)
        return super(AuthView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('order'))


class OrderView(CreateView):
    model = Order
    success_url = reverse_lazy('delete')
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'order'):
            return redirect('delete')
        return super(OrderView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(OrderView, self).get_form_kwargs()
        kwargs.update({'instance': Order(user=self.request.user)})
        return kwargs


class DeleteOrderView(DeleteView):
    model = Order
    success_url = reverse_lazy('order')

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'order'):
            return redirect('order')
        return super(DeleteOrderView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.order


class OrderListView(ListView):
    model = Order

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse('Forbidden '+request.META['REMOTE_ADDR'], status=401)
        return super(OrderListView, self).dispatch(request, *args, **kwargs)
