
# Autogenerated by mlir-tblgen; don't manually edit.

from ._ods_common import _cext as _ods_cext
from ._ods_common import extend_opview_class as _ods_extend_opview_class, segmented_accessor as _ods_segmented_accessor, equally_sized_accessor as _ods_equally_sized_accessor, get_default_loc_context as _ods_get_default_loc_context, get_op_result_or_value as _get_op_result_or_value, get_op_results_or_values as _get_op_results_or_values
_ods_ir = _ods_cext.ir

try:
  from . import _sparse_tensor_ops_ext as _ods_ext_module
except ImportError:
  _ods_ext_module = None

import builtins


@_ods_cext.register_dialect
class _Dialect(_ods_ir.Dialect):
  DIALECT_NAMESPACE = "sparse_tensor"
  pass


@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class BinaryOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.binary"

  _ODS_REGIONS = (3, True)

  def __init__(self, output, x, y, *, left_identity=None, right_identity=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(x))
    operands.append(_get_op_result_or_value(y))
    if bool(left_identity): attributes["left_identity"] = _ods_ir.UnitAttr.get(
      _ods_get_default_loc_context(loc))
    if bool(right_identity): attributes["right_identity"] = _ods_ir.UnitAttr.get(
      _ods_get_default_loc_context(loc))
    results.append(output)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def x(self):
    return self.operation.operands[0]

  @builtins.property
  def y(self):
    return self.operation.operands[1]

  @builtins.property
  def left_identity(self):
    return "left_identity" in self.operation.attributes

  @left_identity.setter
  def left_identity(self, value):
    if bool(value):
      self.operation.attributes["left_identity"] = _ods_ir.UnitAttr.get()
    elif "left_identity" in self.operation.attributes:
      del self.operation.attributes["left_identity"]

  @left_identity.deleter
  def left_identity(self):
    del self.operation.attributes["left_identity"]

  @builtins.property
  def right_identity(self):
    return "right_identity" in self.operation.attributes

  @right_identity.setter
  def right_identity(self, value):
    if bool(value):
      self.operation.attributes["right_identity"] = _ods_ir.UnitAttr.get()
    elif "right_identity" in self.operation.attributes:
      del self.operation.attributes["right_identity"]

  @right_identity.deleter
  def right_identity(self):
    del self.operation.attributes["right_identity"]

  @builtins.property
  def output(self):
    return self.operation.results[0]

  @builtins.property
  def overlapRegion(self):
    return self.regions[0]

  @builtins.property
  def leftRegion(self):
    return self.regions[1]

  @builtins.property
  def rightRegion(self):
    return self.regions[2]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class CompressOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.compress"

  _ODS_REGIONS = (0, True)

  def __init__(self, values, filled, added, count, tensor, indices, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(values))
    operands.append(_get_op_result_or_value(filled))
    operands.append(_get_op_result_or_value(added))
    operands.append(_get_op_result_or_value(count))
    operands.append(_get_op_result_or_value(tensor))
    operands.extend(_get_op_results_or_values(indices))
    _ods_context = _ods_get_default_loc_context(loc)
    results = _ods_ir.InferTypeOpInterface(CompressOp).inferReturnTypes(
        operands=operands,
        attributes=_ods_ir.DictAttr.get(attributes, context=_ods_context),
        context=_ods_context,
        loc=loc)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def values(self):
    return self.operation.operands[0]

  @builtins.property
  def filled(self):
    return self.operation.operands[1]

  @builtins.property
  def added(self):
    return self.operation.operands[2]

  @builtins.property
  def count(self):
    return self.operation.operands[3]

  @builtins.property
  def tensor(self):
    return self.operation.operands[4]

  @builtins.property
  def indices(self):
    _ods_variadic_group_length = len(self.operation.operands) - 6 + 1
    return self.operation.operands[5:5 + _ods_variadic_group_length]

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ConcatenateOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.concatenate"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, inputs, dimension, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.extend(_get_op_results_or_values(inputs))
    attributes["dimension"] = dimension
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def inputs(self):
    _ods_variadic_group_length = len(self.operation.operands) - 1 + 1
    return self.operation.operands[0:0 + _ods_variadic_group_length]

  @builtins.property
  def dimension(self):
    return _ods_ir.IntegerAttr(self.operation.attributes["dimension"])

  @dimension.setter
  def dimension(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["dimension"] = value

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ConvertOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.convert"

  _ODS_REGIONS = (0, True)

  def __init__(self, dest, source, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(source))
    results.append(dest)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def source(self):
    return self.operation.operands[0]

  @builtins.property
  def dest(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ExpandOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.expand"

  _ODS_REGIONS = (0, True)

  def __init__(self, values, filled, added, count, tensor, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(tensor))
    results.append(values)
    results.append(filled)
    results.append(added)
    results.append(count)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def tensor(self):
    return self.operation.operands[0]

  @builtins.property
  def values(self):
    return self.operation.results[0]

  @builtins.property
  def filled(self):
    return self.operation.results[1]

  @builtins.property
  def added(self):
    return self.operation.results[2]

  @builtins.property
  def count(self):
    return self.operation.results[3]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ForeachOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.foreach"

  _ODS_REGIONS = (1, True)

  def __init__(self, results_, tensor, initArgs, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(tensor))
    operands.extend(_get_op_results_or_values(initArgs))
    results.extend(results_)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def tensor(self):
    return self.operation.operands[0]

  @builtins.property
  def initArgs(self):
    _ods_variadic_group_length = len(self.operation.operands) - 2 + 1
    return self.operation.operands[1:1 + _ods_variadic_group_length]

  @builtins.property
  def results_(self):
    _ods_variadic_group_length = len(self.operation.results) - 1 + 1
    return self.operation.results[0:0 + _ods_variadic_group_length]

  @builtins.property
  def region(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class InsertOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.insert"

  _ODS_REGIONS = (0, True)

  def __init__(self, value, tensor, indices, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(value))
    operands.append(_get_op_result_or_value(tensor))
    operands.extend(_get_op_results_or_values(indices))
    _ods_context = _ods_get_default_loc_context(loc)
    results = _ods_ir.InferTypeOpInterface(InsertOp).inferReturnTypes(
        operands=operands,
        attributes=_ods_ir.DictAttr.get(attributes, context=_ods_context),
        context=_ods_context,
        loc=loc)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def value(self):
    return self.operation.operands[0]

  @builtins.property
  def tensor(self):
    return self.operation.operands[1]

  @builtins.property
  def indices(self):
    _ods_variadic_group_length = len(self.operation.operands) - 3 + 1
    return self.operation.operands[2:2 + _ods_variadic_group_length]

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class LoadOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.load"

  _ODS_REGIONS = (0, True)

  def __init__(self, tensor, *, hasInserts=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(tensor))
    if bool(hasInserts): attributes["hasInserts"] = _ods_ir.UnitAttr.get(
      _ods_get_default_loc_context(loc))
    results.extend([operands[0].type] * 1)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def tensor(self):
    return self.operation.operands[0]

  @builtins.property
  def hasInserts(self):
    return "hasInserts" in self.operation.attributes

  @hasInserts.setter
  def hasInserts(self, value):
    if bool(value):
      self.operation.attributes["hasInserts"] = _ods_ir.UnitAttr.get()
    elif "hasInserts" in self.operation.attributes:
      del self.operation.attributes["hasInserts"]

  @hasInserts.deleter
  def hasInserts(self):
    del self.operation.attributes["hasInserts"]

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class NewOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.new"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, source, *, expandSymmetry=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(source))
    if bool(expandSymmetry): attributes["expandSymmetry"] = _ods_ir.UnitAttr.get(
      _ods_get_default_loc_context(loc))
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def source(self):
    return self.operation.operands[0]

  @builtins.property
  def expandSymmetry(self):
    return "expandSymmetry" in self.operation.attributes

  @expandSymmetry.setter
  def expandSymmetry(self, value):
    if bool(value):
      self.operation.attributes["expandSymmetry"] = _ods_ir.UnitAttr.get()
    elif "expandSymmetry" in self.operation.attributes:
      del self.operation.attributes["expandSymmetry"]

  @expandSymmetry.deleter
  def expandSymmetry(self):
    del self.operation.attributes["expandSymmetry"]

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class NumberOfEntriesOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.number_of_entries"

  _ODS_REGIONS = (0, True)

  def __init__(self, tensor, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(tensor))
    _ods_context = _ods_get_default_loc_context(loc)
    results = _ods_ir.InferTypeOpInterface(NumberOfEntriesOp).inferReturnTypes(
        operands=operands,
        attributes=_ods_ir.DictAttr.get(attributes, context=_ods_context),
        context=_ods_context,
        loc=loc)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def tensor(self):
    return self.operation.operands[0]

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class OutOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.out"

  _ODS_REGIONS = (0, True)

  def __init__(self, tensor, dest, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(tensor))
    operands.append(_get_op_result_or_value(dest))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def tensor(self):
    return self.operation.operands[0]

  @builtins.property
  def dest(self):
    return self.operation.operands[1]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class PushBackOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.push_back"

  _ODS_REGIONS = (0, True)

  def __init__(self, bufferSizes, inBuffer, value, idx, *, n=None, inbounds=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(bufferSizes))
    operands.append(_get_op_result_or_value(inBuffer))
    operands.append(_get_op_result_or_value(value))
    if n is not None: operands.append(_get_op_result_or_value(n))
    attributes["idx"] = idx
    if bool(inbounds): attributes["inbounds"] = _ods_ir.UnitAttr.get(
      _ods_get_default_loc_context(loc))
    _ods_context = _ods_get_default_loc_context(loc)
    results = _ods_ir.InferTypeOpInterface(PushBackOp).inferReturnTypes(
        operands=operands,
        attributes=_ods_ir.DictAttr.get(attributes, context=_ods_context),
        context=_ods_context,
        loc=loc)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def bufferSizes(self):
    return self.operation.operands[0]

  @builtins.property
  def inBuffer(self):
    return self.operation.operands[1]

  @builtins.property
  def value(self):
    return self.operation.operands[2]

  @builtins.property
  def n(self):
    return None if len(self.operation.operands) < 4 else self.operation.operands[3]

  @builtins.property
  def idx(self):
    return _ods_ir.IntegerAttr(self.operation.attributes["idx"])

  @idx.setter
  def idx(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["idx"] = value

  @builtins.property
  def inbounds(self):
    return "inbounds" in self.operation.attributes

  @inbounds.setter
  def inbounds(self, value):
    if bool(value):
      self.operation.attributes["inbounds"] = _ods_ir.UnitAttr.get()
    elif "inbounds" in self.operation.attributes:
      del self.operation.attributes["inbounds"]

  @inbounds.deleter
  def inbounds(self):
    del self.operation.attributes["inbounds"]

  @builtins.property
  def outBuffer(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ReduceOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.reduce"

  _ODS_REGIONS = (1, True)

  def __init__(self, x, y, identity, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(x))
    operands.append(_get_op_result_or_value(y))
    operands.append(_get_op_result_or_value(identity))
    results.extend([operands[0].type] * 1)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def x(self):
    return self.operation.operands[0]

  @builtins.property
  def y(self):
    return self.operation.operands[1]

  @builtins.property
  def identity(self):
    return self.operation.operands[2]

  @builtins.property
  def output(self):
    return self.operation.results[0]

  @builtins.property
  def region(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class SelectOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.select"

  _ODS_REGIONS = (1, True)

  def __init__(self, x, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(x))
    results.extend([operands[0].type] * 1)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def x(self):
    return self.operation.operands[0]

  @builtins.property
  def output(self):
    return self.operation.results[0]

  @builtins.property
  def region(self):
    return self.regions[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class SortCooOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.sort_coo"

  _ODS_REGIONS = (0, True)

  def __init__(self, n, xy, ys, *, nx=None, ny=None, stable=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(n))
    operands.append(_get_op_result_or_value(xy))
    operands.extend(_get_op_results_or_values(ys))
    if nx is not None: attributes["nx"] = nx
    if ny is not None: attributes["ny"] = ny
    if bool(stable): attributes["stable"] = _ods_ir.UnitAttr.get(
      _ods_get_default_loc_context(loc))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def n(self):
    return self.operation.operands[0]

  @builtins.property
  def xy(self):
    return self.operation.operands[1]

  @builtins.property
  def ys(self):
    _ods_variadic_group_length = len(self.operation.operands) - 3 + 1
    return self.operation.operands[2:2 + _ods_variadic_group_length]

  @builtins.property
  def nx(self):
    if "nx" not in self.operation.attributes:
      return None
    return _ods_ir.IntegerAttr(self.operation.attributes["nx"])

  @nx.setter
  def nx(self, value):
    if value is not None:
      self.operation.attributes["nx"] = value
    elif "nx" in self.operation.attributes:
      del self.operation.attributes["nx"]

  @nx.deleter
  def nx(self):
    del self.operation.attributes["nx"]

  @builtins.property
  def ny(self):
    if "ny" not in self.operation.attributes:
      return None
    return _ods_ir.IntegerAttr(self.operation.attributes["ny"])

  @ny.setter
  def ny(self, value):
    if value is not None:
      self.operation.attributes["ny"] = value
    elif "ny" in self.operation.attributes:
      del self.operation.attributes["ny"]

  @ny.deleter
  def ny(self):
    del self.operation.attributes["ny"]

  @builtins.property
  def stable(self):
    return "stable" in self.operation.attributes

  @stable.setter
  def stable(self, value):
    if bool(value):
      self.operation.attributes["stable"] = _ods_ir.UnitAttr.get()
    elif "stable" in self.operation.attributes:
      del self.operation.attributes["stable"]

  @stable.deleter
  def stable(self):
    del self.operation.attributes["stable"]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class SortOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.sort"

  _ODS_OPERAND_SEGMENTS = [1,-1,-1,]

  _ODS_REGIONS = (0, True)

  def __init__(self, n, xs, ys, *, stable=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(n))
    operands.append(_get_op_results_or_values(xs))
    operands.append(_get_op_results_or_values(ys))
    if bool(stable): attributes["stable"] = _ods_ir.UnitAttr.get(
      _ods_get_default_loc_context(loc))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def n(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 0)
    return operand_range[0]

  @builtins.property
  def xs(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 1)
    return operand_range

  @builtins.property
  def ys(self):
    operand_range = _ods_segmented_accessor(
         self.operation.operands,
         self.operation.attributes["operand_segment_sizes"], 2)
    return operand_range

  @builtins.property
  def stable(self):
    return "stable" in self.operation.attributes

  @stable.setter
  def stable(self, value):
    if bool(value):
      self.operation.attributes["stable"] = _ods_ir.UnitAttr.get()
    elif "stable" in self.operation.attributes:
      del self.operation.attributes["stable"]

  @stable.deleter
  def stable(self):
    del self.operation.attributes["stable"]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ToIndicesOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.indices"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, tensor, dimension, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(tensor))
    attributes["dimension"] = dimension
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def tensor(self):
    return self.operation.operands[0]

  @builtins.property
  def dimension(self):
    return _ods_ir.IntegerAttr(self.operation.attributes["dimension"])

  @dimension.setter
  def dimension(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["dimension"] = value

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ToPointersOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.pointers"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, tensor, dimension, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(tensor))
    attributes["dimension"] = dimension
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def tensor(self):
    return self.operation.operands[0]

  @builtins.property
  def dimension(self):
    return _ods_ir.IntegerAttr(self.operation.attributes["dimension"])

  @dimension.setter
  def dimension(self, value):
    if value is None:
      raise ValueError("'None' not allowed as value for mandatory attributes")
    self.operation.attributes["dimension"] = value

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class ToValuesOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.values"

  _ODS_REGIONS = (0, True)

  def __init__(self, result, tensor, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(tensor))
    results.append(result)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def tensor(self):
    return self.operation.operands[0]

  @builtins.property
  def result(self):
    return self.operation.results[0]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class UnaryOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.unary"

  _ODS_REGIONS = (2, True)

  def __init__(self, output, x, *, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    operands.append(_get_op_result_or_value(x))
    results.append(output)
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def x(self):
    return self.operation.operands[0]

  @builtins.property
  def output(self):
    return self.operation.results[0]

  @builtins.property
  def presentRegion(self):
    return self.regions[0]

  @builtins.property
  def absentRegion(self):
    return self.regions[1]

@_ods_cext.register_operation(_Dialect)
@_ods_extend_opview_class(_ods_ext_module)
class YieldOp(_ods_ir.OpView):
  OPERATION_NAME = "sparse_tensor.yield"

  _ODS_REGIONS = (0, True)

  def __init__(self, *, result=None, loc=None, ip=None):
    operands = []
    results = []
    attributes = {}
    regions = None
    if result is not None: operands.append(_get_op_result_or_value(result))
    _ods_successors = None
    super().__init__(self.build_generic(
      attributes=attributes, results=results, operands=operands,
      successors=_ods_successors, regions=regions, loc=loc, ip=ip))

  @builtins.property
  def result(self):
    return None if len(self.operation.operands) < 1 else self.operation.operands[0]
