"""
Volume mesh component
"""
import json
import os.path
import warnings
from enum import Enum
from typing import Optional, Union

import numpy as np
from pydantic import Extra, Field, validator

from flow360.cloud.http_util import http
from flow360.cloud.s3_utils import S3TransferType
from flow360.component.flow360_base_model import Flow360BaseModel, Flow360Resource, on_cloud_resource_only
from flow360.component.flow360_solver_params import (
    Flow360MeshParams,
    Flow360Params,
    NoSlipWall,
)
from flow360.version import Flow360Version

try:
    import h5py
    _H5PY_AVAILABLE = True
except ImportError:
    _H5PY_AVAILABLE = False


def get_datatype(dataset):
    """
    Get datatype of dataset
    :param dataset:
    :return:
    """
    data_raw = np.empty(dataset.shape, dataset.dtype)
    dataset.read_direct(data_raw)
    data_str = "".join([chr(i) for i in dataset])
    return data_str


def get_no_slip_walls(params: Union[Flow360Params, Flow360MeshParams]):
    """
    Get wall boundary names
    :param params:
    :param solver_version:
    :return:
    """
    assert params
    if (
        isinstance(params, Flow360MeshParams)
        and params.boundaries
        and params.boundaries.no_slip_walls
    ):
        return params.boundaries.no_slip_walls

    if isinstance(params, Flow360Params) and params.boundaries:
        return [
            wall_name
            for wall_name, wall in params.boundaries.items()
            if isinstance(wall, NoSlipWall)
        ]

    return []


def get_boundries_from_sliding_interfaces(params: Union[Flow360Params, Flow360MeshParams]):
    """
    Get wall boundary names
    :param params:
    :param solver_version:
    :return:
    """
    assert params
    res = []

    if params.sliding_interfaces and params.sliding_interfaces.rotating_patches:
        res += params.sliding_interfaces.rotating_patches[:]
    if params.sliding_interfaces and params.sliding_interfaces.stationary_patches:
        res += params.sliding_interfaces.stationary_patches[:]
    return res


# pylint: disable=too-many-branches
def get_boundaries_from_file(cgns_file: str, solver_version: str = None):
    """
    Get boundary names from CGNS file
    :param cgns_file:
    :param solver_version:
    :return:
    """
    names = []
    with h5py.File(cgns_file, "r") as h5_file:
        base = h5_file["Base"]
        for zone_name, zone in base.items():
            if zone_name == " data":
                continue
            if zone.attrs["label"].decode() != "Zone_t":
                continue
            zone_type = get_datatype(base[f"{zone_name}/ZoneType/ data"])
            if zone_type not in ["Structured", "Unstructured"]:
                continue
            for section_name, section in zone.items():
                if section_name == " data":
                    continue
                if "label" not in section.attrs:
                    continue
                if solver_version and Flow360Version(solver_version) < Flow360Version(
                    "release-22.2.1.0"
                ):
                    if section.attrs["label"].decode() != "Elements_t":
                        continue
                    element_type_tag = int(zone[f"{section_name}/ data"][0])
                    if element_type_tag in [5, 7]:
                        names.append(f"{zone_name}/{section_name}")
                    if element_type_tag == 20:
                        first_element_type_tag = zone[f"{section_name}/ElementConnectivity/ data"][
                            0
                        ]
                        if first_element_type_tag in [5, 7]:
                            names.append(f"{zone_name}/{section_name}")
                else:
                    if section.attrs["label"].decode() != "ZoneBC_t":
                        continue
                    for bc_name, bc_zone in section.items():

                        if bc_zone.attrs["label"].decode() == "BC_t":
                            names.append(f"{zone_name}/{bc_name}")

        return names


def validate_cgns(
    cgns_file: str, params: Union[Flow360Params, Flow360MeshParams], solver_version=None
):
    """
    Validate CGNS file
    :param cgns_file:
    :param params:
    :param solver_version:
    :return:
    """
    assert cgns_file
    assert params
    boundaries_in_file = get_boundaries_from_file(cgns_file, solver_version)

    boundaries_in_params = get_no_slip_walls(params) + get_boundries_from_sliding_interfaces(params)
    boundaries_in_file = set(boundaries_in_file)
    boundaries_in_params = set(boundaries_in_params)
    if not boundaries_in_file.issuperset(boundaries_in_params):
        raise ValueError(
            "The following input boundary names from mesh json are not found in mesh:"
            + f" {' '.join(boundaries_in_params - boundaries_in_file)}."
            + f" Boundary names in cgns: {' '.join(boundaries_in_file)}"
            + f" Boundary names in params: {' '.join(boundaries_in_file)}"
        )
    print(
        f'Notice: {" ".join(boundaries_in_file - boundaries_in_params)} is '
        + "tagged as wall in cgns file, but not in input params"
    )


class VolumeMeshLog(Enum):
    """
    Volume mesh log
    """

    USER_LOG = "user.log"
    PY_LOG = "validateFlow360Mesh.py.log"


class VolumeMeshDownloadable(Enum):
    """
    Volume mesh downloadable files
    """

    CONFIG_JSON = "config.json"


class VolumeMeshFileFormat(Enum):
    """
    Volume mesh file format
    """

    UGRID = "aflr3"
    CGNS = "cgns"

    def ext(self) -> str:
        """
        Get the extention for a file name.
        :return:
        """
        if self is VolumeMeshFileFormat.UGRID:
            return '.ugrid'
        if self is VolumeMeshFileFormat.CGNS:
            return '.cgns'
        return ""

    @classmethod
    def detect(cls, file: str):
        ext = os.path.splitext(file)[1]
        if ext == VolumeMeshFileFormat.UGRID.ext():
            return VolumeMeshFileFormat.UGRID
        elif ext == VolumeMeshFileFormat.CGNS.ext():     
            return VolumeMeshFileFormat.CGNS
        else:
            raise RuntimeError('Unsupported file format {}'.format(file))


class UGRIDEndianness(Enum):
    """
    UGRID endianness
    """

    LITTLE = "little"
    BIG = "big"
    NONE = None

    def ext(self) -> str:
        """
        Get the extention for a file name.
        :return:
        """
        if self is UGRIDEndianness.LITTLE:
            return '.lb8'
        if self is UGRIDEndianness.BIG:
            return '.b8'
        return ""


    @classmethod
    def detect(cls, file: str):
        if VolumeMeshFileFormat.detect(file) is not VolumeMeshFileFormat.UGRID:
            return UGRIDEndianness.NONE
        basename = os.path.splitext(file)[0]
        ext = os.path.splitext(basename)[1]
        if ext == UGRIDEndianness.LITTLE.ext():
            return UGRIDEndianness.LITTLE
        elif ext == UGRIDEndianness.BIG.ext():     
            return UGRIDEndianness.BIG
        else:
            raise RuntimeError('Unknown endianness for file {}'.format(file))


class CompressionFormat(Enum):
    """
    Volume mesh file format
    """

    GZ = "gz"
    BZ2 = "bz2"
    NONE = None

    def ext(self) -> str:
        """
        Get the extention for a file name.
        :return:
        """
        if self is CompressionFormat.GZ:
            return '.gz'
        if self is CompressionFormat.BZ2:
            return '.bz2'
        return ""

    @classmethod
    def detect(cls, file: str):
        file_name, ext = os.path.splitext(file)
        if ext == CompressionFormat.GZ.ext():
            return CompressionFormat.GZ, file_name
        elif ext == CompressionFormat.BZ2.ext():     
            return CompressionFormat.BZ2, file_name
        else:
            return CompressionFormat.NONE, file


class VolumeMeshMeta(Flow360BaseModel, extra=Extra.allow):
    """
    VolumeMeshMeta component
    """

    id: str = Field(alias="meshId")
    name: str = Field(alias="meshName")
    status: str = Field(alias="meshStatus")
    created_at: str = Field(alias="meshAddTime")
    surface_mesh_id: Optional[str] = Field(alias="surfaceMeshId")
    mesh_params: str = Field(alias="meshParams")
    mesh_format: VolumeMeshFileFormat = Field(alias="meshFormat")
    endianness: UGRIDEndianness = Field(alias="meshEndianness")
    compression: CompressionFormat = Field(alias="meshCompression")

    @validator('endianness', pre=True)
    def init_endianness(cls, v):
        return UGRIDEndianness(v) or UGRIDEndianness.NONE

    @validator('compression', pre=True)
    def init_compression(cls, v):
        return CompressionFormat(v) or CompressionFormat.NONE



class VolumeMesh(Flow360Resource):
    """
    Surface mesh component
    """

    def __init__(self, id: str = None):
        super().__init__(resource_type="Volume Mesh",
                         INFO_TYPE_CLASS=VolumeMeshMeta,
                         S3_TRANSFER_METHOD=S3TransferType.VOLUME_MESH, 
                         endpoint="volumemeshes", id=id)
        if id is not None:
            self.get_info()

    @on_cloud_resource_only
    def download_file(
        self, file_name: Union[str, VolumeMeshDownloadable], to_file=".", keep_folder: bool = True
    ):
        """
        Download file from surface mesh
        :param file_name:
        :param to_file:
        :param keep_folder:
        :return:
        """
        if isinstance(file_name, VolumeMeshDownloadable):
            file_name = file_name.value
        super().download(
            file_name, to_file, keep_folder
        )

    @on_cloud_resource_only
    def download(
        self, to_file=".", keep_folder: bool = True
    ):
        """
        Download file from volume mesh
        :param file_name:
        :param to_file:
        :param keep_folder:
        :return:
        """
        super().download(
            self._remote_file_name(), to_file, keep_folder
        )


    @on_cloud_resource_only
    def download_log(self, log: VolumeMeshLog, to_file=".", keep_folder: bool = True):
        """
        Download log
        :param log:
        :param to_file: file name on local disk, could be either folder or file name.
        :param keep_folder: If true, the downloaded file will be put in the same folder as the file on cloud. Only work
        when file_name is a folder name.
        :return:
        """

        self.download_file(f"logs/{log.value}", to_file, keep_folder)

    @on_cloud_resource_only
    def _complete_upload(self, remote_file_name):
        """
        Complete volume mesh upload
        :return:
        """
        resp = self.post({}, method=f'completeUpload?fileName={remote_file_name}')
        self._info = VolumeMeshMeta(**resp)

    @classmethod
    def from_cloud(cls, id: str):
        """
        Get volujme mesh info from cloud
        :param id:
        :return:
        """
        return cls(id)

    # pylint: disable=too-many-arguments
    # @classmethod
    # def from_surface_mesh(
    #     cls,
    #     volume_mesh_name: str,
    #     surface_mesh_id: str,
    #     config_file: str,
    #     tags: [str] = None,
    #     solver_version=None,
    # ):
    #     """
    #     Create volume mesh from surface mesh
    #     :param volume_mesh_name:
    #     :param surface_mesh_id:
    #     :param config_file:
    #     :param tags:
    #     :param solver_version:
    #     :return:
    #     """
    #     assert volume_mesh_name
    #     assert os.path.exists(config_file)
    #     assert surface_mesh_id
    #     with open(config_file, "r", encoding="utf-8") as config_f:
    #         json_content = json.load(config_f)
    #     body = {
    #         "name": volume_mesh_name,
    #         "tags": tags,
    #         "surfaceMeshId": surface_mesh_id,
    #         "config": json.dumps(json_content),
    #         "format": "cgns",
    #     }

    #     if solver_version:
    #         body["solverVersion"] = solver_version

    #     resp = http.post("volumemeshes", body)
    #     if resp:
    #         return cls(**resp)
    #     return None

    @on_cloud_resource_only
    def _remote_file_name(self,  mesh_format=None, compression=None, endianness=None):        
        compression = compression or self.info.compression
        mesh_format = mesh_format or self.info.mesh_format
        endianness = endianness or self.info.endianness

        remote_file_name = 'mesh'
        if mesh_format is VolumeMeshFileFormat.CGNS:
            remote_file_name = self.info.name

        return f'{remote_file_name}{endianness.ext()}{mesh_format.ext()}{compression.ext()}'

    @classmethod
    def from_file(
        cls,
        file_name: str,
        params: Flow360MeshParams,
        name: str = None,
        tags: [str] = None,
        solver_version=None,
    ):
        """
        Create volume mesh from ugrid file
        :param volume_mesh_name:
        :param file_name:
        :param params:
        :param tags:
        :param solver_version:
        :return:
        """
        assert os.path.exists(file_name)
        assert params

        if name is None:
            name = os.path.splitext(os.path.basename(file_name))[0]

        mesh = cls()
        compression, file_name_no_compression = CompressionFormat.detect(file_name)
        mesh_format = VolumeMeshFileFormat.detect(file_name_no_compression)
        endianness = UGRIDEndianness.detect(file_name_no_compression)

        body = {
            "meshName": name,
            "meshTags": tags,
            "meshFormat": mesh_format.value,
            "meshEndianness": endianness.value,
            "meshParams": params.json(),
        }

        if solver_version:
            body["solverVersion"] = solver_version

        resp = mesh.post(body)

        if not resp:
            return None

        mesh._info = VolumeMeshMeta(**resp)
        mesh.init_id(mesh._info.id)
        remote_file_name = mesh._remote_file_name(mesh_format, compression, endianness)
        mesh.upload(remote_file_name, file_name)
        mesh._complete_upload(remote_file_name)
        return mesh


    #     # pylint: disable=too-many-arguments

    # @classmethod
    # def from_cgns_file(
    #     cls,
    #     volume_mesh_name: str,
    #     file_name: str,
    #     params: Union[Flow360Params, Flow360MeshParams],
    #     tags: [str] = None,
    #     solver_version=None,
    # ):
    #     """
    #     Create volume mesh from ugrid file
    #     :param volume_mesh_name:
    #     :param file_name:
    #     :param params:
    #     :param tags:
    #     :param solver_version:
    #     :return:
    #     """
    #     assert volume_mesh_name
    #     assert os.path.exists(file_name)
    #     assert params

    #     if _H5PY_AVAILABLE:
    #         validate_cgns(file_name, params, solver_version=solver_version)
    #     else:
    #         warnings.warn(
    #             "Could not check consistency between mesh file and"
    #             " Flow360.json file. h5py module not found. This is optional functionality"
    #         )

    #     body = {
    #         "meshName": volume_mesh_name,
    #         "meshTags": tags,
    #         "meshFormat": "cgns",
    #         "meshParams": params.json(),
    #     }

    #     if solver_version:
    #         body["solverVersion"] = solver_version

    #     resp = http.post("volumemeshes", body)
    #     if resp:
    #         return cls(**resp)
    #     return None
