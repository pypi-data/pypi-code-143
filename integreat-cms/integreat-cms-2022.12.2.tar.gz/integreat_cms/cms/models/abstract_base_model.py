import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from debug_toolbar.panels.sql.tracking import SQLQueryTriggered


logger = logging.getLogger(__name__)


class AbstractBaseModel(models.Model):
    """
    Abstract base class for all models
    """

    @classmethod
    def get_model_name_plural(cls):
        """
        Get the plural representation of this model name

        :returns: The plural model name
        :rtype: str
        """
        model_name = cls._meta.model_name
        # Build correct plural of models ending with "y"
        if model_name.endswith("y"):
            model_name_plural = f"{model_name[:-1]}ies"
        else:
            model_name_plural = f"{model_name}s"
        return model_name_plural

    def get_repr(self):
        """
        Returns the canonical string representation of the content object

        To be implemented in the inheriting model
        """
        raise NotImplementedError

    def __repr__(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return
        ``<AbstractContentModel: AbstractContentModel object (id)>``.
        It tries to get the representation of the inheriting model, but falls back to a minimal representation in case
        the fields used in the ``get_repr()`` method do not exist yet (e.g. because other errors occurred)

        :return: The canonical string representation of the content object
        :rtype: str
        """
        try:
            return self.get_repr()
        # pylint: disable=broad-except
        except Exception as e:
            fallback_repr = f"<{type(self).__name__} (id: {self.id})>"
            # Skip logging if it's either a triggered SQL query or the id of the object is None and related objects do not exist yet
            if not (
                isinstance(e, SQLQueryTriggered)
                or (isinstance(e, ObjectDoesNotExist) and not self.id)
            ):
                logger.debug(
                    "repr() for object %s failed because of %s: %s "
                    "(If you think this is no problem, please exclude this exception in the repr() method of the AbstractBaseModel.)",
                    fallback_repr,
                    type(e).__name__,
                    e,
                    exc_info=e,
                )
            return fallback_repr

    class Meta:
        #: This model is an abstract base class
        abstract = True
