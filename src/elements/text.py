from .node import Node


class Text(Node):
    """
    Represents a block of text inside an HTML document.

    Parameters:
        - content: the textual content (str), no default
    """
    def __init__(self,
                 content: str):
        super().__init__()
        self.content: str = content

    def __repr__(self) -> str:
        return f"Text(\"{self.content}\")"
