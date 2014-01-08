from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from tbfac.policy import MessageFactory as _


class IInfoSearchPortlet(IPortletDataProvider):
    """A portlet searching for Info items by locations.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """This portlet assignment is what is actually managed through
       the portlets UI and associated with columns.
    """
    implements(IInfoSearchPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u''):
    #    self.some_field = some_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet
           in the "manage portlets" screen.
        """
        return _(u"Info Search")


class Renderer(base.Renderer):
    """This portlet renderer is registered in configure.zcml.
       The referenced page template is rendered, and the implicit
       variable 'view' will refer to an instance of this class.
       Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('infosearch.pt')


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.NullAddForm):
    """This portlet add form is registered in configure.zcml.
       The form_fields variable tells zope.formlib which fields to display.
       The create() method actually constructs the assignment
       that is being added.
    """
    def create(self):
        return Assignment()

