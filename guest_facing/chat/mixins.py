from django.shortcuts import redirect


class ChatDataRequiredMixins:
    """
    View mixin that verifies the user has `chat` in `session`.
    If it does not exist, page will be redirected to `channel` page.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('chat', {}):
            return redirect('chat:channel')
        return super().dispatch(request, *args, **kwargs)