from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Exercise, Comment, Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import LoginForm, RegisterForm, CommentForm, ExerciseForm, EditAccountForm, EditProfileForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages


# Create your views here.


# -----------------------------------------------------------------------------------------------------------------------
# функция для главной страницы

# def index(request):
#     exercises = Exercise.objects.all()  # Получаем все категории из БД
#
#     context = {
#         'title': 'Главная страница',
#         'exercises': exercises
#     }
#
#     return render(request, 'gumfuel_page/index.html', context)

class ExerciseListView(ListView):
    model = Exercise
    context_object_name = 'exercises'
    template_name = 'gumfuel_page/index.html'  # для какой страницы делаем вьюшку
    extra_context = {
        'title': 'Главная страница'
    }


# ------------------------------------------------------------------------------------------------------------------------
#  функция для получения упражнения по id категории

# def category_view(request, pk):
#     exercises = Exercise.objects.filter(category_id=pk)  # получаем упражнения по id категории
#     category = Exercise.objects.get(pk=pk)  # получили саму категорию
#
#     context = {
#         'title': f'Категория: {category.title}',
#         'exercises': exercises
#     }
#
#     return render(request, 'gumfuel_page/index.html', context)


class ExerciseListByCategory(ExerciseListView):
    # Метод клоторый вернет фильмы по id категории
    def get_queryset(self):
        exercises = Exercise.objects.filter(category_id=self.kwargs['pk'])
        return exercises

    # Метод  при помощи которого мыможем дополнительно что то отправлять на страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])  # категория по id
        context['title'] = f'Сплит:  {category.title}'
        return context


# -----------------------------------------------------------------------------------------------------------------------

# Функция для страницы упражнения
# def exercise_view(request, pk):
#     exercise = Exercise.objects.get(pk=pk)
#     context = {
#         'title': f'{exercise.category}: {exercise.title}',
#         'exercise': exercise
#     }
#
#     return render(request, 'gumfuel_page/gumfuel_detail.html', context)

class ExerciseDetail(DeleteView):
    model = Exercise
    context_object_name = 'exercise'
    template_name = 'gumfuel_page/gumfuel_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        exercise = Exercise.objects.get(pk=self.kwargs['pk'])  # упражнение по id
        context['title'] = f'{exercise.title}'
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['comments'] = Comment.objects.filter(exercise=exercise)

        return context


# ----------------------------------------------------------------------------------------------------------------------
# функция для входа в аккаунт
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # проверяет пользователя по логину и паролю
            if user:
                login(request, user)
                return redirect('index')
            else:
                return redirect('login')
    else:
        form = LoginForm()

    context = {
        'title': 'Вход в аккаунт',
        'form': form
    }

    return render(request, 'gumfuel_page/login.html', context)


# функция для выхода с аккаунта

def user_logout(request):
    logout(request)
    return redirect('index')


# -----------------------------------------------------------------------------------------------------------------------


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(BodyPart, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Exercise.Status.PUBLISHED)
#
#     context = {
#         'title': {tag.tag},
#         'posts': posts
#     }
#
#     return render(request, 'gumfuel_page/index.html', context)


# -----------------------------------------------------------------------------------------------------------------

# Регистрация пользователя

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect('login')
        else:
            for field in form.errors:
                return redirect('register')

    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }

    return render(request, 'gumfuel_page/register.html', context)


# Поиск ----------------------------------------------------------------------------------------------------------------

class SearchEx(ExerciseListView):
    def get_queryset(self):
        word = self.request.GET.get('q')  # из запроса адресной сторки будем получить слово
        exercises = Exercise.objects.filter(title__icontains=word.lower()) or Exercise.objects.filter(
            title__icontains=word.capitalize())
        return exercises


# для сохранения комментариев ------------------------------------------------------------------------------------------

def save_comments(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.exercise = Exercise.objects.get(pk=pk)
        comment.save()
        return redirect('gumfuel_detail', pk)


# Добавление постов-----------------------------------------------------------------------------------------------------

# def add_exercise_view(request):
#     if request.method == 'POST':
#         form = ExerciseForm(request.POST, request.FILES)
#         if form.is_valid():
#             exercise = Exercise.objects.create(**form.cleaned_data)
#             exercise.save()
#             return redirect('gumfuel_detail', exercise.pk)
#     else:
#         form = ExerciseForm()
#
#     context = {
#         'title': 'Добавить фильм',
#         'form': form
#     }
#
#     return render(request, 'gumfuel_page/add_exercise.html', context)

class NewExercise(LoginRequiredMixin, CreateView):
    form_class = ExerciseForm
    template_name = 'gumfuel_page/add_exercise.html'
    extra_context = {
        'title': 'Добавить фильм'
    }

    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        #exercises = Exercise.objects.get(pk=self.kwargs['pk'])
        if not self.request.user.is_authenticated:
            return redirect('login')

        return super(NewExercise, self).get(request, *args, **kwargs)

    # Метод добавления автора
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Изменение-------------------------------------------------------------------------------------------------------------

class ExerciseUpdate(UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = 'gumfuel_page/add_exercise.html'
    extra_context = {
        'title': 'Изменение данных поста'
    }

    # проверка на авторизацию
    def get(self, request, *args, **kwargs):
        exercises = Exercise.objects.get(pk=self.kwargs['pk'])
        if not self.request.user.is_authenticated:
            return redirect('gumfuel_detail', exercises.pk)
        else:
            if self.request.user != exercises.author:
                return redirect('gumfuel_detail', exercises.pk)

        return super(ExerciseUpdate, self).get(request, *args, **kwargs)


# Удаление--------------------------------------------------------------------------------------------------------------

class ExerciseDelete(DeleteView):
    model = Exercise
    context_object_name = 'exercise'
    success_url = reverse_lazy('index')
    template_name = 'gumfuel_page/exercise_confirm_delete.html'

    # проверка на авторизацию

    def get(self, request, *args, **kwargs):
        exercises = Exercise.objects.get(pk=self.kwargs['pk'])
        if not self.request.user.is_authenticated:
            return redirect('gumfuel_detail', exercises.pk)
        else:
            if self.request.user != exercises.author:
                return redirect('gumfuel_detail', exercises.pk)

        return super(ExerciseDelete, self).get(request, *args, **kwargs)


# Страница профиля

def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    exercises = Exercise.objects.filter(author_id=pk)  # все упражнения пользователя

    context = {
        'title': f'Профиль: {profile.user.username}',
        'profile': profile,
        'exercises': exercises,
        'edit_account_form': EditAccountForm(instance=request.user if request.user.is_authenticated else None),
        'edit_profile_form': EditProfileForm(instance=request.user.profile if request.user.is_authenticated else None)
    }

    return render(request, 'gumfuel_page/profile.html', context)


# изменение данных акка

def edit_account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditAccountForm(request.POST, instance=request.user)
            if form.is_valid():
                data = form.cleaned_data
                user = User.objects.get(id=request.user.id)
                if user.check_password(data['old_password']):
                    if data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Пароль изменен')
                        return redirect('profile', user.pk)
                    else:
                        for field in form.errors:
                            messages.error(request, form.errors[field].as_text())

                else:
                    for field in form.errors:
                        messages.error(request, form.errors[field].as_text())

                form.save()
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())

            return redirect('profile', request.user.pk)
    else:
        return redirect('login')


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.pk)  # Замените 'profile' на имя вашей страницы профиля
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})
















