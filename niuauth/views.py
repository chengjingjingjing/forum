from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View

from forum.utils import get_pagination


@method_decorator(login_required, name = 'dispatch')
class UserProfileView(TemplateView):
    template_name = "niuauth/home.html"

    def get_context_data(self, **kwargs):
        data = super(UserProfileView, self).get_context_data(**kwargs)

        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, username = user_id)
        user_reply = user.replies.order_by('-date_created').all()

        paginator = Paginator(user_reply, 10)
        page = self.request.GET.get('page')
        try:
            replies = paginator.page(page)
        except PageNotAnInteger:
            replies = paginator.page(1)
        except EmptyPage:
            replies = paginator.page(paginator.num_pages)

        page_list = get_pagination(replies.number, paginator.num_pages, 2)

        data['see_user'] = user
        data['replies'] = replies
        data["page_list"] = page_list

        return data


user_profile = UserProfileView.as_view()


@method_decorator(login_required, name = 'dispatch')
class UserTopicView(TemplateView):
    template_name = "niuauth/user_topic.html"

    def get_context_data(self, **kwargs):
        data = super(UserTopicView, self).get_context_data(**kwargs)

        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, username = user_id)
        user_topics = user.topics.order_by('-date_created').all()

        paginator = Paginator(user_topics, 10)
        page = self.request.GET.get('page')
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)

        page_list = get_pagination(topics.number, paginator.num_pages, 2)

        data['see_user'] = user
        data['topics'] = topics
        data["page_list"] = page_list

        return data


user_topic = UserTopicView.as_view()


@method_decorator(login_required, name = 'dispatch')
class NotificationView(TemplateView):
    template_name = "niuauth/notification.html"

    def get_context_data(self, **kwargs):
        data = super(NotificationView, self).get_context_data(**kwargs)

        notifications = self.request.user.notifications.all()

        paginator = Paginator(notifications, 10)
        page = self.request.GET.get('page')
        try:
            noti_list = paginator.page(page)
        except PageNotAnInteger:
            noti_list = paginator.page(1)
        except EmptyPage:
            noti_list = paginator.page(paginator.num_pages)

        page_list = get_pagination(noti_list.number, paginator.num_pages, 2)

        data["noti_list"] = noti_list
        data["page_list"] = page_list

        profile = self.request.user.profile
        profile.has_notification = False
        profile.save()

        return data


notification_view = NotificationView.as_view()


@method_decorator(login_required, name = 'dispatch')
class ClearNotificationView(View):
    def get(self, request, *args, **kwargs):
        self.request.user.notifications.all().delete()

        return HttpResponseRedirect(reverse('notification_view'))


clear_notification_view = ClearNotificationView.as_view()
