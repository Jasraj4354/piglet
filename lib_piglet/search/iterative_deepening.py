# search/iterative deeping.py
#
#
# @author: dharabor
# @created: 2020-07-16
#

from lib_piglet.search.base_search import base_search
from lib_piglet.search.tree_search import tree_search
from lib_piglet.search.search_node import search_node
from lib_piglet.expanders.base_expander import base_expander
from enum import IntEnum
import time, sys


class ID_threshold(IntEnum):
    depth = 1
    cost = 2


class iterative_deepening(base_search):
    def __init__(
        self,
        open_list,
        expander: base_expander,
        heuristic_function=None,
        time_limit: int = sys.maxsize,
    ):
        super(iterative_deepening, self).__init__(
            open_list, expander, heuristic_function, time_limit
        )
        self.tree_search_engine: tree_search = tree_search(
            open_list, expander, heuristic_function, time_limit
        )

    # Search the path between two state
    # @param start_state The start of the path
    # @param goal_state Then goal of the path
    # @return solution Contains a list of locations between start and goal
    def get_path(self, start_state, goal_state, threshold_type=ID_threshold.depth):
        self.tree_search_engine.listener_ = self.listener_
        self.open_list_.clear()
        self.reset_statistic()
        self.start_ = start_state
        self.goal_ = goal_state
        self.start_time = time.process_time()
        start_node = self.generate(start_state, None, None)

        # depth_threshold = start_node.depth_
        # changed lines
        if threshold_type == ID_threshold.depth:
            threshold = start_node.depth_
        else:
            threshold = start_node.g_

        # Keep search until reach timelimit.
        while self.runtime_ < self.time_limit_:
            # Set time limit to DLS
            self.tree_search_engine.time_limit_ = self.time_limit_ - self.runtime_

            if threshold_type == ID_threshold.depth:
                name = f"depth-{threshold}"
                solution, next_d, next_f = self.tree_search_engine.get_path(
                    self.start_, self.goal_, depth_limit=threshold
                )
            else:
                name = f"cost-{threshold}"
                solution, next_d, next_f = self.tree_search_engine.get_path(
                    self.start_, self.goal_, cost_limit=threshold
                )

            # Update statistic info
            self.nodes_generated_ += self.tree_search_engine.nodes_generated_
            self.nodes_expanded_ += self.tree_search_engine.nodes_expanded_
            self.runtime_ = time.process_time() - self.start_time

            if solution is None:
                if threshold_type == ID_threshold.depth:
                    if next_d == sys.maxsize:
                        self.solution_ = None
                        self.status_ = "Failed"
                        return None
                    threshold = next_d
                else:
                    if next_f == sys.maxsize:
                        self.solution_ = None
                        self.status_ = "Failed"
                        return None
                    threshold = next_f
            else:
                self.solution_ = solution
                self.status_ = "Success"
                return self.solution_

        # OPEN list is exhausted and we did not find the goal
        # return failure instead of a solution
        self.runtime_ = time.process_time() - self.start_time
        self.status_ = "Time out"
        self.solution_ = None
        return None
