from typing import Optional, List, Dict, Union


class Node:
    """
    Base class for all nodes in the parsed HTML tree.
    """
    def __init__(self) -> None:
        self.parent: Optional["Node"] = None