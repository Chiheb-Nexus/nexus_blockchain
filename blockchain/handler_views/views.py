#
# Custom errors
#
#
"""Custom errors"""

from django.shortcuts import render


def handler404(request, exception, *args, **kawargs):
    '''Return custom 404 error'''
    return render(request, 'errors/error404.html', {'error': exception})


def handler500(request, *args, **kwargs):
    '''Return custom 500 error'''
    return render(request, 'errors/error500.html', {'error': '500'})
