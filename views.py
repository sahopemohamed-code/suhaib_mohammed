from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count

from .models import Station, Route
from .forms import RegisterForm


def index(request):
    query = request.GET.get('q', '').strip()
    routes = Route.objects.select_related('origin', 'destination').annotate(
        passenger_count=Count('passengers')
    )
    if query:
        routes = routes.filter(
            Q(origin__name__icontains=query) |
            Q(origin__city__icontains=query) |
            Q(destination__name__icontains=query) |
            Q(destination__city__icontains=query)
        )
    return render(request, 'routes/index.html', {'routes': routes, 'query': query})


def route_detail(request, route_id):
    route = get_object_or_404(
        Route.objects.select_related('origin', 'destination').prefetch_related('passengers'),
        pk=route_id
    )
    is_booked = request.user.is_authenticated and route.passengers.filter(pk=request.user.pk).exists()
    return render(request, 'routes/detail.html', {
        'route': route,
        'is_booked': is_booked,
    })


@login_required
def book_route(request, route_id):
    if request.method == 'POST':
        route = get_object_or_404(Route, pk=route_id)
        route.passengers.add(request.user)
        messages.success(request, f'Successfully booked seat on {route}!')
    return redirect('route_detail', route_id=route_id)


@login_required
def unbook_route(request, route_id):
    if request.method == 'POST':
        route = get_object_or_404(Route, pk=route_id)
        route.passengers.remove(request.user)
        messages.info(request, f'Booking cancelled for {route}.')
    return redirect('route_detail', route_id=route_id)


@login_required
def my_routes(request):
    routes = request.user.booked_trips.select_related('origin', 'destination').annotate(
        passenger_count=Count('passengers')
    )
    return render(request, 'routes/my_routes.html', {'routes': routes})


def station_detail(request, station_id):
    station = get_object_or_404(Station, pk=station_id)
    departing = Route.objects.filter(origin=station).select_related('destination').annotate(
        passenger_count=Count('passengers')
    )
    arriving = Route.objects.filter(destination=station).select_related('origin').annotate(
        passenger_count=Count('passengers')
    )
    return render(request, 'routes/station.html', {
        'station': station,
        'departing': departing,
        'arriving': arriving,
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Account created successfully.')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'routes/register.html', {'form': form})
