from confapp import conf
from pyforms_web.organizers import segment
from pyforms_web.widgets.django import ModelAdminWidget
from rodentdb.models import RodentPermission



class PermissionsListApp(ModelAdminWidget):

    MODEL = RodentPermission
    TITLE = 'Permissions'

    LIST_DISPLAY = ['group', 'viewonly']
    FIELDSETS    = [ ('group', 'viewonly') ]