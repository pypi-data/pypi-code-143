# _*_coding:utf-8_*_

from django.db.models import F
from ..models import Flow, FlowNode, FlowAction, FlowNodeToAction, FlowNodeActionRule, FlowActionToOperator
from ..utils.j_dict import JDict


class FlowBasicService:

    @staticmethod
    def get_flow_list(category_id=None, flow_name=None):
        """
        获取流程列表
        @param category_id 类别ID
        @param flow_name 流程名称
        """

        flow_set = Flow.objects.all()
        if category_id:
            flow_set = flow_set.filter(category_id=category_id)
        if flow_name:
            flow_set = flow_set.filter(flow_name__contains=flow_name)
        # print("flow_set:", flow_set)

        return list(flow_set.values()), None

    @staticmethod
    def get_flow_node_list(flow_id=None):
        """
        获取流程节点列表
        @param flow_id 流程ID
        """

        flow_node_set = FlowNode.objects.all()
        if flow_id:
            flow_node_set = flow_node_set.filter(flow_id=flow_id)
        # print("flow_node_set:", flow_node_set)
        flow_node_list = list(flow_node_set.values(
            "id",
            "flow_id",
            "node_name",
            "module_name",
            "flow_number",
            "summary",
            "description",
        ))

        return flow_node_list, None

    @staticmethod
    def get_flow_action_list(flow_id=None, flow_node_id=None, user_id=None, role_id=None):
        """
        获取流程动作列表
        @param flow_id 流程ID
        @param flow_node_id 流程节点ID
        @param user_id 用户ID
        @param role_id 角色ID
        """

        # 如果不传绑定参数则表示返回所有的动作列表
        if not flow_id and not flow_node_id and not user_id and not role_id:
            action_set = FlowAction.objects.all()
            action_list = list(action_set.values(
                "id",
                "action",
                "name",
                "description",
                "config",
            ))
            return action_list, None

        # 如果按节点则查询当前可以进行的动作
        node_to_action_set = FlowNodeToAction.objects.all()
        if flow_id:
            node_to_action_set = node_to_action_set.filter(flow_node_id__flow_id=flow_id)
        if flow_node_id:
            node_to_action_set = node_to_action_set.filter(flow_node_id=flow_node_id)
        # print("node_to_action_set:", node_to_action_set)

        if user_id or role_id:
            operator_set = FlowActionToOperator.objects.all()
            if user_id:
                operator_set = operator_set.filter(user_id=user_id)
            if role_id:
                operator_set = operator_set.filter(role_id=role_id)
            # print("operator_set:", operator_set)
            operator_action_id_list = [it.flow_action_id for it in operator_set]
            # 如果没有找到操作人，就不应该也不能再往下匹配了，直接返回空列表
            if not operator_action_id_list:
                return [], None
            node_to_action_set = node_to_action_set.filter(flow_action_id__in=operator_action_id_list)
            # print("node_to_action_set 4:", node_to_action_set)

        node_to_action_set = node_to_action_set.annotate(flow_node_to_action_id=F('id'))\
            .annotate(action=F('flow_action_id__action'))\
            .annotate(name=F('flow_action_id__name'))\
            .annotate(description=F('flow_action_id__description'))\
            .annotate(config=F('flow_action_id__config'))
        node_to_action_list = list(node_to_action_set.values(
            "flow_node_to_action_id",
            "flow_action_id",
            "action",
            "name",
            "description",
            "config",
        ))
        # 因为当前接口是动作接口，所以返回的ID也应该是动作ID
        for i, it in enumerate(node_to_action_list):
            it['id'] = it.get('flow_action_id')

        return node_to_action_list, None

    @staticmethod
    def get_flow_node_to_action_list(flow_id=None):
        """
        获取流程动作列表
        @param flow_id 流程ID
        """

        result_set = FlowNodeToAction.objects.all()
        if flow_id:
            result_set = result_set.filter(flow_node_id__flow_id=flow_id)
        # print("get_flow_node_to_action_list:", result_set)
        result_set = result_set.annotate(flow_node_name=F('flow_node_id__node_name'))\
            .annotate(flow_action=F('flow_action_id__action'))\
            .annotate(flow_action_name=F('flow_action_id__name'))\
            .annotate(flow_to_node_name=F('flow_to_node_id__node_name'))
        result_list = list(result_set.values(
            "id",
            "flow_node_id",
            "flow_action_id",
            "flow_to_node_id",
            "flow_node_name",
            "flow_action",
            "flow_action_name",
            "flow_to_node_name",
        ))

        return result_list, None

    @staticmethod
    def get_flow_node_action_rule_list(flow_id=None, flow_node_id=None):
        """
        获取流程节点动作规则列表
        @param flow_id 流程ID
        @param flow_node_id 流程规则ID
        """

        result_set = FlowNodeActionRule.objects.all()
        if flow_id:
            result_set = result_set.filter(flow_node_to_action_id__flow_node_id__flow_id=flow_id)
        if flow_node_id:
            result_set = result_set.filter(flow_node_to_action_id__flow_node_id=flow_node_id)
        # print("rule_set:", rule_set)
        result_set = result_set.annotate(flow_id=F('flow_node_to_action_id__flow_node_id__flow_id'))\
            .annotate(flow_node_id=F('flow_node_to_action_id__flow_node_id'))\
            .annotate(flow_action_id=F('flow_node_to_action_id__flow_action_id'))
        result_list = list(result_set.values(
            "id",
            "flow_id",
            "flow_node_id",
            "flow_action_id",
            "rule_name",
            "rule_sort",
            "inflow_service",
            "inflow_module",
            "inflow_field",
            "outflow_module",
            "outflow_field",
            "default_value",
            "expression_string",
            "python_script",
        ))

        return result_list, None
