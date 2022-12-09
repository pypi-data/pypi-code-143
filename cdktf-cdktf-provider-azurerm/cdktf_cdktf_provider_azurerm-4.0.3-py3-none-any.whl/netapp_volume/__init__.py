'''
# `azurerm_netapp_volume`

Refer to the Terraform Registory for docs: [`azurerm_netapp_volume`](https://www.terraform.io/docs/providers/azurerm/r/netapp_volume).
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


class NetappVolume(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolume",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume azurerm_netapp_volume}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_name: builtins.str,
        location: builtins.str,
        name: builtins.str,
        pool_name: builtins.str,
        resource_group_name: builtins.str,
        service_level: builtins.str,
        storage_quota_in_gb: jsii.Number,
        subnet_id: builtins.str,
        volume_path: builtins.str,
        azure_vmware_data_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_from_snapshot_resource_id: typing.Optional[builtins.str] = None,
        data_protection_replication: typing.Optional[typing.Union["NetappVolumeDataProtectionReplication", typing.Dict[builtins.str, typing.Any]]] = None,
        data_protection_snapshot_policy: typing.Optional[typing.Union["NetappVolumeDataProtectionSnapshotPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        export_policy_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeExportPolicyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        network_features: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_style: typing.Optional[builtins.str] = None,
        snapshot_directory_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        throughput_in_mibps: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume azurerm_netapp_volume} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#account_name NetappVolume#account_name}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#location NetappVolume#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#name NetappVolume#name}.
        :param pool_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#pool_name NetappVolume#pool_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#resource_group_name NetappVolume#resource_group_name}.
        :param service_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#service_level NetappVolume#service_level}.
        :param storage_quota_in_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#storage_quota_in_gb NetappVolume#storage_quota_in_gb}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#subnet_id NetappVolume#subnet_id}.
        :param volume_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#volume_path NetappVolume#volume_path}.
        :param azure_vmware_data_store_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#azure_vmware_data_store_enabled NetappVolume#azure_vmware_data_store_enabled}.
        :param create_from_snapshot_resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#create_from_snapshot_resource_id NetappVolume#create_from_snapshot_resource_id}.
        :param data_protection_replication: data_protection_replication block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#data_protection_replication NetappVolume#data_protection_replication}
        :param data_protection_snapshot_policy: data_protection_snapshot_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#data_protection_snapshot_policy NetappVolume#data_protection_snapshot_policy}
        :param export_policy_rule: export_policy_rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#export_policy_rule NetappVolume#export_policy_rule}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#id NetappVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_features: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#network_features NetappVolume#network_features}.
        :param protocols: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#protocols NetappVolume#protocols}.
        :param security_style: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#security_style NetappVolume#security_style}.
        :param snapshot_directory_visible: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#snapshot_directory_visible NetappVolume#snapshot_directory_visible}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#tags NetappVolume#tags}.
        :param throughput_in_mibps: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#throughput_in_mibps NetappVolume#throughput_in_mibps}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#timeouts NetappVolume#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980f8f0ee2b8dcb347c2afa0fa8f444b0148698c9264e6f6fba3dccea919aaab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetappVolumeConfig(
            account_name=account_name,
            location=location,
            name=name,
            pool_name=pool_name,
            resource_group_name=resource_group_name,
            service_level=service_level,
            storage_quota_in_gb=storage_quota_in_gb,
            subnet_id=subnet_id,
            volume_path=volume_path,
            azure_vmware_data_store_enabled=azure_vmware_data_store_enabled,
            create_from_snapshot_resource_id=create_from_snapshot_resource_id,
            data_protection_replication=data_protection_replication,
            data_protection_snapshot_policy=data_protection_snapshot_policy,
            export_policy_rule=export_policy_rule,
            id=id,
            network_features=network_features,
            protocols=protocols,
            security_style=security_style,
            snapshot_directory_visible=snapshot_directory_visible,
            tags=tags,
            throughput_in_mibps=throughput_in_mibps,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putDataProtectionReplication")
    def put_data_protection_replication(
        self,
        *,
        remote_volume_location: builtins.str,
        remote_volume_resource_id: builtins.str,
        replication_frequency: builtins.str,
        endpoint_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_volume_location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#remote_volume_location NetappVolume#remote_volume_location}.
        :param remote_volume_resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#remote_volume_resource_id NetappVolume#remote_volume_resource_id}.
        :param replication_frequency: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#replication_frequency NetappVolume#replication_frequency}.
        :param endpoint_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#endpoint_type NetappVolume#endpoint_type}.
        '''
        value = NetappVolumeDataProtectionReplication(
            remote_volume_location=remote_volume_location,
            remote_volume_resource_id=remote_volume_resource_id,
            replication_frequency=replication_frequency,
            endpoint_type=endpoint_type,
        )

        return typing.cast(None, jsii.invoke(self, "putDataProtectionReplication", [value]))

    @jsii.member(jsii_name="putDataProtectionSnapshotPolicy")
    def put_data_protection_snapshot_policy(
        self,
        *,
        snapshot_policy_id: builtins.str,
    ) -> None:
        '''
        :param snapshot_policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#snapshot_policy_id NetappVolume#snapshot_policy_id}.
        '''
        value = NetappVolumeDataProtectionSnapshotPolicy(
            snapshot_policy_id=snapshot_policy_id
        )

        return typing.cast(None, jsii.invoke(self, "putDataProtectionSnapshotPolicy", [value]))

    @jsii.member(jsii_name="putExportPolicyRule")
    def put_export_policy_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeExportPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3be3ef25b86d53ef43a7979775dd8bd2b195716efeda32e595898fb138652b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExportPolicyRule", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#create NetappVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#delete NetappVolume#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#read NetappVolume#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#update NetappVolume#update}.
        '''
        value = NetappVolumeTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAzureVmwareDataStoreEnabled")
    def reset_azure_vmware_data_store_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureVmwareDataStoreEnabled", []))

    @jsii.member(jsii_name="resetCreateFromSnapshotResourceId")
    def reset_create_from_snapshot_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateFromSnapshotResourceId", []))

    @jsii.member(jsii_name="resetDataProtectionReplication")
    def reset_data_protection_replication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProtectionReplication", []))

    @jsii.member(jsii_name="resetDataProtectionSnapshotPolicy")
    def reset_data_protection_snapshot_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProtectionSnapshotPolicy", []))

    @jsii.member(jsii_name="resetExportPolicyRule")
    def reset_export_policy_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExportPolicyRule", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworkFeatures")
    def reset_network_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkFeatures", []))

    @jsii.member(jsii_name="resetProtocols")
    def reset_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocols", []))

    @jsii.member(jsii_name="resetSecurityStyle")
    def reset_security_style(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityStyle", []))

    @jsii.member(jsii_name="resetSnapshotDirectoryVisible")
    def reset_snapshot_directory_visible(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnapshotDirectoryVisible", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetThroughputInMibps")
    def reset_throughput_in_mibps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThroughputInMibps", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionReplication")
    def data_protection_replication(
        self,
    ) -> "NetappVolumeDataProtectionReplicationOutputReference":
        return typing.cast("NetappVolumeDataProtectionReplicationOutputReference", jsii.get(self, "dataProtectionReplication"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionSnapshotPolicy")
    def data_protection_snapshot_policy(
        self,
    ) -> "NetappVolumeDataProtectionSnapshotPolicyOutputReference":
        return typing.cast("NetappVolumeDataProtectionSnapshotPolicyOutputReference", jsii.get(self, "dataProtectionSnapshotPolicy"))

    @builtins.property
    @jsii.member(jsii_name="exportPolicyRule")
    def export_policy_rule(self) -> "NetappVolumeExportPolicyRuleList":
        return typing.cast("NetappVolumeExportPolicyRuleList", jsii.get(self, "exportPolicyRule"))

    @builtins.property
    @jsii.member(jsii_name="mountIpAddresses")
    def mount_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mountIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetappVolumeTimeoutsOutputReference":
        return typing.cast("NetappVolumeTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="azureVmwareDataStoreEnabledInput")
    def azure_vmware_data_store_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "azureVmwareDataStoreEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="createFromSnapshotResourceIdInput")
    def create_from_snapshot_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createFromSnapshotResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionReplicationInput")
    def data_protection_replication_input(
        self,
    ) -> typing.Optional["NetappVolumeDataProtectionReplication"]:
        return typing.cast(typing.Optional["NetappVolumeDataProtectionReplication"], jsii.get(self, "dataProtectionReplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionSnapshotPolicyInput")
    def data_protection_snapshot_policy_input(
        self,
    ) -> typing.Optional["NetappVolumeDataProtectionSnapshotPolicy"]:
        return typing.cast(typing.Optional["NetappVolumeDataProtectionSnapshotPolicy"], jsii.get(self, "dataProtectionSnapshotPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="exportPolicyRuleInput")
    def export_policy_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeExportPolicyRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeExportPolicyRule"]]], jsii.get(self, "exportPolicyRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkFeaturesInput")
    def network_features_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="poolNameInput")
    def pool_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolNameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="securityStyleInput")
    def security_style_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceLevelInput")
    def service_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotDirectoryVisibleInput")
    def snapshot_directory_visible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "snapshotDirectoryVisibleInput"))

    @builtins.property
    @jsii.member(jsii_name="storageQuotaInGbInput")
    def storage_quota_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageQuotaInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputInMibpsInput")
    def throughput_in_mibps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputInMibpsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["NetappVolumeTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["NetappVolumeTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumePathInput")
    def volume_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumePathInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44d14a47300c2bb82f1cd4ea6c0776ec7893cea50b74e2098900a0d57a19031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value)

    @builtins.property
    @jsii.member(jsii_name="azureVmwareDataStoreEnabled")
    def azure_vmware_data_store_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "azureVmwareDataStoreEnabled"))

    @azure_vmware_data_store_enabled.setter
    def azure_vmware_data_store_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a63e4f82caf618c8c66b6bd2ab0cfa9ebdaec7cf0ea419f104127adeeb23dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureVmwareDataStoreEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="createFromSnapshotResourceId")
    def create_from_snapshot_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createFromSnapshotResourceId"))

    @create_from_snapshot_resource_id.setter
    def create_from_snapshot_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b42eede59cbed32ed556d8245ed6267df09c0b3c7ffbd7456eda12dd7070a3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createFromSnapshotResourceId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7765a6c7343b4c8095511ee246a5d0855a110569eaf2799c49bc654639a90f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8192c0e3d5f35a560e076efa9469e152886dc55773b4a9e3942a49739ea219e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5e80f71ae17c74d529f5eaf794b437dd777ba02f4e3f4d1babf6addfd67e703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkFeatures")
    def network_features(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkFeatures"))

    @network_features.setter
    def network_features(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0bc321f6c49a4d8ccc3a8d79ab22ddc823c51ae24afe6eafbd568290564708d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkFeatures", value)

    @builtins.property
    @jsii.member(jsii_name="poolName")
    def pool_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "poolName"))

    @pool_name.setter
    def pool_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b38032e1cf966eb4d4b207fb26c347bd2ec369efd5449d6e7c3fde19c2953c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolName", value)

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0526d73dc8f9adbc2a588c698f8656cf84543b1c5dbde8ac3402cd5723ff7417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e415f25b0db852cdd09704980cbd5d2919fa632784ae5cdc01d6d02b9edfe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="securityStyle")
    def security_style(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityStyle"))

    @security_style.setter
    def security_style(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1a88aa3c2ffff97bd53fe11756c7955ccae68470109d0dcee37028a3c277d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityStyle", value)

    @builtins.property
    @jsii.member(jsii_name="serviceLevel")
    def service_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLevel"))

    @service_level.setter
    def service_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd687d5fbbbe5d54e57f89c91eb4ac0f648bc0fdc8c97828b14d5b9e6fcae2e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceLevel", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotDirectoryVisible")
    def snapshot_directory_visible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "snapshotDirectoryVisible"))

    @snapshot_directory_visible.setter
    def snapshot_directory_visible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6574d299e197324fb61f41f397466a0609dcdf65506ad76ea2b4137f8d151083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotDirectoryVisible", value)

    @builtins.property
    @jsii.member(jsii_name="storageQuotaInGb")
    def storage_quota_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageQuotaInGb"))

    @storage_quota_in_gb.setter
    def storage_quota_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc4a1e9db20465458b1c4823d93994f8936be704bba4642930f780e5addb7c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageQuotaInGb", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66692039a526452bb25e4d1dd7f928730fd9447321124a2387ff668291b872a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e133b35d0e32a9b79a33936d5d445151bcefbe5ca171c3dd64c0679831da3b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="throughputInMibps")
    def throughput_in_mibps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughputInMibps"))

    @throughput_in_mibps.setter
    def throughput_in_mibps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2aa1303618b907c0133f3ab8ca076db1882600d5adac1729b1347ccab10662)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputInMibps", value)

    @builtins.property
    @jsii.member(jsii_name="volumePath")
    def volume_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumePath"))

    @volume_path.setter
    def volume_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fdaea5d1356fd0c281b90cd0f152e7be7c42ca97e559fbee179d0209dbf70df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumePath", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_name": "accountName",
        "location": "location",
        "name": "name",
        "pool_name": "poolName",
        "resource_group_name": "resourceGroupName",
        "service_level": "serviceLevel",
        "storage_quota_in_gb": "storageQuotaInGb",
        "subnet_id": "subnetId",
        "volume_path": "volumePath",
        "azure_vmware_data_store_enabled": "azureVmwareDataStoreEnabled",
        "create_from_snapshot_resource_id": "createFromSnapshotResourceId",
        "data_protection_replication": "dataProtectionReplication",
        "data_protection_snapshot_policy": "dataProtectionSnapshotPolicy",
        "export_policy_rule": "exportPolicyRule",
        "id": "id",
        "network_features": "networkFeatures",
        "protocols": "protocols",
        "security_style": "securityStyle",
        "snapshot_directory_visible": "snapshotDirectoryVisible",
        "tags": "tags",
        "throughput_in_mibps": "throughputInMibps",
        "timeouts": "timeouts",
    },
)
class NetappVolumeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_name: builtins.str,
        location: builtins.str,
        name: builtins.str,
        pool_name: builtins.str,
        resource_group_name: builtins.str,
        service_level: builtins.str,
        storage_quota_in_gb: jsii.Number,
        subnet_id: builtins.str,
        volume_path: builtins.str,
        azure_vmware_data_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        create_from_snapshot_resource_id: typing.Optional[builtins.str] = None,
        data_protection_replication: typing.Optional[typing.Union["NetappVolumeDataProtectionReplication", typing.Dict[builtins.str, typing.Any]]] = None,
        data_protection_snapshot_policy: typing.Optional[typing.Union["NetappVolumeDataProtectionSnapshotPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        export_policy_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeExportPolicyRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        network_features: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_style: typing.Optional[builtins.str] = None,
        snapshot_directory_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        throughput_in_mibps: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#account_name NetappVolume#account_name}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#location NetappVolume#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#name NetappVolume#name}.
        :param pool_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#pool_name NetappVolume#pool_name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#resource_group_name NetappVolume#resource_group_name}.
        :param service_level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#service_level NetappVolume#service_level}.
        :param storage_quota_in_gb: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#storage_quota_in_gb NetappVolume#storage_quota_in_gb}.
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#subnet_id NetappVolume#subnet_id}.
        :param volume_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#volume_path NetappVolume#volume_path}.
        :param azure_vmware_data_store_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#azure_vmware_data_store_enabled NetappVolume#azure_vmware_data_store_enabled}.
        :param create_from_snapshot_resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#create_from_snapshot_resource_id NetappVolume#create_from_snapshot_resource_id}.
        :param data_protection_replication: data_protection_replication block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#data_protection_replication NetappVolume#data_protection_replication}
        :param data_protection_snapshot_policy: data_protection_snapshot_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#data_protection_snapshot_policy NetappVolume#data_protection_snapshot_policy}
        :param export_policy_rule: export_policy_rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#export_policy_rule NetappVolume#export_policy_rule}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#id NetappVolume#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param network_features: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#network_features NetappVolume#network_features}.
        :param protocols: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#protocols NetappVolume#protocols}.
        :param security_style: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#security_style NetappVolume#security_style}.
        :param snapshot_directory_visible: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#snapshot_directory_visible NetappVolume#snapshot_directory_visible}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#tags NetappVolume#tags}.
        :param throughput_in_mibps: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#throughput_in_mibps NetappVolume#throughput_in_mibps}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#timeouts NetappVolume#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_protection_replication, dict):
            data_protection_replication = NetappVolumeDataProtectionReplication(**data_protection_replication)
        if isinstance(data_protection_snapshot_policy, dict):
            data_protection_snapshot_policy = NetappVolumeDataProtectionSnapshotPolicy(**data_protection_snapshot_policy)
        if isinstance(timeouts, dict):
            timeouts = NetappVolumeTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e42bf1b4137fa695051e34d876b82ba1419b2d79b46a55e4ae5a1f2f973c01f9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pool_name", value=pool_name, expected_type=type_hints["pool_name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument service_level", value=service_level, expected_type=type_hints["service_level"])
            check_type(argname="argument storage_quota_in_gb", value=storage_quota_in_gb, expected_type=type_hints["storage_quota_in_gb"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument volume_path", value=volume_path, expected_type=type_hints["volume_path"])
            check_type(argname="argument azure_vmware_data_store_enabled", value=azure_vmware_data_store_enabled, expected_type=type_hints["azure_vmware_data_store_enabled"])
            check_type(argname="argument create_from_snapshot_resource_id", value=create_from_snapshot_resource_id, expected_type=type_hints["create_from_snapshot_resource_id"])
            check_type(argname="argument data_protection_replication", value=data_protection_replication, expected_type=type_hints["data_protection_replication"])
            check_type(argname="argument data_protection_snapshot_policy", value=data_protection_snapshot_policy, expected_type=type_hints["data_protection_snapshot_policy"])
            check_type(argname="argument export_policy_rule", value=export_policy_rule, expected_type=type_hints["export_policy_rule"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument network_features", value=network_features, expected_type=type_hints["network_features"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument security_style", value=security_style, expected_type=type_hints["security_style"])
            check_type(argname="argument snapshot_directory_visible", value=snapshot_directory_visible, expected_type=type_hints["snapshot_directory_visible"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument throughput_in_mibps", value=throughput_in_mibps, expected_type=type_hints["throughput_in_mibps"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "location": location,
            "name": name,
            "pool_name": pool_name,
            "resource_group_name": resource_group_name,
            "service_level": service_level,
            "storage_quota_in_gb": storage_quota_in_gb,
            "subnet_id": subnet_id,
            "volume_path": volume_path,
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
        if azure_vmware_data_store_enabled is not None:
            self._values["azure_vmware_data_store_enabled"] = azure_vmware_data_store_enabled
        if create_from_snapshot_resource_id is not None:
            self._values["create_from_snapshot_resource_id"] = create_from_snapshot_resource_id
        if data_protection_replication is not None:
            self._values["data_protection_replication"] = data_protection_replication
        if data_protection_snapshot_policy is not None:
            self._values["data_protection_snapshot_policy"] = data_protection_snapshot_policy
        if export_policy_rule is not None:
            self._values["export_policy_rule"] = export_policy_rule
        if id is not None:
            self._values["id"] = id
        if network_features is not None:
            self._values["network_features"] = network_features
        if protocols is not None:
            self._values["protocols"] = protocols
        if security_style is not None:
            self._values["security_style"] = security_style
        if snapshot_directory_visible is not None:
            self._values["snapshot_directory_visible"] = snapshot_directory_visible
        if tags is not None:
            self._values["tags"] = tags
        if throughput_in_mibps is not None:
            self._values["throughput_in_mibps"] = throughput_in_mibps
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#account_name NetappVolume#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#location NetappVolume#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#name NetappVolume#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pool_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#pool_name NetappVolume#pool_name}.'''
        result = self._values.get("pool_name")
        assert result is not None, "Required property 'pool_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#resource_group_name NetappVolume#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#service_level NetappVolume#service_level}.'''
        result = self._values.get("service_level")
        assert result is not None, "Required property 'service_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_quota_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#storage_quota_in_gb NetappVolume#storage_quota_in_gb}.'''
        result = self._values.get("storage_quota_in_gb")
        assert result is not None, "Required property 'storage_quota_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#subnet_id NetappVolume#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#volume_path NetappVolume#volume_path}.'''
        result = self._values.get("volume_path")
        assert result is not None, "Required property 'volume_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azure_vmware_data_store_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#azure_vmware_data_store_enabled NetappVolume#azure_vmware_data_store_enabled}.'''
        result = self._values.get("azure_vmware_data_store_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def create_from_snapshot_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#create_from_snapshot_resource_id NetappVolume#create_from_snapshot_resource_id}.'''
        result = self._values.get("create_from_snapshot_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_protection_replication(
        self,
    ) -> typing.Optional["NetappVolumeDataProtectionReplication"]:
        '''data_protection_replication block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#data_protection_replication NetappVolume#data_protection_replication}
        '''
        result = self._values.get("data_protection_replication")
        return typing.cast(typing.Optional["NetappVolumeDataProtectionReplication"], result)

    @builtins.property
    def data_protection_snapshot_policy(
        self,
    ) -> typing.Optional["NetappVolumeDataProtectionSnapshotPolicy"]:
        '''data_protection_snapshot_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#data_protection_snapshot_policy NetappVolume#data_protection_snapshot_policy}
        '''
        result = self._values.get("data_protection_snapshot_policy")
        return typing.cast(typing.Optional["NetappVolumeDataProtectionSnapshotPolicy"], result)

    @builtins.property
    def export_policy_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeExportPolicyRule"]]]:
        '''export_policy_rule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#export_policy_rule NetappVolume#export_policy_rule}
        '''
        result = self._values.get("export_policy_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeExportPolicyRule"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#id NetappVolume#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_features(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#network_features NetappVolume#network_features}.'''
        result = self._values.get("network_features")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#protocols NetappVolume#protocols}.'''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_style(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#security_style NetappVolume#security_style}.'''
        result = self._values.get("security_style")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def snapshot_directory_visible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#snapshot_directory_visible NetappVolume#snapshot_directory_visible}.'''
        result = self._values.get("snapshot_directory_visible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#tags NetappVolume#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def throughput_in_mibps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#throughput_in_mibps NetappVolume#throughput_in_mibps}.'''
        result = self._values.get("throughput_in_mibps")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetappVolumeTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#timeouts NetappVolume#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetappVolumeTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeDataProtectionReplication",
    jsii_struct_bases=[],
    name_mapping={
        "remote_volume_location": "remoteVolumeLocation",
        "remote_volume_resource_id": "remoteVolumeResourceId",
        "replication_frequency": "replicationFrequency",
        "endpoint_type": "endpointType",
    },
)
class NetappVolumeDataProtectionReplication:
    def __init__(
        self,
        *,
        remote_volume_location: builtins.str,
        remote_volume_resource_id: builtins.str,
        replication_frequency: builtins.str,
        endpoint_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_volume_location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#remote_volume_location NetappVolume#remote_volume_location}.
        :param remote_volume_resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#remote_volume_resource_id NetappVolume#remote_volume_resource_id}.
        :param replication_frequency: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#replication_frequency NetappVolume#replication_frequency}.
        :param endpoint_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#endpoint_type NetappVolume#endpoint_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c3b0072417db6c0e396f5bf407d1e47b7cd5effb877114c52693cf5c568bf6)
            check_type(argname="argument remote_volume_location", value=remote_volume_location, expected_type=type_hints["remote_volume_location"])
            check_type(argname="argument remote_volume_resource_id", value=remote_volume_resource_id, expected_type=type_hints["remote_volume_resource_id"])
            check_type(argname="argument replication_frequency", value=replication_frequency, expected_type=type_hints["replication_frequency"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_volume_location": remote_volume_location,
            "remote_volume_resource_id": remote_volume_resource_id,
            "replication_frequency": replication_frequency,
        }
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type

    @builtins.property
    def remote_volume_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#remote_volume_location NetappVolume#remote_volume_location}.'''
        result = self._values.get("remote_volume_location")
        assert result is not None, "Required property 'remote_volume_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_volume_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#remote_volume_resource_id NetappVolume#remote_volume_resource_id}.'''
        result = self._values.get("remote_volume_resource_id")
        assert result is not None, "Required property 'remote_volume_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#replication_frequency NetappVolume#replication_frequency}.'''
        result = self._values.get("replication_frequency")
        assert result is not None, "Required property 'replication_frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#endpoint_type NetappVolume#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeDataProtectionReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeDataProtectionReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeDataProtectionReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d658831a27e29a0729169e9ab0761cbc61c9b11084520f15330205605bbdad4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndpointType")
    def reset_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointType", []))

    @builtins.property
    @jsii.member(jsii_name="endpointTypeInput")
    def endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeLocationInput")
    def remote_volume_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteVolumeLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeResourceIdInput")
    def remote_volume_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteVolumeResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationFrequencyInput")
    def replication_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2faf0355dcc5198eef90a4b7d0572319e68be812bedbf31b6ca5e86eae27a3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value)

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeLocation")
    def remote_volume_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteVolumeLocation"))

    @remote_volume_location.setter
    def remote_volume_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7309a1ed7bdf1d5df315b65ee3091f5f4eed61babc93f404bd28aa8db1afb638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVolumeLocation", value)

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeResourceId")
    def remote_volume_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteVolumeResourceId"))

    @remote_volume_resource_id.setter
    def remote_volume_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f766e5ac6cf9ba6e11fe72a301538e1210a4324d8a9a131392b54f279e5c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVolumeResourceId", value)

    @builtins.property
    @jsii.member(jsii_name="replicationFrequency")
    def replication_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationFrequency"))

    @replication_frequency.setter
    def replication_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2e86618a5838cfc78eb61b02c4f8bba56f2da7639a90ae64a93d5017c9e5e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetappVolumeDataProtectionReplication]:
        return typing.cast(typing.Optional[NetappVolumeDataProtectionReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeDataProtectionReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef1fd26d945762c39f1c8a768e28638af148c68f423c8e2852bca2979328bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeDataProtectionSnapshotPolicy",
    jsii_struct_bases=[],
    name_mapping={"snapshot_policy_id": "snapshotPolicyId"},
)
class NetappVolumeDataProtectionSnapshotPolicy:
    def __init__(self, *, snapshot_policy_id: builtins.str) -> None:
        '''
        :param snapshot_policy_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#snapshot_policy_id NetappVolume#snapshot_policy_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee13f7ba943bbcb7dc6a3c98dbb0f2cb199a0f41a23ce1f7499686ebd777cc7)
            check_type(argname="argument snapshot_policy_id", value=snapshot_policy_id, expected_type=type_hints["snapshot_policy_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snapshot_policy_id": snapshot_policy_id,
        }

    @builtins.property
    def snapshot_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#snapshot_policy_id NetappVolume#snapshot_policy_id}.'''
        result = self._values.get("snapshot_policy_id")
        assert result is not None, "Required property 'snapshot_policy_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeDataProtectionSnapshotPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeDataProtectionSnapshotPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeDataProtectionSnapshotPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__835caed9cc66c88695cb77bff5366eee945dcfb30d16bb3687e37daa130e4323)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicyIdInput")
    def snapshot_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicyId")
    def snapshot_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotPolicyId"))

    @snapshot_policy_id.setter
    def snapshot_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04bb511c89f7a396d2c35849a6d8908b0ba6367ad53880927c0807ce823ff28b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotPolicyId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeDataProtectionSnapshotPolicy]:
        return typing.cast(typing.Optional[NetappVolumeDataProtectionSnapshotPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeDataProtectionSnapshotPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a919e095942fc04932c9251b6adb71b610fdb99e058493c4bff891f2d4389cdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeExportPolicyRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_clients": "allowedClients",
        "rule_index": "ruleIndex",
        "protocols_enabled": "protocolsEnabled",
        "root_access_enabled": "rootAccessEnabled",
        "unix_read_only": "unixReadOnly",
        "unix_read_write": "unixReadWrite",
    },
)
class NetappVolumeExportPolicyRule:
    def __init__(
        self,
        *,
        allowed_clients: typing.Sequence[builtins.str],
        rule_index: jsii.Number,
        protocols_enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
        root_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unix_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unix_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_clients: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#allowed_clients NetappVolume#allowed_clients}.
        :param rule_index: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#rule_index NetappVolume#rule_index}.
        :param protocols_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#protocols_enabled NetappVolume#protocols_enabled}.
        :param root_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#root_access_enabled NetappVolume#root_access_enabled}.
        :param unix_read_only: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#unix_read_only NetappVolume#unix_read_only}.
        :param unix_read_write: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#unix_read_write NetappVolume#unix_read_write}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34c4c56163cc4aeec6c0bde58cff05aeed8fe4d2203bdb81ec0db6952f9829da)
            check_type(argname="argument allowed_clients", value=allowed_clients, expected_type=type_hints["allowed_clients"])
            check_type(argname="argument rule_index", value=rule_index, expected_type=type_hints["rule_index"])
            check_type(argname="argument protocols_enabled", value=protocols_enabled, expected_type=type_hints["protocols_enabled"])
            check_type(argname="argument root_access_enabled", value=root_access_enabled, expected_type=type_hints["root_access_enabled"])
            check_type(argname="argument unix_read_only", value=unix_read_only, expected_type=type_hints["unix_read_only"])
            check_type(argname="argument unix_read_write", value=unix_read_write, expected_type=type_hints["unix_read_write"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_clients": allowed_clients,
            "rule_index": rule_index,
        }
        if protocols_enabled is not None:
            self._values["protocols_enabled"] = protocols_enabled
        if root_access_enabled is not None:
            self._values["root_access_enabled"] = root_access_enabled
        if unix_read_only is not None:
            self._values["unix_read_only"] = unix_read_only
        if unix_read_write is not None:
            self._values["unix_read_write"] = unix_read_write

    @builtins.property
    def allowed_clients(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#allowed_clients NetappVolume#allowed_clients}.'''
        result = self._values.get("allowed_clients")
        assert result is not None, "Required property 'allowed_clients' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def rule_index(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#rule_index NetappVolume#rule_index}.'''
        result = self._values.get("rule_index")
        assert result is not None, "Required property 'rule_index' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def protocols_enabled(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#protocols_enabled NetappVolume#protocols_enabled}.'''
        result = self._values.get("protocols_enabled")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def root_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#root_access_enabled NetappVolume#root_access_enabled}.'''
        result = self._values.get("root_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unix_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#unix_read_only NetappVolume#unix_read_only}.'''
        result = self._values.get("unix_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unix_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#unix_read_write NetappVolume#unix_read_write}.'''
        result = self._values.get("unix_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeExportPolicyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeExportPolicyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeExportPolicyRuleList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5605da7952ef5419b2327b7ca2c681eacd2178cff9516c0c8e6ed9024d8a916)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetappVolumeExportPolicyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982c45a89496e3e9f94dd54566e220dfc8429e628d059f4c4cd9e189cde421dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeExportPolicyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab0f9741e8ea89cd820ca3b76e794d29c9cd22bd5aea5013b8a3f3c760faf1c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e9f101cf917aad3bf88c6d12c2177260ae5bcbeab7a04cc5c001b4cf567656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754d8d94a6d001f3c2190ab6bf90e0920a0dd80dead096fc21915679fd6d77da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeExportPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeExportPolicyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeExportPolicyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8254d7db65678a3574d67b4f0b33ae0d9f4b571ab76b619543238a4280ea0a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetappVolumeExportPolicyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeExportPolicyRuleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7011c1bafe03a36f8cb17b2ff8b283a1f2a3bc36e578754a3d55c9c2af8bf51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetProtocolsEnabled")
    def reset_protocols_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolsEnabled", []))

    @jsii.member(jsii_name="resetRootAccessEnabled")
    def reset_root_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootAccessEnabled", []))

    @jsii.member(jsii_name="resetUnixReadOnly")
    def reset_unix_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnixReadOnly", []))

    @jsii.member(jsii_name="resetUnixReadWrite")
    def reset_unix_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnixReadWrite", []))

    @builtins.property
    @jsii.member(jsii_name="allowedClientsInput")
    def allowed_clients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedClientsInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsEnabledInput")
    def protocols_enabled_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="rootAccessEnabledInput")
    def root_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rootAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleIndexInput")
    def rule_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="unixReadOnlyInput")
    def unix_read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "unixReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="unixReadWriteInput")
    def unix_read_write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "unixReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedClients")
    def allowed_clients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedClients"))

    @allowed_clients.setter
    def allowed_clients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c2a5bb93f0ddd5ed91ce76a900e496e0a7eddb4b3bdcfed86bd0dc59032e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedClients", value)

    @builtins.property
    @jsii.member(jsii_name="protocolsEnabled")
    def protocols_enabled(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocolsEnabled"))

    @protocols_enabled.setter
    def protocols_enabled(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6f0bdaa682aec681d9871bcd99abc3dd63b3f64f04bf92b38df102f3174d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="rootAccessEnabled")
    def root_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rootAccessEnabled"))

    @root_access_enabled.setter
    def root_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2698c1b3cebb3716dba70f6c785c68e4353c4c1ce676d0955fa9f21a1e1125e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootAccessEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="ruleIndex")
    def rule_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleIndex"))

    @rule_index.setter
    def rule_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4a51fa8f260dfcb5f572be02228efb461221c002783be51b11b65d5c326109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleIndex", value)

    @builtins.property
    @jsii.member(jsii_name="unixReadOnly")
    def unix_read_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "unixReadOnly"))

    @unix_read_only.setter
    def unix_read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73d1ba87e6989d8a102b271c2ac8973abdfb424872e4f817429c9bd79e4e429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unixReadOnly", value)

    @builtins.property
    @jsii.member(jsii_name="unixReadWrite")
    def unix_read_write(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "unixReadWrite"))

    @unix_read_write.setter
    def unix_read_write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498a0c75d28fc26e17c1b23b855e68486b6c4581325de8acbca604ec45ea136d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unixReadWrite", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NetappVolumeExportPolicyRule, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NetappVolumeExportPolicyRule, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NetappVolumeExportPolicyRule, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d098bb8a03254ec32a8044ecbd0a6824f646f8adbcabc934f0f0560948eb3449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class NetappVolumeTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#create NetappVolume#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#delete NetappVolume#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#read NetappVolume#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#update NetappVolume#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdfcec1901ee2f86062876fccdc590b8fadf7cdf41ae21f9132ed60f679e5fad)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#create NetappVolume#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#delete NetappVolume#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#read NetappVolume#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/netapp_volume#update NetappVolume#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolume.NetappVolumeTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46d696574c021e958baf1fdbefd80b058de9b48291d99d6b089893f245458ea2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9a5c011a803c28c9afd6982278d75bc0ee37c4eba62a58babcb1638c29ff3f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ec587ee22f37e8fc5dc1be5d3765a89a43c68ca383e37217e39c024b70ae4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5eca9598ed409d772d368e89e0a4c8b8d64f5af66f9265c28180feb533e762a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5248693f35fed02ad53ac19719ccf855f76049c53df796f003c3f2a4dac1c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NetappVolumeTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NetappVolumeTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NetappVolumeTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28a83a777e1e7cbc899d99daefebcd40e487356ba4d18dcd9a183a085d62a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NetappVolume",
    "NetappVolumeConfig",
    "NetappVolumeDataProtectionReplication",
    "NetappVolumeDataProtectionReplicationOutputReference",
    "NetappVolumeDataProtectionSnapshotPolicy",
    "NetappVolumeDataProtectionSnapshotPolicyOutputReference",
    "NetappVolumeExportPolicyRule",
    "NetappVolumeExportPolicyRuleList",
    "NetappVolumeExportPolicyRuleOutputReference",
    "NetappVolumeTimeouts",
    "NetappVolumeTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__980f8f0ee2b8dcb347c2afa0fa8f444b0148698c9264e6f6fba3dccea919aaab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_name: builtins.str,
    location: builtins.str,
    name: builtins.str,
    pool_name: builtins.str,
    resource_group_name: builtins.str,
    service_level: builtins.str,
    storage_quota_in_gb: jsii.Number,
    subnet_id: builtins.str,
    volume_path: builtins.str,
    azure_vmware_data_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_from_snapshot_resource_id: typing.Optional[builtins.str] = None,
    data_protection_replication: typing.Optional[typing.Union[NetappVolumeDataProtectionReplication, typing.Dict[builtins.str, typing.Any]]] = None,
    data_protection_snapshot_policy: typing.Optional[typing.Union[NetappVolumeDataProtectionSnapshotPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    export_policy_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    network_features: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_style: typing.Optional[builtins.str] = None,
    snapshot_directory_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    throughput_in_mibps: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3be3ef25b86d53ef43a7979775dd8bd2b195716efeda32e595898fb138652b7d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44d14a47300c2bb82f1cd4ea6c0776ec7893cea50b74e2098900a0d57a19031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a63e4f82caf618c8c66b6bd2ab0cfa9ebdaec7cf0ea419f104127adeeb23dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b42eede59cbed32ed556d8245ed6267df09c0b3c7ffbd7456eda12dd7070a3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7765a6c7343b4c8095511ee246a5d0855a110569eaf2799c49bc654639a90f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8192c0e3d5f35a560e076efa9469e152886dc55773b4a9e3942a49739ea219e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5e80f71ae17c74d529f5eaf794b437dd777ba02f4e3f4d1babf6addfd67e703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bc321f6c49a4d8ccc3a8d79ab22ddc823c51ae24afe6eafbd568290564708d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b38032e1cf966eb4d4b207fb26c347bd2ec369efd5449d6e7c3fde19c2953c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0526d73dc8f9adbc2a588c698f8656cf84543b1c5dbde8ac3402cd5723ff7417(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e415f25b0db852cdd09704980cbd5d2919fa632784ae5cdc01d6d02b9edfe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1a88aa3c2ffff97bd53fe11756c7955ccae68470109d0dcee37028a3c277d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd687d5fbbbe5d54e57f89c91eb4ac0f648bc0fdc8c97828b14d5b9e6fcae2e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6574d299e197324fb61f41f397466a0609dcdf65506ad76ea2b4137f8d151083(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc4a1e9db20465458b1c4823d93994f8936be704bba4642930f780e5addb7c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66692039a526452bb25e4d1dd7f928730fd9447321124a2387ff668291b872a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e133b35d0e32a9b79a33936d5d445151bcefbe5ca171c3dd64c0679831da3b0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2aa1303618b907c0133f3ab8ca076db1882600d5adac1729b1347ccab10662(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fdaea5d1356fd0c281b90cd0f152e7be7c42ca97e559fbee179d0209dbf70df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42bf1b4137fa695051e34d876b82ba1419b2d79b46a55e4ae5a1f2f973c01f9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_name: builtins.str,
    location: builtins.str,
    name: builtins.str,
    pool_name: builtins.str,
    resource_group_name: builtins.str,
    service_level: builtins.str,
    storage_quota_in_gb: jsii.Number,
    subnet_id: builtins.str,
    volume_path: builtins.str,
    azure_vmware_data_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    create_from_snapshot_resource_id: typing.Optional[builtins.str] = None,
    data_protection_replication: typing.Optional[typing.Union[NetappVolumeDataProtectionReplication, typing.Dict[builtins.str, typing.Any]]] = None,
    data_protection_snapshot_policy: typing.Optional[typing.Union[NetappVolumeDataProtectionSnapshotPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    export_policy_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    network_features: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_style: typing.Optional[builtins.str] = None,
    snapshot_directory_visible: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    throughput_in_mibps: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c3b0072417db6c0e396f5bf407d1e47b7cd5effb877114c52693cf5c568bf6(
    *,
    remote_volume_location: builtins.str,
    remote_volume_resource_id: builtins.str,
    replication_frequency: builtins.str,
    endpoint_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d658831a27e29a0729169e9ab0761cbc61c9b11084520f15330205605bbdad4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2faf0355dcc5198eef90a4b7d0572319e68be812bedbf31b6ca5e86eae27a3b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7309a1ed7bdf1d5df315b65ee3091f5f4eed61babc93f404bd28aa8db1afb638(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f766e5ac6cf9ba6e11fe72a301538e1210a4324d8a9a131392b54f279e5c10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e86618a5838cfc78eb61b02c4f8bba56f2da7639a90ae64a93d5017c9e5e30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef1fd26d945762c39f1c8a768e28638af148c68f423c8e2852bca2979328bdc(
    value: typing.Optional[NetappVolumeDataProtectionReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee13f7ba943bbcb7dc6a3c98dbb0f2cb199a0f41a23ce1f7499686ebd777cc7(
    *,
    snapshot_policy_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835caed9cc66c88695cb77bff5366eee945dcfb30d16bb3687e37daa130e4323(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bb511c89f7a396d2c35849a6d8908b0ba6367ad53880927c0807ce823ff28b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a919e095942fc04932c9251b6adb71b610fdb99e058493c4bff891f2d4389cdc(
    value: typing.Optional[NetappVolumeDataProtectionSnapshotPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c4c56163cc4aeec6c0bde58cff05aeed8fe4d2203bdb81ec0db6952f9829da(
    *,
    allowed_clients: typing.Sequence[builtins.str],
    rule_index: jsii.Number,
    protocols_enabled: typing.Optional[typing.Sequence[builtins.str]] = None,
    root_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unix_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unix_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5605da7952ef5419b2327b7ca2c681eacd2178cff9516c0c8e6ed9024d8a916(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982c45a89496e3e9f94dd54566e220dfc8429e628d059f4c4cd9e189cde421dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0f9741e8ea89cd820ca3b76e794d29c9cd22bd5aea5013b8a3f3c760faf1c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e9f101cf917aad3bf88c6d12c2177260ae5bcbeab7a04cc5c001b4cf567656(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754d8d94a6d001f3c2190ab6bf90e0920a0dd80dead096fc21915679fd6d77da(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8254d7db65678a3574d67b4f0b33ae0d9f4b571ab76b619543238a4280ea0a6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeExportPolicyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7011c1bafe03a36f8cb17b2ff8b283a1f2a3bc36e578754a3d55c9c2af8bf51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c2a5bb93f0ddd5ed91ce76a900e496e0a7eddb4b3bdcfed86bd0dc59032e7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6f0bdaa682aec681d9871bcd99abc3dd63b3f64f04bf92b38df102f3174d48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2698c1b3cebb3716dba70f6c785c68e4353c4c1ce676d0955fa9f21a1e1125e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4a51fa8f260dfcb5f572be02228efb461221c002783be51b11b65d5c326109(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73d1ba87e6989d8a102b271c2ac8973abdfb424872e4f817429c9bd79e4e429(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498a0c75d28fc26e17c1b23b855e68486b6c4581325de8acbca604ec45ea136d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d098bb8a03254ec32a8044ecbd0a6824f646f8adbcabc934f0f0560948eb3449(
    value: typing.Optional[typing.Union[NetappVolumeExportPolicyRule, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdfcec1901ee2f86062876fccdc590b8fadf7cdf41ae21f9132ed60f679e5fad(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d696574c021e958baf1fdbefd80b058de9b48291d99d6b089893f245458ea2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a5c011a803c28c9afd6982278d75bc0ee37c4eba62a58babcb1638c29ff3f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ec587ee22f37e8fc5dc1be5d3765a89a43c68ca383e37217e39c024b70ae4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5eca9598ed409d772d368e89e0a4c8b8d64f5af66f9265c28180feb533e762a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5248693f35fed02ad53ac19719ccf855f76049c53df796f003c3f2a4dac1c09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28a83a777e1e7cbc899d99daefebcd40e487356ba4d18dcd9a183a085d62a5d(
    value: typing.Optional[typing.Union[NetappVolumeTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
