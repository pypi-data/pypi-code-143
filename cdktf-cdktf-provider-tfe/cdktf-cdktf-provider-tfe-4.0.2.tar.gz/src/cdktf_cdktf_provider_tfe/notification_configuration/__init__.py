'''
# `tfe_notification_configuration`

Refer to the Terraform Registory for docs: [`tfe_notification_configuration`](https://www.terraform.io/docs/providers/tfe/r/notification_configuration).
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


class NotificationConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tfe.notificationConfiguration.NotificationConfiguration",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration tfe_notification_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        destination_type: builtins.str,
        name: builtins.str,
        workspace_id: builtins.str,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration tfe_notification_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param destination_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#destination_type NotificationConfiguration#destination_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#name NotificationConfiguration#name}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#workspace_id NotificationConfiguration#workspace_id}.
        :param email_addresses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_addresses NotificationConfiguration#email_addresses}.
        :param email_user_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_user_ids NotificationConfiguration#email_user_ids}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#enabled NotificationConfiguration#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#id NotificationConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#token NotificationConfiguration#token}.
        :param triggers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#triggers NotificationConfiguration#triggers}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#url NotificationConfiguration#url}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc917ccedf3e195f7f6d9417588d6fee77906cf9f67983f530cfc0430466233)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NotificationConfigurationConfig(
            destination_type=destination_type,
            name=name,
            workspace_id=workspace_id,
            email_addresses=email_addresses,
            email_user_ids=email_user_ids,
            enabled=enabled,
            id=id,
            token=token,
            triggers=triggers,
            url=url,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetEmailAddresses")
    def reset_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddresses", []))

    @jsii.member(jsii_name="resetEmailUserIds")
    def reset_email_user_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailUserIds", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetToken")
    def reset_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToken", []))

    @jsii.member(jsii_name="resetTriggers")
    def reset_triggers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggers", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="destinationTypeInput")
    def destination_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="emailUserIdsInput")
    def email_user_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailUserIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenInput")
    def token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenInput"))

    @builtins.property
    @jsii.member(jsii_name="triggersInput")
    def triggers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggersInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationType")
    def destination_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "destinationType"))

    @destination_type.setter
    def destination_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f57ce5ffdedcb0cc6b0aff33373b92985d5feff18dc800d91558af00b8930e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationType", value)

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598906221a4b6a4c9a2ffc4f7918741d2bb929d7524b8855ff7b41464c70a336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="emailUserIds")
    def email_user_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailUserIds"))

    @email_user_ids.setter
    def email_user_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e49d4bffbfefd14747af98828b4867dc35aa545a8ef25895da8956faa9471c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailUserIds", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363397a388a63916a0957eac8c085d298677eb5d31bf28649bd8993f08b5b498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb8512f48a6ad73c6e862d21203a2b9281f1e3658d019c5b5e3c2b31d902484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5032617de01086e0df4b5b50018e4f68e9d49ebfd17e4eaf64e081c88f66d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @token.setter
    def token(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e7ad4a4b1c6d43d3798049863a14483b7285c69253b113da8a7fc7ed2645fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "token", value)

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggers"))

    @triggers.setter
    def triggers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c972cf2948d0fac9f97ce0c813ba20856ca7f170118b6725e59e02cb266424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggers", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f8c8d4f20ce6a3ce4263794a057db4e4235ff2ea51cc855fc9782091da306e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b40f1f268e17fd233e57fe94c2c23edb49af46e51545f5ef36b47e0d552048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tfe.notificationConfiguration.NotificationConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "destination_type": "destinationType",
        "name": "name",
        "workspace_id": "workspaceId",
        "email_addresses": "emailAddresses",
        "email_user_ids": "emailUserIds",
        "enabled": "enabled",
        "id": "id",
        "token": "token",
        "triggers": "triggers",
        "url": "url",
    },
)
class NotificationConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        destination_type: builtins.str,
        name: builtins.str,
        workspace_id: builtins.str,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param destination_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#destination_type NotificationConfiguration#destination_type}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#name NotificationConfiguration#name}.
        :param workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#workspace_id NotificationConfiguration#workspace_id}.
        :param email_addresses: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_addresses NotificationConfiguration#email_addresses}.
        :param email_user_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_user_ids NotificationConfiguration#email_user_ids}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#enabled NotificationConfiguration#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#id NotificationConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param token: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#token NotificationConfiguration#token}.
        :param triggers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#triggers NotificationConfiguration#triggers}.
        :param url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#url NotificationConfiguration#url}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf60f4f2785c2ba3015ff934a101f122826a3e0bb648979f71afdde2cff691c4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
            check_type(argname="argument email_user_ids", value=email_user_ids, expected_type=type_hints["email_user_ids"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument triggers", value=triggers, expected_type=type_hints["triggers"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_type": destination_type,
            "name": name,
            "workspace_id": workspace_id,
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
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if email_user_ids is not None:
            self._values["email_user_ids"] = email_user_ids
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if token is not None:
            self._values["token"] = token
        if triggers is not None:
            self._values["triggers"] = triggers
        if url is not None:
            self._values["url"] = url

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
    def destination_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#destination_type NotificationConfiguration#destination_type}.'''
        result = self._values.get("destination_type")
        assert result is not None, "Required property 'destination_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#name NotificationConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#workspace_id NotificationConfiguration#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_addresses NotificationConfiguration#email_addresses}.'''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_user_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#email_user_ids NotificationConfiguration#email_user_ids}.'''
        result = self._values.get("email_user_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#enabled NotificationConfiguration#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#id NotificationConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#token NotificationConfiguration#token}.'''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def triggers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#triggers NotificationConfiguration#triggers}.'''
        result = self._values.get("triggers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/tfe/r/notification_configuration#url NotificationConfiguration#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NotificationConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NotificationConfiguration",
    "NotificationConfigurationConfig",
]

publication.publish()

def _typecheckingstub__fbc917ccedf3e195f7f6d9417588d6fee77906cf9f67983f530cfc0430466233(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    destination_type: builtins.str,
    name: builtins.str,
    workspace_id: builtins.str,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3f57ce5ffdedcb0cc6b0aff33373b92985d5feff18dc800d91558af00b8930e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598906221a4b6a4c9a2ffc4f7918741d2bb929d7524b8855ff7b41464c70a336(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e49d4bffbfefd14747af98828b4867dc35aa545a8ef25895da8956faa9471c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363397a388a63916a0957eac8c085d298677eb5d31bf28649bd8993f08b5b498(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb8512f48a6ad73c6e862d21203a2b9281f1e3658d019c5b5e3c2b31d902484(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5032617de01086e0df4b5b50018e4f68e9d49ebfd17e4eaf64e081c88f66d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e7ad4a4b1c6d43d3798049863a14483b7285c69253b113da8a7fc7ed2645fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c972cf2948d0fac9f97ce0c813ba20856ca7f170118b6725e59e02cb266424(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f8c8d4f20ce6a3ce4263794a057db4e4235ff2ea51cc855fc9782091da306e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b40f1f268e17fd233e57fe94c2c23edb49af46e51545f5ef36b47e0d552048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf60f4f2785c2ba3015ff934a101f122826a3e0bb648979f71afdde2cff691c4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    destination_type: builtins.str,
    name: builtins.str,
    workspace_id: builtins.str,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_user_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
