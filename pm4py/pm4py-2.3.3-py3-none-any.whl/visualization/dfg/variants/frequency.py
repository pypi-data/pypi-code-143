'''
    This file is part of PM4Py (More Info: https://pm4py.fit.fraunhofer.de).

    PM4Py is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PM4Py is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PM4Py.  If not, see <https://www.gnu.org/licenses/>.
'''
import tempfile
from copy import copy

from graphviz import Digraph

from pm4py.statistics.attributes.log import get as attr_get
from pm4py.objects.dfg.utils import dfg_utils
from pm4py.util import xes_constants as xes
from pm4py.visualization.common.utils import *
from pm4py.util import exec_utils
from pm4py.statistics.sojourn_time.log import get as soj_time_get
from enum import Enum
from pm4py.util import constants
from typing import Optional, Dict, Any, Tuple
from pm4py.objects.log.obj import EventLog
from collections import Counter


class Parameters(Enum):
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    FORMAT = "format"
    MAX_NO_EDGES_IN_DIAGRAM = "maxNoOfEdgesInDiagram"
    START_ACTIVITIES = "start_activities"
    END_ACTIVITIES = "end_activities"
    TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_TIMESTAMP_KEY
    START_TIMESTAMP_KEY = constants.PARAMETER_CONSTANT_START_TIMESTAMP_KEY
    FONT_SIZE = "font_size"
    BGCOLOR = "bgcolor"
    STAT_LOCALE = "stat_locale"


def get_min_max_value(dfg):
    """
    Gets min and max value assigned to edges
    in DFG graph

    Parameters
    -----------
    dfg
        Directly follows graph

    Returns
    -----------
    min_value
        Minimum value in directly follows graph
    max_value
        Maximum value in directly follows graph
    """
    min_value = 9999999999
    max_value = -1

    for edge in dfg:
        if dfg[edge] < min_value:
            min_value = dfg[edge]
        if dfg[edge] > max_value:
            max_value = dfg[edge]

    return min_value, max_value


def assign_penwidth_edges(dfg):
    """
    Assign penwidth to edges in directly-follows graph

    Parameters
    -----------
    dfg
        Direcly follows graph

    Returns
    -----------
    penwidth
        Graph penwidth that edges should have in the direcly follows graph
    """
    penwidth = {}
    min_value, max_value = get_min_max_value(dfg)
    for edge in dfg:
        v0 = dfg[edge]
        v1 = get_arc_penwidth(v0, min_value, max_value)
        penwidth[edge] = str(v1)

    return penwidth


def get_activities_color(activities_count):
    """
    Get frequency color for attributes

    Parameters
    -----------
    activities_count
        Count of attributes in the log

    Returns
    -----------
    activities_color
        Color assigned to attributes in the graph
    """
    activities_color = {}

    min_value, max_value = get_min_max_value(activities_count)

    for ac in activities_count:
        v0 = activities_count[ac]
        """transBaseColor = int(
            255 - 100 * (v0 - min_value) / (max_value - min_value + 0.00001))
        transBaseColorHex = str(hex(transBaseColor))[2:].upper()
        v1 = "#" + transBaseColorHex + transBaseColorHex + "FF"""

        v1 = get_trans_freq_color(v0, min_value, max_value)

        activities_color[ac] = v1

    return activities_color


def graphviz_visualization(activities_count, dfg, image_format="png", measure="frequency",
                           max_no_of_edges_in_diagram=100000, start_activities=None, end_activities=None, soj_time=None,
                            font_size="12", bgcolor=constants.DEFAULT_BGCOLOR, stat_locale=None):
    """
    Do GraphViz visualization of a DFG graph

    Parameters
    -----------
    activities_count
        Count of attributes in the log (may include attributes that are not in the DFG graph)
    dfg
        DFG graph
    image_format
        GraphViz should be represented in this format
    measure
        Describes which measure is assigned to edges in direcly follows graph (frequency/performance)
    max_no_of_edges_in_diagram
        Maximum number of edges in the diagram allowed for visualization
    start_activities
        Start activities of the log
    end_activities
        End activities of the log
    soj_time
        For each activity, the sojourn time in the log
    stat_locale
        Dict to locale the stat strings
    
    Returns
    -----------
    viz
        Digraph object
    """
    if start_activities is None:
        start_activities = {}
    if end_activities is None:
        end_activities = {}
    if stat_locale is None:
        stat_locale = {}

    filename = tempfile.NamedTemporaryFile(suffix='.gv')
    viz = Digraph("", filename=filename.name, engine='dot', graph_attr={'bgcolor': bgcolor})

    # first, remove edges in diagram that exceeds the maximum number of edges in the diagram
    dfg_key_value_list = []
    for edge in dfg:
        dfg_key_value_list.append([edge, dfg[edge]])
    # more fine grained sorting to avoid that edges that are below the threshold are
    # undeterministically removed
    dfg_key_value_list = sorted(dfg_key_value_list, key=lambda x: (x[1], x[0][0], x[0][1]), reverse=True)
    dfg_key_value_list = dfg_key_value_list[0:min(len(dfg_key_value_list), max_no_of_edges_in_diagram)]
    dfg_allowed_keys = [x[0] for x in dfg_key_value_list]
    dfg_keys = list(dfg.keys())
    for edge in dfg_keys:
        if edge not in dfg_allowed_keys:
            del dfg[edge]

    # calculate edges penwidth
    penwidth = assign_penwidth_edges(dfg)
    activities_in_dfg = set()
    activities_count_int = copy(activities_count)

    for edge in dfg:
        activities_in_dfg.add(edge[0])
        activities_in_dfg.add(edge[1])

    # assign attributes color
    activities_color = get_activities_color(activities_count_int)

    # represent nodes
    viz.attr('node', shape='box')

    if len(activities_in_dfg) == 0:
        activities_to_include = sorted(list(set(activities_count_int)))
    else:
        # take unique elements as a list not as a set (in this way, nodes are added in the same order to the graph)
        activities_to_include = sorted(list(set(activities_in_dfg)))

    activities_map = {}

    for act in activities_to_include:
        if "frequency" in measure and act in activities_count_int:
            viz.node(str(hash(act)), act + " (" + str(activities_count_int[act]) + ")", style='filled',
                     fillcolor=activities_color[act], fontsize=font_size)
            activities_map[act] = str(hash(act))
        else:
            stat_string = human_readable_stat(soj_time[act], stat_locale)
            viz.node(str(hash(act)), act + f" ({stat_string})", fontsize=font_size)
            activities_map[act] = str(hash(act))

    # make edges addition always in the same order
    dfg_edges = sorted(list(dfg.keys()))

    # represent edges
    for edge in dfg_edges:
        if "frequency" in measure:
            label = str(dfg[edge])
        else:
            label = human_readable_stat(dfg[edge], stat_locale)
        viz.edge(str(hash(edge[0])), str(hash(edge[1])), label=label, penwidth=str(penwidth[edge]), fontsize=font_size)

    start_activities_to_include = [act for act in start_activities if act in activities_map]
    end_activities_to_include = [act for act in end_activities if act in activities_map]

    if start_activities_to_include:
        viz.node("@@startnode", "<&#9679;>", shape='circle', fontsize="34")
        for act in start_activities_to_include:
            label = str(start_activities[act]) if isinstance(start_activities, dict) else ""
            viz.edge("@@startnode", activities_map[act], label=label, fontsize=font_size)

    if end_activities_to_include:
        # <&#9632;>
        viz.node("@@endnode", "<&#9632;>", shape='doublecircle', fontsize="32")
        for act in end_activities_to_include:
            label = str(end_activities[act]) if isinstance(end_activities, dict) else ""
            viz.edge(activities_map[act], "@@endnode", label=label, fontsize=font_size)

    viz.attr(overlap='false')

    viz.format = image_format

    return viz


def apply(dfg: Dict[Tuple[str, str], int], log: EventLog = None, parameters: Optional[Dict[Any, Any]] = None, activities_count : Dict[str, int] = None, soj_time: Dict[str, float] = None) -> Digraph:
    """
    Visualize a frequency directly-follows graph

    Parameters
    -----------------
    dfg
        Frequency Directly-follows graph
    log
        (if provided) Event log for the calculation of statistics
    activities_count
        (if provided) Dictionary associating to each activity the number of occurrences in the log.
    soj_time
        (if provided) Dictionary associating to each activity the average sojourn time
    parameters
        Variant-specific parameters

    Returns
    -----------------
    gviz
        Graphviz digraph
    """
    if parameters is None:
        parameters = {}

    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, xes.DEFAULT_NAME_KEY)
    image_format = exec_utils.get_param_value(Parameters.FORMAT, parameters, "png")
    max_no_of_edges_in_diagram = exec_utils.get_param_value(Parameters.MAX_NO_EDGES_IN_DIAGRAM, parameters, 100000)
    start_activities = exec_utils.get_param_value(Parameters.START_ACTIVITIES, parameters, {})
    end_activities = exec_utils.get_param_value(Parameters.END_ACTIVITIES, parameters, {})
    font_size = exec_utils.get_param_value(Parameters.FONT_SIZE, parameters, 12)
    font_size = str(font_size)
    activities = dfg_utils.get_activities_from_dfg(dfg)
    bgcolor = exec_utils.get_param_value(Parameters.BGCOLOR, parameters, constants.DEFAULT_BGCOLOR)
    stat_locale = exec_utils.get_param_value(Parameters.STAT_LOCALE, parameters, {})

    if activities_count is None:
        if log is not None:
            activities_count = attr_get.get_attribute_values(log, activity_key, parameters=parameters)
        else:
            # the frequency of an activity in the log is at least the number of occurrences of
            # incoming arcs in the DFG.
            # if the frequency of the start activities nodes is also provided, use also that.
            activities_count = Counter({key: 0 for key in activities})
            for el in dfg:
                activities_count[el[1]] += dfg[el]
            if isinstance(start_activities, dict):
                for act in start_activities:
                    activities_count[act] += start_activities[act]

    if soj_time is None:
        if log is not None:
            soj_time = soj_time_get.apply(log, parameters=parameters)
        else:
            soj_time = {key: 0 for key in activities}

    return graphviz_visualization(activities_count, dfg, image_format=image_format, measure="frequency",
                                  max_no_of_edges_in_diagram=max_no_of_edges_in_diagram,
                                  start_activities=start_activities, end_activities=end_activities, 
                                  soj_time=soj_time, font_size=font_size, bgcolor=bgcolor, stat_locale=stat_locale)
