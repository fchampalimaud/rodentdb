from .rodent_queryset import RodentQuerySet
from .rodent_permission import RodentPermission
from .rodent_base import RodentBase

class Rodent(RodentBase):

    objects = RodentQuerySet.as_manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.lab is not None:
            RodentPermission.objects.get_or_create(rodent=self, group=self.lab, viewonly=False)
