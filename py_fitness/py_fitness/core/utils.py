from django.http import (Http404, HttpResponseRedirect)
from django.contrib import messages
from django.core.urlresolvers import reverse


class FormValidMixin(object):

    def form_valid(self, form):
        self.object = form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())


class ActionedMessageMixin(object):
    message_prefix = ''
    message_suffix = 'actioned'

    """
        Mixin for success messages on non-class-based views
    """
    def action_message(self, objects):
        object_names = ''

        try:
            if self.message_prefix is '':
                prefix_set = False
            else:
                prefix_set = True
            for obj in objects:
                object_names += obj.__str__() + ", "
                if prefix_set:
                    self.message_prefix += type(obj)._meta.model_name.title() + ", "
            self.message_prefix = self.message_prefix[:len(self.message_prefix) - 2]
            object_names = object_names[:len(object_names) - 2]
        except TypeError:
            object_names += objects.__str__()
            if self.message_prefix is '':
                self.message_prefix += type(objects)._meta.model_name.title()

        return "{0} {1} {2}".format(self.message_prefix, object_names, self.message_suffix).strip()


class SuccessUrlMixin(object):
    kwargs_key = ['slug', 'pk', 'mpk']

    def get_success_url(self):
        new_kwargs = {}
        for key in self.kwargs_key:
            if key in self.kwargs:
                new_kwargs[key] = self.kwargs[key]

        return reverse(self.success_url, kwargs=new_kwargs)


class ArchiveSuccessUrlMixin(object):
    kwargs_key = ['year', 'month', 'day']

    def get_success_url(self):
        new_kwargs = {}
        for key in self.kwargs_key:
            if key in self.kwargs:
                new_kwargs[key] = self.kwargs[key]

        return reverse(self.success_url, kwargs=new_kwargs)


class DeleteMessageMixin(object):
    default_success_message = '%s was deleted'
    success_message = None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.success_message is not None:
            messages.success(self.request, self.success_message)
        else:
            messages.success(self.request, self.default_success_message % self.object.__str__())
        return super(DeleteMessageMixin, self).delete(request, *args, **kwargs)
