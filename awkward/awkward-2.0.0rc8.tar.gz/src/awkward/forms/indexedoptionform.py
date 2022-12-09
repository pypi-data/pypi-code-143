# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import awkward as ak
from awkward._util import unset
from awkward.forms.form import Form, _parameters_equal


class IndexedOptionForm(Form):
    is_option = True
    is_indexed = True

    def __init__(
        self,
        index,
        content,
        *,
        parameters=None,
        form_key=None,
    ):
        if not isinstance(index, str):
            raise ak._errors.wrap_error(
                TypeError(
                    "{} 'index' must be of type str, not {}".format(
                        type(self).__name__, repr(index)
                    )
                )
            )
        if not isinstance(content, Form):
            raise ak._errors.wrap_error(
                TypeError(
                    "{} all 'contents' must be Form subclasses, not {}".format(
                        type(self).__name__, repr(content)
                    )
                )
            )

        self._index = index
        self._content = content
        self._init(parameters, form_key)

    @property
    def index(self):
        return self._index

    @property
    def content(self):
        return self._content

    def copy(
        self,
        index=unset,
        content=unset,
        *,
        parameters=unset,
        form_key=unset,
    ):
        return IndexedOptionForm(
            self._index if index is unset else index,
            self._content if content is unset else content,
            parameters=self._parameters if parameters is unset else parameters,
            form_key=self._form_key if form_key is unset else form_key,
        )

    @classmethod
    def simplified(
        cls,
        index,
        content,
        *,
        parameters=None,
        form_key=None,
    ):
        is_cat = parameters is not None and parameters.get("__array__") == "categorical"

        if content.is_union and not is_cat:
            return content._union_of_optionarrays(index, parameters)

        elif content.is_indexed or content.is_option:
            return ak.forms.IndexedOptionForm.simplified(
                "i64",
                content.content,
                parameters=ak._util.merge_parameters(content._parameters, parameters),
            )

        else:
            return cls(index, content, parameters=parameters, form_key=form_key)

    def __repr__(self):
        args = [repr(self._index), repr(self._content)] + self._repr_args()
        return "{}({})".format(type(self).__name__, ", ".join(args))

    def _to_dict_part(self, verbose, toplevel):
        return self._to_dict_extra(
            {
                "class": "IndexedOptionArray",
                "index": self._index,
                "content": self._content._to_dict_part(verbose, toplevel=False),
            },
            verbose,
        )

    def _type(self, typestrs):
        if self.parameter("__array__") == "categorical":
            parameters = dict(self._parameters)
            del parameters["__array__"]
            parameters["__categorical__"] = True
        else:
            parameters = self._parameters

        return ak.types.OptionType(
            self._content._type(typestrs),
            parameters=parameters,
            typestr=ak._util.gettypestr(self._parameters, typestrs),
        ).simplify_option_union()

    def __eq__(self, other):
        if isinstance(other, IndexedOptionForm):
            return (
                self._form_key == other._form_key
                and self._index == other._index
                and _parameters_equal(
                    self._parameters, other._parameters, only_array_record=True
                )
                and self._content == other._content
            )
        else:
            return False

    def purelist_parameter(self, key):
        if self._parameters is None or key not in self._parameters:
            return self._content.purelist_parameter(key)
        else:
            return self._parameters[key]

    @property
    def purelist_isregular(self):
        return self._content.purelist_isregular

    @property
    def purelist_depth(self):
        return self._content.purelist_depth

    @property
    def is_identity_like(self):
        return self._content.is_identity_like

    @property
    def minmax_depth(self):
        return self._content.minmax_depth

    @property
    def branch_depth(self):
        return self._content.branch_depth

    @property
    def fields(self):
        return self._content.fields

    @property
    def is_tuple(self):
        return self._content.is_tuple

    @property
    def dimension_optiontype(self):
        return True

    def _columns(self, path, output, list_indicator):
        self._content._columns(path, output, list_indicator)

    def _select_columns(self, index, specifier, matches, output):
        return IndexedOptionForm(
            self._index,
            self._content._select_columns(index, specifier, matches, output),
            parameters=self._parameters,
            form_key=self._form_key,
        )

    def _column_types(self):
        return self._content._column_types()
