from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ApplicationForm,
    LoginForm,
    RegistrationForm,
    ReviewForm,
    StatusForm,
)
from .models import Application


ADMIN_LOGIN = 'Admin26'
ADMIN_PASSWORD = 'Demo20'


def home(request):
    """Главная — лендинг с краткой информацией о портале."""
    return render(request, 'main/home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('cabinet')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Добро пожаловать!')
            return redirect('cabinet')
        messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('cabinet')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if username == ADMIN_LOGIN:
                    return redirect('admin_panel')
                return redirect('cabinet')
            messages.error(request, 'Неверный логин или пароль.')
        else:
            messages.error(request, 'Заполните оба поля.')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')


@login_required
def cabinet(request):
    """Личный кабинет — история заявок и форма отзыва."""
    applications = (
        Application.objects.filter(user=request.user)
        .select_related('review')
        .order_by('-created_at')
    )
    review_form = ReviewForm()
    return render(
        request,
        'main/cabinet.html',
        {'applications': applications, 'review_form': review_form},
    )


@login_required
def apply_view(request):
    """Страница оформления заявки на обучение."""
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.status = Application.STATUS_NEW
            app.save()
            messages.success(request, 'Заявка отправлена на согласование администратору.')
            return redirect('cabinet')
        messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ApplicationForm()
    return render(request, 'main/apply.html', {'form': form})


@login_required
def leave_review(request, app_id):
    """Оставить отзыв — доступно только после смены статуса администратором."""
    app = get_object_or_404(Application, pk=app_id, user=request.user)
    if not app.can_be_reviewed:
        messages.error(request, 'Отзыв можно оставить только после начала обучения.')
        return redirect('cabinet')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.application = app
            review.save()
            messages.success(request, 'Спасибо! Отзыв сохранён.')
            return redirect('cabinet')
    return redirect('cabinet')


def is_admin(user):
    """Допуск к панели только для логина Admin26."""
    return user.is_authenticated and user.username == ADMIN_LOGIN


@user_passes_test(is_admin, login_url='login')
def admin_panel(request):
    """
    Панель администратора со списком всех заявок,
    фильтрами, поиском, сортировкой и постраничной навигацией.
    """
    qs = Application.objects.select_related('user', 'user__profile').all()

    status = request.GET.get('status', '')
    transport = request.GET.get('transport', '')
    search = request.GET.get('q', '').strip()
    order = request.GET.get('order', '-created_at')

    if status:
        qs = qs.filter(status=status)
    if transport:
        qs = qs.filter(transport_type=transport)
    if search:
        qs = qs.filter(
            Q(user__username__icontains=search)
            | Q(user__profile__full_name__icontains=search)
            | Q(user__email__icontains=search)
        )

    allowed_orders = {'created_at', '-created_at', 'status', '-status', 'start_date', '-start_date'}
    if order in allowed_orders:
        qs = qs.order_by(order)

    paginator = Paginator(qs, 8)
    page = paginator.get_page(request.GET.get('page'))

    return render(
        request,
        'main/admin_panel.html',
        {
            'page_obj': page,
            'status': status,
            'transport': transport,
            'search': search,
            'order': order,
            'status_choices': Application.STATUS_CHOICES,
            'transport_choices': Application.TRANSPORT_CHOICES,
        },
    )


@user_passes_test(is_admin, login_url='login')
def change_status(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, f'Статус заявки №{app.pk} обновлён.')
        else:
            messages.error(request, 'Не удалось обновить статус.')
    return redirect(request.META.get('HTTP_REFERER', 'admin_panel'))
