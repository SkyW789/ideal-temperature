from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return redirect("temperature/current_status/")
    #return HttpResponse("This is the main page.")
