from typing import Optional, Dict

from .node import Node
from .text import Text
from .filter import NodeFilter


class Tag(Node):
    """
    Represents an HTML tag node with attributes and child nodes.

    Parameters:
        - name: the tag name
        - attrs: the attributes of the tag
    """
    def __init__(self,
                 name: str,
                 attrs: Optional[Dict[str, str]] = None):
        super().__init__()
        self.name = name
        self.attrs = attrs if attrs else {}
        self.children = []

    def append(self,
               node: Node) -> None:
        """
        Adds a child node to the current tag.

        Parameters:
            - node: the node to append (Node), no default
        """
        node.parent = self
        self.children.append(node)

    def find(self,
             filter: NodeFilter):
        """
        Recursively searches for the first tag with the given name.

        Parameters:
            - filter: Filter To check for
        """
        for child in self.children:
            if isinstance(child, Tag):
                if filter.match(child):
                    return child
                result = child.find(filter)
                if result:
                    return result
        return None

    def find_all(self,
                 filter: NodeFilter):
        """
        Recursively searches for the first tag with the given name.

        Parameters:
            - filter: Filter To check for
        """
        results = []
        for child in self.children:
            if isinstance(child, Tag):
                if filter.match(child):
                    results.append(child)
                child_results = child.find_all(filter)
                if len(child_results):
                    results.extend(child_results)

        return results

    @property
    def text(self) -> str:
        """
        Extracts all text content from the tag and its descendants.

        Returns:
            - Text content (str)
        """
        texts = []
        for child in self.children:
            if isinstance(child, Text):
                texts.append(child.content)
            elif isinstance(child, Tag):
                texts.append(child.text)
        return ''.join(texts)

    def __repr__(self) -> str:
        return f"<{self.name} {self.attrs}> {self.text}</{self.name}>"
