from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForms
from .models import Album


class IndexView(generic.ListView):
  template_name="music/index.html"
  def get_queryset(self):
    return Album.objects.all()


class DetailView(generic.DetailView):
  model = Album
  template_name = "music/detail.html"


class AlbumCreate(CreateView):
  model = Album
  fields = ['artist','album_title','genre','album_logo']

class AlbumUpdate(UpdateView):
  model = Album
  fields = ['artist','album_title','genre','album_logo']

class AlbumDelete(DeleteView):
  model = Album
  success_url=reverse_lazy('index')

class UserFormView(View):
  form_class= UserForms
  template_name = 'music/Registration_form.html'

  def get(self,request):
    form = self.form_class(None)
    return render(request,self.template_name,{'form':form})

  def post(self,request):
    form = self.form_class(request.POST)

    if form.is_valid():
      user = form.save(commit=False)

      #cleaned (NORMALIZED) data
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user.set_password(password)
      user.save()

      #return user object if credentials are correct
      user = authenticate(username=username , password=password)


      if user is not None:

        if user.is_active:
          login(request , user)
          return redirect('index')

    return render(request, self.template_name, {'form': form})