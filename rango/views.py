from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from rango.bing_search import run_query
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page


def index(request):
    # category_list = Category.objects.all()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits', 1)

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')

    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')

        if (datetime.now() - last_visit_time).seconds > 0:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits

    response = render(request, 'rango/index.html', context_dict)
    return response


def about(request):
    context_dict = {}
    visits = request.session.get('visits', 1)

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')

    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')

        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits

    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        category = get_object_or_404(Category, slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)



@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            # cat = form.save(commit=True)
            # print cat, cat.slug
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form  = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # print 'ok...page before category.html', page
                # Problem: didn't redirect to category.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}
    # print 'ok...page before add_page.html'
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
        {'user_form': user_form,
         'profile_form': profile_form,
         'registered': registered})


def register_profile(request):
    registered = False
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            # as the same time..??
            user = User.objects.order_by('-pk')[0]

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

            return HttpResponseRedirect(reverse('rango:index'))
        else:
            print profile_form.errors
    else:
        profile_form = UserProfileForm()

    return render(request, 'rango/profile_registration.html',
        {'profile_form': profile_form,
         'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse('Your Rango account is disabled.')
        else:
            print 'Invalid login details: {0}, {1}'.format(username, password)
            return HttpResponse('Invalid login details supplied.')
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


def search(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render(request, 'rango/search.html',
        {'result_list': result_list})


def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            # Security issue? not filtering...
            page_id = request.GET['page_id']
            if not page_id.isdigit():
                raise 'You always input digits.'

            try:
                page = Page.objects.get(pk=page_id)
                page.views += 1
                page.save()
            except:
                pass
            else:
                return HttpResponseRedirect(page.url)
    return HttpResponseRedirect(reverse('rango:index'))



@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    if cat_id:
        cat = get_object_or_404(Category, id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]

    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        cat_list = get_category_list(8, starts_with)
        if starts_with == '':
            cat_list = Category.objects.all()

    return render(request, 'rango/category_list.html',
        {'cat_list': cat_list})


def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}

    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            try:
                category = get_object_or_404(Category, pk=int(cat_id))
                p = Page.objects.get_or_create(category=category,
                                               title=title,
                                               url=url)
                pages = Page.objects.filter(category=category).order_by('-views')
                context_dict['pages'] = pages
            except Exception as e:
                print(e)

    return render(request, 'rango/page_list.html', context_dict)


# def test_cookie(request):
#     if 'id' in request.COOKIES:
#         cookie_id = request.COOKIES['id']
#         return HttpResponse('Got cookie with id=%s' % cookie_id)
#     else:
#         resp = HttpResponse('No id cookie! Sending cookie to client')
#         resp.set_cookie('id', 'some_value_99')
#         return resp
#
#
# def test_count_session(request):
#     if 'count' in request.session:
#         request.session['count'] += 1
#         return HttpResponse('new counts=%s' % request.session['count'])
#     else:
#         request.session['count'] = 1
#         return HttpResponse('No count in session. Setting to 1')
#
#
# def test_user(request):
#     user_str = str(request.user)
#     if request.user.is_authenticated():
#         return HttpResponse('%s is logged in' % user_str)
#     else:
#         return HttpResponse('%s is not logged in' % user_str)