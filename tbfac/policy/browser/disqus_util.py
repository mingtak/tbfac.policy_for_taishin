from zope.component import getUtility

from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID

from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView

from collective.disqus.interfaces import IDisqusSettings


class DisqusUtilsView(BrowserView):

    def get_disqus_identifier(self):
        """Returns object UID"""
        uid = IUUID(self.context, None)
        if not uid:
            uid = self.context.UID()
        return uid

    def get_counter_js(self):
        """ Get the js mentioned in
        http://disqus.com/admin/universal/ for counting comments
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IDisqusSettings)

        short_name = settings.forum_short_name
        if short_name:
            result = ("<script type=\"text/javascript\">"
                "var disqus_shortname = '%s';"
                "</script><script type=\"text/javascript\""
                "        src=\"http://%s.disqus.com/count.js\" >"
                "</script>" % (short_name, short_name))

        else:
            result = ""

        return result
