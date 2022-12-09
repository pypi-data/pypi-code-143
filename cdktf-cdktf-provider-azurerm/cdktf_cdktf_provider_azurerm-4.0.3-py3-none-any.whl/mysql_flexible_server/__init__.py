'''
# `azurerm_mysql_flexible_server`

Refer to the Terraform Registory for docs: [`azurerm_mysql_flexible_server`](https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class MysqlFlexibleServer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServer",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server azurerm_mysql_flexible_server}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_password: typing.Optional[builtins.str] = None,
        backup_retention_days: typing.Optional[jsii.Number] = None,
        create_mode: typing.Optional[builtins.str] = None,
        delegated_subnet_id: typing.Optional[builtins.str] = None,
        geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        high_availability: typing.Optional[typing.Union["MysqlFlexibleServerHighAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["MysqlFlexibleServerMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        point_in_time_restore_time_in_utc: typing.Optional[builtins.str] = None,
        private_dns_zone_id: typing.Optional[builtins.str] = None,
        replication_role: typing.Optional[builtins.str] = None,
        sku_name: typing.Optional[builtins.str] = None,
        source_server_id: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Union["MysqlFlexibleServerStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MysqlFlexibleServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server azurerm_mysql_flexible_server} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#location MysqlFlexibleServer#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#name MysqlFlexibleServer#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#resource_group_name MysqlFlexibleServer#resource_group_name}.
        :param administrator_login: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#administrator_login MysqlFlexibleServer#administrator_login}.
        :param administrator_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#administrator_password MysqlFlexibleServer#administrator_password}.
        :param backup_retention_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#backup_retention_days MysqlFlexibleServer#backup_retention_days}.
        :param create_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#create_mode MysqlFlexibleServer#create_mode}.
        :param delegated_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#delegated_subnet_id MysqlFlexibleServer#delegated_subnet_id}.
        :param geo_redundant_backup_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#geo_redundant_backup_enabled MysqlFlexibleServer#geo_redundant_backup_enabled}.
        :param high_availability: high_availability block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#high_availability MysqlFlexibleServer#high_availability}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#id MysqlFlexibleServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#maintenance_window MysqlFlexibleServer#maintenance_window}
        :param point_in_time_restore_time_in_utc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#point_in_time_restore_time_in_utc MysqlFlexibleServer#point_in_time_restore_time_in_utc}.
        :param private_dns_zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#private_dns_zone_id MysqlFlexibleServer#private_dns_zone_id}.
        :param replication_role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#replication_role MysqlFlexibleServer#replication_role}.
        :param sku_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#sku_name MysqlFlexibleServer#sku_name}.
        :param source_server_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#source_server_id MysqlFlexibleServer#source_server_id}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#storage MysqlFlexibleServer#storage}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#tags MysqlFlexibleServer#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#timeouts MysqlFlexibleServer#timeouts}
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#version MysqlFlexibleServer#version}.
        :param zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#zone MysqlFlexibleServer#zone}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98dba0c4eafb7da79e34c906cce09b04572fcf4f18e7375783ac837c9e2202bc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MysqlFlexibleServerConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            administrator_login=administrator_login,
            administrator_password=administrator_password,
            backup_retention_days=backup_retention_days,
            create_mode=create_mode,
            delegated_subnet_id=delegated_subnet_id,
            geo_redundant_backup_enabled=geo_redundant_backup_enabled,
            high_availability=high_availability,
            id=id,
            maintenance_window=maintenance_window,
            point_in_time_restore_time_in_utc=point_in_time_restore_time_in_utc,
            private_dns_zone_id=private_dns_zone_id,
            replication_role=replication_role,
            sku_name=sku_name,
            source_server_id=source_server_id,
            storage=storage,
            tags=tags,
            timeouts=timeouts,
            version=version,
            zone=zone,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putHighAvailability")
    def put_high_availability(
        self,
        *,
        mode: builtins.str,
        standby_availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#mode MysqlFlexibleServer#mode}.
        :param standby_availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#standby_availability_zone MysqlFlexibleServer#standby_availability_zone}.
        '''
        value = MysqlFlexibleServerHighAvailability(
            mode=mode, standby_availability_zone=standby_availability_zone
        )

        return typing.cast(None, jsii.invoke(self, "putHighAvailability", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        day_of_week: typing.Optional[jsii.Number] = None,
        start_hour: typing.Optional[jsii.Number] = None,
        start_minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#day_of_week MysqlFlexibleServer#day_of_week}.
        :param start_hour: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#start_hour MysqlFlexibleServer#start_hour}.
        :param start_minute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#start_minute MysqlFlexibleServer#start_minute}.
        '''
        value = MysqlFlexibleServerMaintenanceWindow(
            day_of_week=day_of_week, start_hour=start_hour, start_minute=start_minute
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

    @jsii.member(jsii_name="putStorage")
    def put_storage(
        self,
        *,
        auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        iops: typing.Optional[jsii.Number] = None,
        size_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param auto_grow_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#auto_grow_enabled MysqlFlexibleServer#auto_grow_enabled}.
        :param iops: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#iops MysqlFlexibleServer#iops}.
        :param size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#size_gb MysqlFlexibleServer#size_gb}.
        '''
        value = MysqlFlexibleServerStorage(
            auto_grow_enabled=auto_grow_enabled, iops=iops, size_gb=size_gb
        )

        return typing.cast(None, jsii.invoke(self, "putStorage", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#create MysqlFlexibleServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#delete MysqlFlexibleServer#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#read MysqlFlexibleServer#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#update MysqlFlexibleServer#update}.
        '''
        value = MysqlFlexibleServerTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdministratorLogin")
    def reset_administrator_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorLogin", []))

    @jsii.member(jsii_name="resetAdministratorPassword")
    def reset_administrator_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorPassword", []))

    @jsii.member(jsii_name="resetBackupRetentionDays")
    def reset_backup_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupRetentionDays", []))

    @jsii.member(jsii_name="resetCreateMode")
    def reset_create_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateMode", []))

    @jsii.member(jsii_name="resetDelegatedSubnetId")
    def reset_delegated_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelegatedSubnetId", []))

    @jsii.member(jsii_name="resetGeoRedundantBackupEnabled")
    def reset_geo_redundant_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoRedundantBackupEnabled", []))

    @jsii.member(jsii_name="resetHighAvailability")
    def reset_high_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHighAvailability", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetPointInTimeRestoreTimeInUtc")
    def reset_point_in_time_restore_time_in_utc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTimeRestoreTimeInUtc", []))

    @jsii.member(jsii_name="resetPrivateDnsZoneId")
    def reset_private_dns_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateDnsZoneId", []))

    @jsii.member(jsii_name="resetReplicationRole")
    def reset_replication_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationRole", []))

    @jsii.member(jsii_name="resetSkuName")
    def reset_sku_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuName", []))

    @jsii.member(jsii_name="resetSourceServerId")
    def reset_source_server_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceServerId", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="highAvailability")
    def high_availability(self) -> "MysqlFlexibleServerHighAvailabilityOutputReference":
        return typing.cast("MysqlFlexibleServerHighAvailabilityOutputReference", jsii.get(self, "highAvailability"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> "MysqlFlexibleServerMaintenanceWindowOutputReference":
        return typing.cast("MysqlFlexibleServerMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "publicNetworkAccessEnabled"))

    @builtins.property
    @jsii.member(jsii_name="replicaCapacity")
    def replica_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicaCapacity"))

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> "MysqlFlexibleServerStorageOutputReference":
        return typing.cast("MysqlFlexibleServerStorageOutputReference", jsii.get(self, "storage"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MysqlFlexibleServerTimeoutsOutputReference":
        return typing.cast("MysqlFlexibleServerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginInput")
    def administrator_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorPasswordInput")
    def administrator_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDaysInput")
    def backup_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="createModeInput")
    def create_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createModeInput"))

    @builtins.property
    @jsii.member(jsii_name="delegatedSubnetIdInput")
    def delegated_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delegatedSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="geoRedundantBackupEnabledInput")
    def geo_redundant_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "geoRedundantBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="highAvailabilityInput")
    def high_availability_input(
        self,
    ) -> typing.Optional["MysqlFlexibleServerHighAvailability"]:
        return typing.cast(typing.Optional["MysqlFlexibleServerHighAvailability"], jsii.get(self, "highAvailabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["MysqlFlexibleServerMaintenanceWindow"]:
        return typing.cast(typing.Optional["MysqlFlexibleServerMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRestoreTimeInUtcInput")
    def point_in_time_restore_time_in_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pointInTimeRestoreTimeInUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="privateDnsZoneIdInput")
    def private_dns_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateDnsZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationRoleInput")
    def replication_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceServerIdInput")
    def source_server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceServerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional["MysqlFlexibleServerStorage"]:
        return typing.cast(typing.Optional["MysqlFlexibleServerStorage"], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MysqlFlexibleServerTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MysqlFlexibleServerTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLogin")
    def administrator_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLogin"))

    @administrator_login.setter
    def administrator_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ef5ad1b2bd7c4c26756a9e74b01187576b5fe86c392358510b32331d0c67e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLogin", value)

    @builtins.property
    @jsii.member(jsii_name="administratorPassword")
    def administrator_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorPassword"))

    @administrator_password.setter
    def administrator_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bc4d275af0282ef11bcfad3a8f508adf78e8a4cccdd4316fce877356eac014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorPassword", value)

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDays")
    def backup_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetentionDays"))

    @backup_retention_days.setter
    def backup_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd06c81e1406708dca4818db38e1dd098665b6a9c8d3247ebe76f4daa85582e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionDays", value)

    @builtins.property
    @jsii.member(jsii_name="createMode")
    def create_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createMode"))

    @create_mode.setter
    def create_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d52a71fe824bd00adf57d636f2643818bf98a836e3917481183068e16c836c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createMode", value)

    @builtins.property
    @jsii.member(jsii_name="delegatedSubnetId")
    def delegated_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delegatedSubnetId"))

    @delegated_subnet_id.setter
    def delegated_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13738d58a66f3858f5f88044b9f1b5bda080ca50d1cc3db9240005cf27bc0f4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delegatedSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="geoRedundantBackupEnabled")
    def geo_redundant_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "geoRedundantBackupEnabled"))

    @geo_redundant_backup_enabled.setter
    def geo_redundant_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efbdf3bd66711ba0b94d830ae8c74124f2a6bcafa2d5b0bf104b2ecd68cc2bd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoRedundantBackupEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d89d1cf56ca1653cd36fe686c31232c5cd7c094da0804c9c493ec47d031516)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4500da6b95b111f33853b3ca3bd771bee3cbd0809739e0dc169b00acedd4ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085c9c613ce4bc5feee7b0dc704ab7867dc69bc38214a0a1ba348ca55741f6e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRestoreTimeInUtc")
    def point_in_time_restore_time_in_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pointInTimeRestoreTimeInUtc"))

    @point_in_time_restore_time_in_utc.setter
    def point_in_time_restore_time_in_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5a9293734b78aa55a2946b04a3a4251fbd337bfb6029c9f2f47ec850410671e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeRestoreTimeInUtc", value)

    @builtins.property
    @jsii.member(jsii_name="privateDnsZoneId")
    def private_dns_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateDnsZoneId"))

    @private_dns_zone_id.setter
    def private_dns_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f1fffed5945eab306d15ff45b618976387df9efb85e111efa8c03f4e4cb5b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateDnsZoneId", value)

    @builtins.property
    @jsii.member(jsii_name="replicationRole")
    def replication_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationRole"))

    @replication_role.setter
    def replication_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0805959e0fa32393de04921df0c733873cce2baa7bcd5ac1a0eb9a2423693a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationRole", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0392a4841e0ae1176f0100605e1621880d23398983428b6ec9cbbeea73d8d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937b9ae1c47e7f149f1d5c2183118ca9e19170284a6bc08b5d866f68620511b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value)

    @builtins.property
    @jsii.member(jsii_name="sourceServerId")
    def source_server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceServerId"))

    @source_server_id.setter
    def source_server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358fd27a7465c6270fb31408b66ee708b28f0f08bbc52874ae11a420c5f17a26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceServerId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04b4f5b17e834f8347608a6adca803dba6a3638ced4ac96da8302fa092a7ad19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e407ee2fbeb8b423ac8019d5cb7e3e7fb3e360bb305bd81255e674605fed9e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26168eeac64f48f2a83eb53f29fe2f0f41e1d08c37ebc435d68d137008534664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "administrator_login": "administratorLogin",
        "administrator_password": "administratorPassword",
        "backup_retention_days": "backupRetentionDays",
        "create_mode": "createMode",
        "delegated_subnet_id": "delegatedSubnetId",
        "geo_redundant_backup_enabled": "geoRedundantBackupEnabled",
        "high_availability": "highAvailability",
        "id": "id",
        "maintenance_window": "maintenanceWindow",
        "point_in_time_restore_time_in_utc": "pointInTimeRestoreTimeInUtc",
        "private_dns_zone_id": "privateDnsZoneId",
        "replication_role": "replicationRole",
        "sku_name": "skuName",
        "source_server_id": "sourceServerId",
        "storage": "storage",
        "tags": "tags",
        "timeouts": "timeouts",
        "version": "version",
        "zone": "zone",
    },
)
class MysqlFlexibleServerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_password: typing.Optional[builtins.str] = None,
        backup_retention_days: typing.Optional[jsii.Number] = None,
        create_mode: typing.Optional[builtins.str] = None,
        delegated_subnet_id: typing.Optional[builtins.str] = None,
        geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        high_availability: typing.Optional[typing.Union["MysqlFlexibleServerHighAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        maintenance_window: typing.Optional[typing.Union["MysqlFlexibleServerMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        point_in_time_restore_time_in_utc: typing.Optional[builtins.str] = None,
        private_dns_zone_id: typing.Optional[builtins.str] = None,
        replication_role: typing.Optional[builtins.str] = None,
        sku_name: typing.Optional[builtins.str] = None,
        source_server_id: typing.Optional[builtins.str] = None,
        storage: typing.Optional[typing.Union["MysqlFlexibleServerStorage", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MysqlFlexibleServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#location MysqlFlexibleServer#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#name MysqlFlexibleServer#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#resource_group_name MysqlFlexibleServer#resource_group_name}.
        :param administrator_login: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#administrator_login MysqlFlexibleServer#administrator_login}.
        :param administrator_password: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#administrator_password MysqlFlexibleServer#administrator_password}.
        :param backup_retention_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#backup_retention_days MysqlFlexibleServer#backup_retention_days}.
        :param create_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#create_mode MysqlFlexibleServer#create_mode}.
        :param delegated_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#delegated_subnet_id MysqlFlexibleServer#delegated_subnet_id}.
        :param geo_redundant_backup_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#geo_redundant_backup_enabled MysqlFlexibleServer#geo_redundant_backup_enabled}.
        :param high_availability: high_availability block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#high_availability MysqlFlexibleServer#high_availability}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#id MysqlFlexibleServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#maintenance_window MysqlFlexibleServer#maintenance_window}
        :param point_in_time_restore_time_in_utc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#point_in_time_restore_time_in_utc MysqlFlexibleServer#point_in_time_restore_time_in_utc}.
        :param private_dns_zone_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#private_dns_zone_id MysqlFlexibleServer#private_dns_zone_id}.
        :param replication_role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#replication_role MysqlFlexibleServer#replication_role}.
        :param sku_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#sku_name MysqlFlexibleServer#sku_name}.
        :param source_server_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#source_server_id MysqlFlexibleServer#source_server_id}.
        :param storage: storage block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#storage MysqlFlexibleServer#storage}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#tags MysqlFlexibleServer#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#timeouts MysqlFlexibleServer#timeouts}
        :param version: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#version MysqlFlexibleServer#version}.
        :param zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#zone MysqlFlexibleServer#zone}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(high_availability, dict):
            high_availability = MysqlFlexibleServerHighAvailability(**high_availability)
        if isinstance(maintenance_window, dict):
            maintenance_window = MysqlFlexibleServerMaintenanceWindow(**maintenance_window)
        if isinstance(storage, dict):
            storage = MysqlFlexibleServerStorage(**storage)
        if isinstance(timeouts, dict):
            timeouts = MysqlFlexibleServerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57207811f7b2f58d2cf455efd0f16e6a04c6fe775092948a3bb4fd99a5b8aed9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument administrator_login", value=administrator_login, expected_type=type_hints["administrator_login"])
            check_type(argname="argument administrator_password", value=administrator_password, expected_type=type_hints["administrator_password"])
            check_type(argname="argument backup_retention_days", value=backup_retention_days, expected_type=type_hints["backup_retention_days"])
            check_type(argname="argument create_mode", value=create_mode, expected_type=type_hints["create_mode"])
            check_type(argname="argument delegated_subnet_id", value=delegated_subnet_id, expected_type=type_hints["delegated_subnet_id"])
            check_type(argname="argument geo_redundant_backup_enabled", value=geo_redundant_backup_enabled, expected_type=type_hints["geo_redundant_backup_enabled"])
            check_type(argname="argument high_availability", value=high_availability, expected_type=type_hints["high_availability"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument point_in_time_restore_time_in_utc", value=point_in_time_restore_time_in_utc, expected_type=type_hints["point_in_time_restore_time_in_utc"])
            check_type(argname="argument private_dns_zone_id", value=private_dns_zone_id, expected_type=type_hints["private_dns_zone_id"])
            check_type(argname="argument replication_role", value=replication_role, expected_type=type_hints["replication_role"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument source_server_id", value=source_server_id, expected_type=type_hints["source_server_id"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if administrator_login is not None:
            self._values["administrator_login"] = administrator_login
        if administrator_password is not None:
            self._values["administrator_password"] = administrator_password
        if backup_retention_days is not None:
            self._values["backup_retention_days"] = backup_retention_days
        if create_mode is not None:
            self._values["create_mode"] = create_mode
        if delegated_subnet_id is not None:
            self._values["delegated_subnet_id"] = delegated_subnet_id
        if geo_redundant_backup_enabled is not None:
            self._values["geo_redundant_backup_enabled"] = geo_redundant_backup_enabled
        if high_availability is not None:
            self._values["high_availability"] = high_availability
        if id is not None:
            self._values["id"] = id
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if point_in_time_restore_time_in_utc is not None:
            self._values["point_in_time_restore_time_in_utc"] = point_in_time_restore_time_in_utc
        if private_dns_zone_id is not None:
            self._values["private_dns_zone_id"] = private_dns_zone_id
        if replication_role is not None:
            self._values["replication_role"] = replication_role
        if sku_name is not None:
            self._values["sku_name"] = sku_name
        if source_server_id is not None:
            self._values["source_server_id"] = source_server_id
        if storage is not None:
            self._values["storage"] = storage
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#location MysqlFlexibleServer#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#name MysqlFlexibleServer#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#resource_group_name MysqlFlexibleServer#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrator_login(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#administrator_login MysqlFlexibleServer#administrator_login}.'''
        result = self._values.get("administrator_login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def administrator_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#administrator_password MysqlFlexibleServer#administrator_password}.'''
        result = self._values.get("administrator_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_retention_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#backup_retention_days MysqlFlexibleServer#backup_retention_days}.'''
        result = self._values.get("backup_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def create_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#create_mode MysqlFlexibleServer#create_mode}.'''
        result = self._values.get("create_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delegated_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#delegated_subnet_id MysqlFlexibleServer#delegated_subnet_id}.'''
        result = self._values.get("delegated_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geo_redundant_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#geo_redundant_backup_enabled MysqlFlexibleServer#geo_redundant_backup_enabled}.'''
        result = self._values.get("geo_redundant_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def high_availability(
        self,
    ) -> typing.Optional["MysqlFlexibleServerHighAvailability"]:
        '''high_availability block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#high_availability MysqlFlexibleServer#high_availability}
        '''
        result = self._values.get("high_availability")
        return typing.cast(typing.Optional["MysqlFlexibleServerHighAvailability"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#id MysqlFlexibleServer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["MysqlFlexibleServerMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#maintenance_window MysqlFlexibleServer#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["MysqlFlexibleServerMaintenanceWindow"], result)

    @builtins.property
    def point_in_time_restore_time_in_utc(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#point_in_time_restore_time_in_utc MysqlFlexibleServer#point_in_time_restore_time_in_utc}.'''
        result = self._values.get("point_in_time_restore_time_in_utc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_dns_zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#private_dns_zone_id MysqlFlexibleServer#private_dns_zone_id}.'''
        result = self._values.get("private_dns_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#replication_role MysqlFlexibleServer#replication_role}.'''
        result = self._values.get("replication_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#sku_name MysqlFlexibleServer#sku_name}.'''
        result = self._values.get("sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_server_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#source_server_id MysqlFlexibleServer#source_server_id}.'''
        result = self._values.get("source_server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage(self) -> typing.Optional["MysqlFlexibleServerStorage"]:
        '''storage block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#storage MysqlFlexibleServer#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional["MysqlFlexibleServerStorage"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#tags MysqlFlexibleServer#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MysqlFlexibleServerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#timeouts MysqlFlexibleServer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MysqlFlexibleServerTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#version MysqlFlexibleServer#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#zone MysqlFlexibleServer#zone}.'''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlFlexibleServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerHighAvailability",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "standby_availability_zone": "standbyAvailabilityZone",
    },
)
class MysqlFlexibleServerHighAvailability:
    def __init__(
        self,
        *,
        mode: builtins.str,
        standby_availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#mode MysqlFlexibleServer#mode}.
        :param standby_availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#standby_availability_zone MysqlFlexibleServer#standby_availability_zone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07ca551fc5bef2b8bb83e2996a6462d83d3636c69ed72a6e250379a82a84262)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument standby_availability_zone", value=standby_availability_zone, expected_type=type_hints["standby_availability_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if standby_availability_zone is not None:
            self._values["standby_availability_zone"] = standby_availability_zone

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#mode MysqlFlexibleServer#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standby_availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#standby_availability_zone MysqlFlexibleServer#standby_availability_zone}.'''
        result = self._values.get("standby_availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlFlexibleServerHighAvailability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MysqlFlexibleServerHighAvailabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerHighAvailabilityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88afb4591363b40f89c96eff8cfb92540c9f3b61a3cdd1369255cd23f0634fbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStandbyAvailabilityZone")
    def reset_standby_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandbyAvailabilityZone", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="standbyAvailabilityZoneInput")
    def standby_availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "standbyAvailabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fef5eee2ffe3cd0df9e9281ef7e4b0c13ff8a58dc8f61776c11494bbe98c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="standbyAvailabilityZone")
    def standby_availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standbyAvailabilityZone"))

    @standby_availability_zone.setter
    def standby_availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c0ec196860dd6424d9b6f9f4cf40cbfe7f2ebc93daf8ed4b514d7451281a85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standbyAvailabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MysqlFlexibleServerHighAvailability]:
        return typing.cast(typing.Optional[MysqlFlexibleServerHighAvailability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MysqlFlexibleServerHighAvailability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3637f4be01bbce889587488c8ebbc351ef14ce6c431d30a460e2609cf5f6138c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={
        "day_of_week": "dayOfWeek",
        "start_hour": "startHour",
        "start_minute": "startMinute",
    },
)
class MysqlFlexibleServerMaintenanceWindow:
    def __init__(
        self,
        *,
        day_of_week: typing.Optional[jsii.Number] = None,
        start_hour: typing.Optional[jsii.Number] = None,
        start_minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#day_of_week MysqlFlexibleServer#day_of_week}.
        :param start_hour: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#start_hour MysqlFlexibleServer#start_hour}.
        :param start_minute: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#start_minute MysqlFlexibleServer#start_minute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e569994e64ddb6c47d6f0757cc7344dd194886ccd9ebd507fe9e53502d12e7)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument start_hour", value=start_hour, expected_type=type_hints["start_hour"])
            check_type(argname="argument start_minute", value=start_minute, expected_type=type_hints["start_minute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day_of_week is not None:
            self._values["day_of_week"] = day_of_week
        if start_hour is not None:
            self._values["start_hour"] = start_hour
        if start_minute is not None:
            self._values["start_minute"] = start_minute

    @builtins.property
    def day_of_week(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#day_of_week MysqlFlexibleServer#day_of_week}.'''
        result = self._values.get("day_of_week")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_hour(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#start_hour MysqlFlexibleServer#start_hour}.'''
        result = self._values.get("start_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_minute(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#start_minute MysqlFlexibleServer#start_minute}.'''
        result = self._values.get("start_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlFlexibleServerMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MysqlFlexibleServerMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerMaintenanceWindowOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006de97fe21bbe1b885129cfa77eaeeec1a326fc2f508d41656dbfcd0278ab8a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDayOfWeek")
    def reset_day_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayOfWeek", []))

    @jsii.member(jsii_name="resetStartHour")
    def reset_start_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartHour", []))

    @jsii.member(jsii_name="resetStartMinute")
    def reset_start_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartMinute", []))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="startHourInput")
    def start_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startHourInput"))

    @builtins.property
    @jsii.member(jsii_name="startMinuteInput")
    def start_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2edff08e5e25465d80578a782e1b3d37a27407126c1eb5813fdcb71061ff091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value)

    @builtins.property
    @jsii.member(jsii_name="startHour")
    def start_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startHour"))

    @start_hour.setter
    def start_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baccfe03afd6ab79dc5fe328f4889b36e19bc218df4b5c48b1395486041134a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startHour", value)

    @builtins.property
    @jsii.member(jsii_name="startMinute")
    def start_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startMinute"))

    @start_minute.setter
    def start_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd5526e5752e4cf0565c829ae2df41476f6d94a17ad2a6d4f8ddc8a24d97b70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startMinute", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MysqlFlexibleServerMaintenanceWindow]:
        return typing.cast(typing.Optional[MysqlFlexibleServerMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MysqlFlexibleServerMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2610e584367b940efd6484fedf6fb8db2c07b666a15bdf60597ca0aaa4138341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerStorage",
    jsii_struct_bases=[],
    name_mapping={
        "auto_grow_enabled": "autoGrowEnabled",
        "iops": "iops",
        "size_gb": "sizeGb",
    },
)
class MysqlFlexibleServerStorage:
    def __init__(
        self,
        *,
        auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        iops: typing.Optional[jsii.Number] = None,
        size_gb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param auto_grow_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#auto_grow_enabled MysqlFlexibleServer#auto_grow_enabled}.
        :param iops: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#iops MysqlFlexibleServer#iops}.
        :param size_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#size_gb MysqlFlexibleServer#size_gb}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7450b3901e678821777d44d047ad7dafda5705c48aa197b7c104d1964c256e)
            check_type(argname="argument auto_grow_enabled", value=auto_grow_enabled, expected_type=type_hints["auto_grow_enabled"])
            check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
            check_type(argname="argument size_gb", value=size_gb, expected_type=type_hints["size_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_grow_enabled is not None:
            self._values["auto_grow_enabled"] = auto_grow_enabled
        if iops is not None:
            self._values["iops"] = iops
        if size_gb is not None:
            self._values["size_gb"] = size_gb

    @builtins.property
    def auto_grow_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#auto_grow_enabled MysqlFlexibleServer#auto_grow_enabled}.'''
        result = self._values.get("auto_grow_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#iops MysqlFlexibleServer#iops}.'''
        result = self._values.get("iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#size_gb MysqlFlexibleServer#size_gb}.'''
        result = self._values.get("size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlFlexibleServerStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MysqlFlexibleServerStorageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerStorageOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5249f146712c452ca117e1e5d77f7cd4b6670f7e3773c01311c732b873f901fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutoGrowEnabled")
    def reset_auto_grow_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoGrowEnabled", []))

    @jsii.member(jsii_name="resetIops")
    def reset_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIops", []))

    @jsii.member(jsii_name="resetSizeGb")
    def reset_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeGb", []))

    @builtins.property
    @jsii.member(jsii_name="autoGrowEnabledInput")
    def auto_grow_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoGrowEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="iopsInput")
    def iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "iopsInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeGbInput")
    def size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="autoGrowEnabled")
    def auto_grow_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoGrowEnabled"))

    @auto_grow_enabled.setter
    def auto_grow_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf6ac36b0b34b224d41198898bd84e54250b9924702094df83cd918117012b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoGrowEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "iops"))

    @iops.setter
    def iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe0a9c651097ee176b77996243ea26506751830200d682daab83078eca18de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iops", value)

    @builtins.property
    @jsii.member(jsii_name="sizeGb")
    def size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeGb"))

    @size_gb.setter
    def size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b319441c1f5b1eda2254b996a3c9334ada44d4fc04623a705c4f76e024bdbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MysqlFlexibleServerStorage]:
        return typing.cast(typing.Optional[MysqlFlexibleServerStorage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MysqlFlexibleServerStorage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cbb455eaf88dd18952bf5544ee996cad778aa1fad03106eec383dc1d94c6c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MysqlFlexibleServerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#create MysqlFlexibleServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#delete MysqlFlexibleServer#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#read MysqlFlexibleServer#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#update MysqlFlexibleServer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43e431b72d68113ac598cd6a8f8be10045aafd8411bfae7cb77f7421d322d179)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#create MysqlFlexibleServer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#delete MysqlFlexibleServer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#read MysqlFlexibleServer#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/mysql_flexible_server#update MysqlFlexibleServer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MysqlFlexibleServerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MysqlFlexibleServerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mysqlFlexibleServer.MysqlFlexibleServerTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2a4231c48350b1e4389a23f8b2366dbeb28214d11891d1b0b5385e6b2b91ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bec683695d18491696f76e555de9aae2995aa284f111b7c5cb53f02367faa5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1833aab5abcc4b8ccbc3412d5c20545e993316b59d348815245e656f050d5482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd04b5376c96c5aa3718a0dbb756b9ed3b699255193cfc63988fded172167b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f537545b5483fdd9b08cd3559d7d5d1c64d213d56e59a73c658bedf2ea638a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MysqlFlexibleServerTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MysqlFlexibleServerTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MysqlFlexibleServerTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce151dac10b843d6d5f20afc30b6e97b5fe2165a635ba05c74cf29ade2afd1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MysqlFlexibleServer",
    "MysqlFlexibleServerConfig",
    "MysqlFlexibleServerHighAvailability",
    "MysqlFlexibleServerHighAvailabilityOutputReference",
    "MysqlFlexibleServerMaintenanceWindow",
    "MysqlFlexibleServerMaintenanceWindowOutputReference",
    "MysqlFlexibleServerStorage",
    "MysqlFlexibleServerStorageOutputReference",
    "MysqlFlexibleServerTimeouts",
    "MysqlFlexibleServerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__98dba0c4eafb7da79e34c906cce09b04572fcf4f18e7375783ac837c9e2202bc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    administrator_login: typing.Optional[builtins.str] = None,
    administrator_password: typing.Optional[builtins.str] = None,
    backup_retention_days: typing.Optional[jsii.Number] = None,
    create_mode: typing.Optional[builtins.str] = None,
    delegated_subnet_id: typing.Optional[builtins.str] = None,
    geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    high_availability: typing.Optional[typing.Union[MysqlFlexibleServerHighAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[MysqlFlexibleServerMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    point_in_time_restore_time_in_utc: typing.Optional[builtins.str] = None,
    private_dns_zone_id: typing.Optional[builtins.str] = None,
    replication_role: typing.Optional[builtins.str] = None,
    sku_name: typing.Optional[builtins.str] = None,
    source_server_id: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Union[MysqlFlexibleServerStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MysqlFlexibleServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ef5ad1b2bd7c4c26756a9e74b01187576b5fe86c392358510b32331d0c67e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bc4d275af0282ef11bcfad3a8f508adf78e8a4cccdd4316fce877356eac014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd06c81e1406708dca4818db38e1dd098665b6a9c8d3247ebe76f4daa85582e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d52a71fe824bd00adf57d636f2643818bf98a836e3917481183068e16c836c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13738d58a66f3858f5f88044b9f1b5bda080ca50d1cc3db9240005cf27bc0f4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbdf3bd66711ba0b94d830ae8c74124f2a6bcafa2d5b0bf104b2ecd68cc2bd3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d89d1cf56ca1653cd36fe686c31232c5cd7c094da0804c9c493ec47d031516(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4500da6b95b111f33853b3ca3bd771bee3cbd0809739e0dc169b00acedd4ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085c9c613ce4bc5feee7b0dc704ab7867dc69bc38214a0a1ba348ca55741f6e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a9293734b78aa55a2946b04a3a4251fbd337bfb6029c9f2f47ec850410671e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f1fffed5945eab306d15ff45b618976387df9efb85e111efa8c03f4e4cb5b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0805959e0fa32393de04921df0c733873cce2baa7bcd5ac1a0eb9a2423693a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0392a4841e0ae1176f0100605e1621880d23398983428b6ec9cbbeea73d8d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937b9ae1c47e7f149f1d5c2183118ca9e19170284a6bc08b5d866f68620511b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358fd27a7465c6270fb31408b66ee708b28f0f08bbc52874ae11a420c5f17a26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04b4f5b17e834f8347608a6adca803dba6a3638ced4ac96da8302fa092a7ad19(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e407ee2fbeb8b423ac8019d5cb7e3e7fb3e360bb305bd81255e674605fed9e49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26168eeac64f48f2a83eb53f29fe2f0f41e1d08c37ebc435d68d137008534664(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57207811f7b2f58d2cf455efd0f16e6a04c6fe775092948a3bb4fd99a5b8aed9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    administrator_login: typing.Optional[builtins.str] = None,
    administrator_password: typing.Optional[builtins.str] = None,
    backup_retention_days: typing.Optional[jsii.Number] = None,
    create_mode: typing.Optional[builtins.str] = None,
    delegated_subnet_id: typing.Optional[builtins.str] = None,
    geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    high_availability: typing.Optional[typing.Union[MysqlFlexibleServerHighAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    maintenance_window: typing.Optional[typing.Union[MysqlFlexibleServerMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    point_in_time_restore_time_in_utc: typing.Optional[builtins.str] = None,
    private_dns_zone_id: typing.Optional[builtins.str] = None,
    replication_role: typing.Optional[builtins.str] = None,
    sku_name: typing.Optional[builtins.str] = None,
    source_server_id: typing.Optional[builtins.str] = None,
    storage: typing.Optional[typing.Union[MysqlFlexibleServerStorage, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MysqlFlexibleServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07ca551fc5bef2b8bb83e2996a6462d83d3636c69ed72a6e250379a82a84262(
    *,
    mode: builtins.str,
    standby_availability_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88afb4591363b40f89c96eff8cfb92540c9f3b61a3cdd1369255cd23f0634fbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fef5eee2ffe3cd0df9e9281ef7e4b0c13ff8a58dc8f61776c11494bbe98c51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c0ec196860dd6424d9b6f9f4cf40cbfe7f2ebc93daf8ed4b514d7451281a85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3637f4be01bbce889587488c8ebbc351ef14ce6c431d30a460e2609cf5f6138c(
    value: typing.Optional[MysqlFlexibleServerHighAvailability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e569994e64ddb6c47d6f0757cc7344dd194886ccd9ebd507fe9e53502d12e7(
    *,
    day_of_week: typing.Optional[jsii.Number] = None,
    start_hour: typing.Optional[jsii.Number] = None,
    start_minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006de97fe21bbe1b885129cfa77eaeeec1a326fc2f508d41656dbfcd0278ab8a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2edff08e5e25465d80578a782e1b3d37a27407126c1eb5813fdcb71061ff091(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baccfe03afd6ab79dc5fe328f4889b36e19bc218df4b5c48b1395486041134a7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd5526e5752e4cf0565c829ae2df41476f6d94a17ad2a6d4f8ddc8a24d97b70(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2610e584367b940efd6484fedf6fb8db2c07b666a15bdf60597ca0aaa4138341(
    value: typing.Optional[MysqlFlexibleServerMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7450b3901e678821777d44d047ad7dafda5705c48aa197b7c104d1964c256e(
    *,
    auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    iops: typing.Optional[jsii.Number] = None,
    size_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5249f146712c452ca117e1e5d77f7cd4b6670f7e3773c01311c732b873f901fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf6ac36b0b34b224d41198898bd84e54250b9924702094df83cd918117012b9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe0a9c651097ee176b77996243ea26506751830200d682daab83078eca18de6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b319441c1f5b1eda2254b996a3c9334ada44d4fc04623a705c4f76e024bdbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cbb455eaf88dd18952bf5544ee996cad778aa1fad03106eec383dc1d94c6c9(
    value: typing.Optional[MysqlFlexibleServerStorage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43e431b72d68113ac598cd6a8f8be10045aafd8411bfae7cb77f7421d322d179(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2a4231c48350b1e4389a23f8b2366dbeb28214d11891d1b0b5385e6b2b91ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bec683695d18491696f76e555de9aae2995aa284f111b7c5cb53f02367faa5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1833aab5abcc4b8ccbc3412d5c20545e993316b59d348815245e656f050d5482(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd04b5376c96c5aa3718a0dbb756b9ed3b699255193cfc63988fded172167b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f537545b5483fdd9b08cd3559d7d5d1c64d213d56e59a73c658bedf2ea638a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce151dac10b843d6d5f20afc30b6e97b5fe2165a635ba05c74cf29ade2afd1dc(
    value: typing.Optional[typing.Union[MysqlFlexibleServerTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
