from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm,UserForm,UserProfileInfoForm,ContactForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic.edit import FormMixin
from django.views.generic import (TemplateView,ListView,
                                DetailView,CreateView,
                                UpdateView,DeleteView,
                                )

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class ContactView(TemplateView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        form = ContactForm(self.request.POST or None)
        context = super(ContactView, self).get_context_data(**kwargs)
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            contact = form.save(commit=False)
            contact.post = post
            contact.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(ContactView, self).form_valid(form)

class PostListView(ListView):
    paginate_by = 3
    model = Post

    def get_queryset(self):
        return Post.objects.all().filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(FormMixin,DetailView):
    model = Post
    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def get_initial(self):
        return {"post": self.get_object() }

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def post(self, request, pk, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        post = get_object_or_404(Post,pk=pk)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)
 
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Post
    form_class = PostForm
    redirect_field_name = 'blog/post_detail.html'
    
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


##############
############


@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)


#ACCOUNT 
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_list'))

def register(request):
    registered = False

    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data= request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'registration/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})
            
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('post_list'))
            else:
                return HttpResponse("Account Not Active!")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid username and password!")
    else:
        return render(request,'registration/login.html',{})
