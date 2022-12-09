# coding=utf-8
from django.db import models
from django.utils import timezone

module_choices = [
    ('USER', '用户(USER)'),
    ('THREAD', '信息(THREAD)'),
    ('COMMENT', '评论(COMMENT)'),
    ('FINANCE', '资金(FINANCE)'),
    ('ENROLL', '报名(ENROLL)'),
    ('RESOURCE', '资源(RESOURCE)'),
    ('DICTIONARY', '字典(DICTIONARY)'),
    ('PAYMENT', '支付(PAYMENT)'),
    ('ROLE', '角色(ROLE)'),
]


class Flow(models.Model):
    """ 流程表 """

    class Meta:
        db_table = u'flow_flow'
        verbose_name = '1.流程主表'
        verbose_name_plural = verbose_name

    category_id = models.IntegerField(verbose_name='类别ID', blank=True, null=True, help_text='')
    flow_name = models.CharField(verbose_name='流程名称', max_length=255, db_index=True, help_text='必填')
    module_name = models.CharField(verbose_name='模块名称', max_length=32, db_index=True, blank=True, null=True,
                                   choices=module_choices, help_text='')
    description = models.CharField(verbose_name='流程描述', max_length=255, blank=True, null=True, help_text='')

    def __str__(self):
        return self.flow_name


class FlowNode(models.Model):
    """
    流程节点表
    @note 注意：时态为进行时，节点表是记录当前节点发生的动作。
    """

    class Meta:
        db_table = u'flow_node'
        verbose_name = '2.流程节点表'
        verbose_name_plural = verbose_name

    flow_id = models.ForeignKey(Flow, verbose_name='流程ID', db_column='flow_id', on_delete=models.DO_NOTHING,
                                help_text='')
    node_name = models.CharField(verbose_name='节点名称', max_length=255, blank=True, null=True, help_text='节点名称建议使用下一流程状态命名。例如：已付款的下一状态是接单，则写待接单')
    module_name = models.CharField(verbose_name='模块名称', max_length=32, db_index=True, blank=True, null=True, choices=module_choices, help_text='')
    flow_number = models.IntegerField(verbose_name='流程号', db_index=True, blank=True, null=True, help_text='')
    status_code = models.IntegerField(verbose_name='状态码', db_index=True, blank=True, null=True, help_text='订单状态表示法：0完成、1 留空或非、2下单、3接单、4付款、5发货、6收货、7退货、8评价、9冗余')
    # true_flow_to = models.ForeignKey(to='self', verbose_name='真值流向号', db_column='true_flow_to', related_name='+', blank=True, null=True, on_delete=models.DO_NOTHING, db_constraint=False, help_text='')
    # false_flow_to = models.ForeignKey(to='self', verbose_name='假值流向号', db_column='false_flow_to', related_name='+', blank=True, null=True, on_delete=models.DO_NOTHING, db_constraint=False, help_text='')
    # flow_flag = models.IntegerField(verbose_name='流向符号', db_index=True, blank=True, null=True, choices=[(0, '起始'), (1, '正向'), (2, '逆向'), (3, '停止')], help_text='当流程号大于真值流向号时为正向，相等为停止，小于为逆向')
    summary = models.CharField(verbose_name='摘要', max_length=1024, db_index=True, blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='描述', max_length=1024, blank=True, null=True, help_text='')
    # operate_role_id = models.IntegerField(verbose_name='操作角色ID', db_index=True, blank=True, null=True, help_text='允许操作信息的角色ID')
    # has_more_operators = models.BooleanField(verbose_name='有更多操作者', blank=True, null=True, help_text='有则走多对多表')
    many_flow_action_id = models.ManyToManyField(verbose_name='多对多流程动作ID', to='FlowAction', through='FlowNodeToAction',
                                                 through_fields=('flow_node_id', 'flow_action_id'))

    def __str__(self):
        return f"{self.flow_number}. {self.node_name} ({self.flow_id.flow_name})"


class FlowAction(models.Model):
    """ 流程动作表 """

    class Meta:
        db_table = u'flow_action'
        verbose_name = '3.流程动作表'
        verbose_name_plural = verbose_name

    id = models.AutoField(verbose_name='ID', primary_key=True)
    action = models.CharField(verbose_name='动作关键字', max_length=255, unique=True, db_index=True, help_text='必填')
    name = models.CharField(verbose_name='动作名称', max_length=255, blank=True, null=True, help_text='')
    description = models.CharField(verbose_name='动作描述', max_length=255, blank=True, null=True, help_text='')
    config = models.JSONField(verbose_name='前端配置', blank=True, null=True, help_text='')

    def __str__(self):
        return f"{self.action} - {self.name}"


class FlowNodeToAction(models.Model):
    """ 流程节点多对多动作表 """

    class Meta:
        db_table = u'flow_node_to_action'
        verbose_name = '4.流程节点多对多动作表'
        verbose_name_plural = verbose_name
        unique_together = ['flow_node_id', 'flow_action_id', 'flow_to_node_id']

    flow_node_id = models.ForeignKey(FlowNode, verbose_name='流程节点ID', db_column='flow_node_id', on_delete=models.DO_NOTHING, help_text='')
    flow_action_id = models.ForeignKey(FlowAction, verbose_name='流程动作ID', db_column='flow_action_id', on_delete=models.DO_NOTHING, help_text='')
    flow_to_node_id = models.ForeignKey(FlowNode, verbose_name='流向节点ID', db_column='flow_to_node_id', related_name='+', blank=True, null=True, on_delete=models.DO_NOTHING, help_text='')

    def __str__(self):
        return f"{self.flow_node_id.flow_id.flow_name} - {self.flow_node_id.node_name} - {self.flow_action_id.name}"


class FlowActionToOperator(models.Model):
    """ 流程节点多对多操作者表 """

    class Meta:
        db_table = u'flow_action_to_operator'
        verbose_name = '5.流程动作多对多操作人表'
        verbose_name_plural = verbose_name

    flow_action_id = models.ForeignKey(FlowAction, verbose_name='流程动作ID', db_column='flow_action_id', on_delete=models.DO_NOTHING, help_text='')
    role_id = models.IntegerField(verbose_name='操作角色ID', blank=True, null=True, help_text='操作该记录的所属角色(即操作组)')
    user_id = models.BigIntegerField(verbose_name='操作人员ID', blank=True, null=True, help_text='操作该记录的所属用户(即操作人)')

    def __str__(self):
        return f"[{self.flow_action_id}-{self.role_id},{self.user_id}]"


class FlowNodeActionRule(models.Model):
    """ 流程节点规则表 """

    class Meta:
        db_table = 'flow_node_action_rule'
        verbose_name_plural = '6. 流程节点动作规则表'

    service_choices = [
        ('enroll_detail', '报名详细(enroll_detail)'),
        ('thread_detail', '信息详细(thread_detail)'),
        ('payment_detail', '支付详细(payment_detail)'),
    ]

    flow_node_to_action_id = models.ForeignKey(FlowNodeToAction, verbose_name='流程节点动作ID', db_column='flow_node_to_action_id', db_constraint=False, on_delete=models.DO_NOTHING, help_text='')
    rule_name = models.CharField(verbose_name='规则名称', max_length=255, blank=True, null=True, help_text='')
    rule_sort = models.IntegerField(verbose_name='规则顺序', db_index=True, blank=True, null=True, help_text='')
    inflow_service = models.CharField(verbose_name='流入服务', max_length=32, db_index=True, blank=True, null=True,
                                      choices=service_choices, help_text='')
    inflow_module = models.CharField(verbose_name='流入模块', max_length=32, db_index=True, blank=True, null=True, choices=module_choices,
                                     help_text='')
    inflow_field = models.CharField(verbose_name='流入字段', max_length=32, blank=True, null=True, help_text='')
    outflow_module = models.CharField(verbose_name='流出模块', max_length=32, db_index=True, blank=True, null=True, choices=module_choices,
                                      help_text='默认与流入模块相同')
    outflow_field = models.CharField(verbose_name='流出字段', max_length=32, blank=True, null=True,
                                     help_text='默认与流入字段相同。如果流出字段不存在则自动创建')
    default_value = models.CharField(verbose_name='默认值', max_length=255, blank=True, null=True, help_text='')
    expression_string = models.CharField(verbose_name='逻辑表达式', max_length=2048, blank=True, null=True, help_text='')
    python_script = models.TextField(verbose_name='帕森脚本', blank=True, null=True, help_text='')

    def __str__(self):
        return self.rule_name


class FlowRecord(models.Model):
    """ 流程记录表 """

    class Meta:
        db_table = 'flow_record'
        verbose_name_plural = '7. 流程记录表'

    flow_node_id = models.ForeignKey(FlowNode, verbose_name='流程节点ID', db_column='flow_node_id',
                                     on_delete=models.DO_NOTHING,
                                     help_text='')
    user_id = models.BigIntegerField(verbose_name='用户ID', db_index=True, help_text='')
    belong_role_id = models.IntegerField(verbose_name='所属角色ID', blank=True, null=True, help_text='操作该记录的所属角色(即操作人)')
    summary = models.CharField(verbose_name='摘要(自动)', max_length=255, db_index=True, blank=True, null=True,
                               help_text='摘要自动生成。例如：“【张三】检查完成【马云】的“XXX”资料，并信息补充”')

    def __str__(self):
        return self.summary


class FlowNodeLog(models.Model):
    """
    流程节点日志表
    @note 注意：时态为完成时，日志表是对当前节点动作完成的记录日志，不能理解为编辑的记录。
    """

    class Meta:
        db_table = 'flow_node_log'
        verbose_name_plural = '8. 流程节点日志表'

    flow_record_id = models.ForeignKey(FlowRecord, verbose_name='流程节点ID', db_column='flow_record_id',
                                       on_delete=models.DO_NOTHING, help_text='')
    flow_node_id = models.ForeignKey(FlowNode, verbose_name='流程节点ID', db_column='flow_node_id',
                                     on_delete=models.DO_NOTHING, help_text='')
    user_id = models.BigIntegerField(verbose_name='用户ID', db_index=True, help_text='')
    belong_role_id = models.IntegerField(verbose_name='所属角色ID', blank=True, null=True, help_text='操作该日志的所属角色(即操作人)')
    summary = models.CharField(verbose_name='摘要(自动)', max_length=255, db_index=True, blank=True, null=True,
                               help_text='摘要自动生成。例如：“【张三】检查完成【马云】的“XXX”资料，并信息补充”')
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now, help_text='')

    def __str__(self):
        return self.summary
