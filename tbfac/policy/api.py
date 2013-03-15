import disqusapi as base

from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry

from collective.disqus.interfaces import IDisqusSettings


class Resource(base.Resource):

    def __getattr__(self, attr):
        if attr in getattr(self, '__dict__'):
            return getattr(self, attr)
        interface = self.interface
        if attr not in interface:
            raise base.InterfaceNotDefined(attr)
        return Resource(self.api, interface[attr], attr, self.tree)

    def __call__(self, **kwargs):
        """Add here forum shortname if it's missing"""
        if not kwargs.get('forum', None) and self.api.forum:
            kwargs['forum'] = self.api.forum
        return super(Resource, self).__call__(**kwargs)

class DisqusAPI(Resource, base.DisqusAPI):
    """Disqus API with Application secret key and forum shortname
    fetched from collective.disqus control panel settings.
    """

    def __init__(self, context, *args, **kw):
        self.context = context
        self.portal = getToolByName(self.context,
            'portal_url').getPortalObject()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IDisqusSettings)
        self.forum = self.settings.forum_short_name

        super(DisqusAPI, self).__init__(*args, **kw)

        # set secret key set in collective.disqus control panel
        key = kw.get('key', None)
        if key is None and self.settings.app_secret_key:
            self.setKey(self.settings.app_secret_key)

        # also set public key
        if self.settings.app_public_key:
            self.setPublicKey(self.settings.app_public_key)
