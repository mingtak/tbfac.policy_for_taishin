from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import safe_unicode

from collective.addthis.addthis import AddThisViewlet


class AddThisDependencies(AddThisViewlet):

    template = ViewPageTemplateFile('templates/addthis_dependencies.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return self.template()

class AddThisListingItemButtons(AddThisViewlet):

    _macro = u'''
    <div class="addthis_toolbox addthis_default_style" id="socialtools"
         addthis:url="%(url)s"
         addthis:title="%(title)s"
         addthis:description="%(desc)s">
      %(body)s
    </div>
    '''

    template = ViewPageTemplateFile('templates/addthis_listing_item_buttons.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = aq_inner(self.context)
        info = {'body': self.template()}
        info['title'] = safe_unicode(context.Title())
        info['desc'] = safe_unicode(context.Description())
        info['url'] = context.absolute_url()
        return self._macro % info
