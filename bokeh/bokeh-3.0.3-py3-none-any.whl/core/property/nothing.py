#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2022, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
""" """

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from typing import Any, NoReturn

# Bokeh imports
from .bases import Property, Undefined

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    "Nothing",
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class Nothing(Property[NoReturn]):
    """ The bottom type of bokeh's type system. It doesn't accept any values. """

    def __init__(self, *, help: str | None = None) -> None:
        super().__init__(default=Undefined, help=help)

    def validate(self, value: Any, detail: bool = True) -> None:
        raise ValueError("no value is allowed")


#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
