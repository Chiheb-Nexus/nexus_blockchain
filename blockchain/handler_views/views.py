#
#
#
#

from django.shortcuts import render


def Handler404(request, exception, *args, **kawargs):
    return render(request, 'errors/error404.html', {'error': exception})

def Handler500(request, *args, **kwargs):
    return render(request, 'errors/error500.html', {'error': '500'})