from django.shortcuts import render

# Create your views here.
def index(request):
    fsum_array = [0.1, 0.2, 0.3, 0.4]
    return render(request, "index.html", {"fsum_array": fsum_array})