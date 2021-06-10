import datetime
from datetime import datetime as dt
from django.conf                import settings
from django.shortcuts           import render
from django.utils               import timezone, translation
from django.views.generic       import *
from django.utils.translation   import gettext, gettext_lazy as _
from guest_facing.core          import gateways
from guest_facing.core.views    import IndexView
from guest_facing.core.mixins   import RequestFormKwargsMixin, JSONResponseMixin
from .forms                     import ChatChannelForm, ChatMessageForm
from .mixins                    import ChatDataRequiredMixins


class IndexView(IndexView):
    pattern_name = 'chat:channel'


class ChatChannelView(RequestFormKwargsMixin, FormView):
    template_name   = 'chat/channel.html'
    form_class      = ChatChannelForm
    success_url     = '/chat/message'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = {}
        data['email'] = self.request.GET.get('email')
        data['name'] = self.request.GET.get('name')
        data['property_id'] = self.request.GET.get('property') or self.request.GET.get('property_id')
        kwargs['data'] = data
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if 'lang' in request.GET: self.request.session[translation.LANGUAGE_SESSION_KEY] = self.request.GET.get('lang', 'en')
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ChatMessageView(ChatDataRequiredMixins, JSONResponseMixin, RequestFormKwargsMixin, FormView):
    template_name   = 'chat/message.html'
    form_class      = ChatMessageForm

    system_messages = {
        'welcome': _('Welcome to Hotel Template! Thank you for contacting us through our app. How may we assist you today?'),
        'out_time': _('Thank you for using our messaging. Please expect delay and a slower response to your message. Should you require any assistance urgently, please approach Front Desk Officer.')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pubnub_config = {}
        pubnub_config['subscribe_key'] = settings.CHAT_SUB_KEY
        pubnub_config['channel'] = self.request.session.get('chat', {}).get('channel', '')
        pubnub_config['uuid'] = self.request.session.get('chat', {}).get('uuid', '')
        context['pubnub_config'] = pubnub_config
        context['system_messages'] = self.system_messages
        # check for auto reply system message
        context ['system_message_out_time'] = False
        config = gateways.amp_endpoint('get', '/configVariables', self.request.session.get('chat', {}).get('property_id', '')) or {}
        start_time = config.get('data', {}).get('autoReplyStartTime_24h', settings.CHAT_AUTO_START_TIME)
        end_time = config.get('data', {}).get('autoReplyEndTime_24h', settings.CHAT_AUTO_END_TIME)
        if start_time <= end_time:
            start_date = datetime.date.today()
            end_date = datetime.date.today()
        else:
            start_date = datetime.date.today()
            end_date = datetime.date.today() + datetime.timedelta(days=1)
        start_datetime = dt.strptime(start_date.strftime('%Y-%m-%d') +' '+ start_time, '%Y-%m-%d %H:%M')
        end_datetime = dt.strptime(end_date.strftime('%Y-%m-%d') +' '+ end_time, '%Y-%m-%d %H:%M')
        start_datetime = timezone.make_aware(start_datetime)
        end_datetime = timezone.make_aware(end_datetime)
        if start_datetime <= timezone.localtime() <= end_datetime:
            context ['system_message_out_time'] = True
        return context

    def form_valid(self, form):
        form.save()
        self.json_status = 'success'
        return self.render_to_json_response(self.get_context_data())

    def form_invalid(self, form):
        self.json_status = 'error'
        self.json_errors = form.errors
        return self.render_to_json_response(self.get_context_data())
