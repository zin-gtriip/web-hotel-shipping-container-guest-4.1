from django                                         import forms
from django.conf                                    import settings
from django.utils.translation                       import gettext, gettext_lazy as _
from pubnub.pnconfiguration                         import PNConfiguration
from pubnub.pubnub                                  import PubNub
from pubnub.models.consumer.objects_v2.memberships  import PNChannelMembership
from pubnub.endpoints.objects_v2.objects_endpoint   import ChannelIncludeEndpoint
from .                                              import utils


class ChatChannelForm(forms.Form):
    email = forms.CharField(label=_('Email'))
    name = forms.CharField(label=_('Name'))
    property_id = forms.CharField(label=_('Property'))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def clean(self):
        property_id = self.cleaned_data.get('property_id')
        if property_id:
            prop_data = next((prop for prop in settings.GUEST_ENDPOINT or [] if prop.get('id', '') == property_id), None)
            if not prop_data:
                self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([_('No property selected.')])

    def save(self):
        email = utils.replace_illegal_char(self.cleaned_data.get('email', ''))
        name = self.cleaned_data.get('name')
        property_id = self.cleaned_data.get('property_id')
        channel_group = 'guest_%s' % property_id
        channel = '%(name)s-%(email)s' % {'name': name, 'email': email}
        # assign pubnub channel to channel group
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = settings.CHAT_SUB_KEY
        pnconfig.publish_key = settings.CHAT_PUB_KEY
        pnconfig.uuid = name
        pubnub = PubNub(pnconfig)
        pubnub.add_channel_to_channel_group().channels([channel]).channel_group(channel_group).sync()
        # check for membership
        response = pubnub.get_memberships().include_custom(True).include_channel(ChannelIncludeEndpoint.CHANNEL_WITH_CUSTOM).uuid(settings.CHAT_UUID).sync()
        if response.status.status_code == 200:
            memberships = response.result.data
            membership = next((data for data in memberships if data.get('channel', {}).get('id', '') == channel), {})
            token = membership.get('custom', {}).get('lastReadTimetoken')
            if not membership or not token: # set token
                new_token = {'lastReadTimetoken': 946684800000} # 2000-01-01 00:00:00, 0 is not working
                pubnub.set_memberships().uuid(settings.CHAT_UUID).channel_memberships([PNChannelMembership.channel_with_custom(channel, new_token)]).include_custom(True).sync()
        # assign to request
        self.request.session['chat'] = {}
        self.request.session['chat']['channel_group'] = channel_group
        self.request.session['chat']['channel'] = channel
        self.request.session['chat']['uuid'] = name


class ChatMessageForm(forms.Form):
    message = forms.CharField(label=_('Message'))

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.label_suffix = ''

    def save(self):
        channel = self.request.session.get('chat', {}).get('channel')
        message = self.cleaned_data.get('message')
        # initiate pubnub
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = settings.CHAT_SUB_KEY
        pnconfig.publish_key = settings.CHAT_PUB_KEY
        pnconfig.uuid = self.request.session.get('chat', {}).get('uuid')
        pubnub = PubNub(pnconfig)
        # send message
        pubnub.publish().channel(channel).message(message).sync()
        # check for membership
        response = pubnub.get_memberships().include_custom(True).include_channel(ChannelIncludeEndpoint.CHANNEL_WITH_CUSTOM).uuid(settings.CHAT_UUID).sync()
        if response.status.status_code == 200:
            memberships = response.result.data
            membership = next((data for data in memberships if data.get('channel', {}).get('id', '') == channel), {})
            token = membership.get('custom', {}).get('lastReadTimetoken')
            if not membership or not token: # re-set token, FIXME set membership for first time is not reflected therefore re-set
                new_token = {'lastReadTimetoken': 946684800000} # 2000-01-01 00:00:00, 0 is not working
                pubnub.set_memberships().uuid(settings.CHAT_UUID).channel_memberships([PNChannelMembership.channel_with_custom(channel, new_token)]).include_custom(True).sync()
