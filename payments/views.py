from django.views.generic import TemplateView
from django.shortcuts import render
from .accesstokengenerate import get_access_token
from .stkpush import initiate_stk_push
from .query import query_stk_status

class HomePageView(TemplateView):
    template_name = "employee-registration.html"

