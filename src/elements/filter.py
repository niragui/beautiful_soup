from typing import Callable, Union, Optional, Dict

from .node import Node

import warnings


FILTER_TYPE = Union[str, Callable[[str], bool]]
AGGS_FILTER_TYPE = Union[str, Callable[[Dict[str, str]], bool]]
OTHER_FILTER_TYPE = Callable[[Node], bool]


def check_filter_type(filter,
                      could_str: bool):
    """
    Check if the filter type is valid

    Parameters:
        - filter: Filter to check if valid
        - could_str: Bool indicating if it can be a string
    """
    if filter is None:
        return

    if isinstance(filter, str) and could_str:
        return

    if callable(filter):
        return

    raise TypeError(f"Invalid Filter [{filter}]")


class NodeFilter():
    def __init__(self,
                 name: Optional[FILTER_TYPE] = None,
                 text: Optional[FILTER_TYPE] = None,
                 attributes: Optional[AGGS_FILTER_TYPE] = None,
                 others: Optional[OTHER_FILTER_TYPE] = None):
        check_filter_type(name, True)
        check_filter_type(text, True)
        check_filter_type(attributes, False)
        check_filter_type(others, False)

        self.name = name
        self.text = text
        self.attrs = attributes
        self.others = others

    def match_field(self,
                    node: Node,
                    filter_field: str):
        """
        Check if the node matches the asked filter

        Parameters:
            - node: Node to check
            - filter_field: Field to check for filter
        """
        if not hasattr(self, filter_field):
            raise KeyError(f"Can't Check For Non Existing Filter [{filter_field}]")

        filter = getattr(self, filter_field)
        if filter is None:
            return True

        if not hasattr(node, filter_field):
            return False

        node_value = getattr(node, filter_field)

        if isinstance(filter, str):
            return node_value == filter

        if callable(filter):
            return filter(node_value)

        warnings.warn(f"{filter_field.title()} Filter Has Unknwon Format")
        return False

    def match_name(self,
                   node: Node):
        """
        Check if the node matches the name filter

        Parameters:
            - node: Node to check
        """
        return self.match_field(node, "name")

    def match_text(self,
                   node: Node):
        """
        Check if the node matches the text filter

        Parameters:
            - node: Node to check
        """
        return self.match_field(node, "text")

    def match_attributes(self,
                         node: Node):
        """
        Check if the node matches the attributes filter

        Parameters:
            - node: Node to check
        """
        return self.match_field(node, "attrs")

    def match(self,
              node: Node):
        """
        Check if the node matches all the given filters.

        Parameters:
            - node: Node to check
        """
        if not self.match_name(node):
            return False

        if not self.match_text(node):
            return False

        if not self.match_attributes(node):
            return False

        if callable(self.others):
            return self.others(node)

        return True
