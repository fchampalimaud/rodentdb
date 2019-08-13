from confapp import conf
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from rodentdb.models import ReporterGene


class RodentReporterGeneForm(ModelFormWidget):

    FIELDSETS = ["name"]

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_WINDOW


class RodentReporterGeneApp(ModelAdminWidget):

    UID = "rodent-reportergenes"
    MODEL = ReporterGene

    TITLE = "Reporter Genes"

    EDITFORM_CLASS = RodentReporterGeneForm

    USE_DETAILS_TO_ADD = False  # required to have form in NEW_TAB
    USE_DETAILS_TO_EDIT = False  # required to have form in NEW_TAB

    LAYOUT_POSITION = conf.ORQUESTRA_HOME
    ORQUESTRA_MENU = "left>RodentApp"
    ORQUESTRA_MENU_ORDER = 1
    ORQUESTRA_MENU_ICON = "cog"

    @classmethod
    def has_permissions(cls, user):
        if user.is_superuser:
            return True
        return False
