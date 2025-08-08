from typing import List, Tuple

from html.parser import HTMLParser
from typing import Optional

from .constants import VOID_TAGS

from .elements.tag import Tag
from .elements.text import Text


class MySoupParser(HTMLParser):
    """
    Internal parser that builds a tag tree from HTML using the standard library.

    Uses html.parser.HTMLParser to walk the document and build a tree.
    """
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[Tag] = []
        self.root: Tag = Tag("html")
        self.stack.append(self.root)

    def handle_starttag(self,
                        tag: str,
                        attrs: List[Tuple[str, Optional[str]]]) -> None:
        """
        Handles an opening tag and pushes it onto the stack.

        Parameters:
            - tag: tag name (str), no default
            - attrs: list of (attribute, value) tuples, value may be None
        """
        attr_dict = {k: v if v is not None else "" for k, v in attrs}
        new_tag = Tag(tag, attr_dict)
        self.stack[-1].append(new_tag)

        if tag.lower() not in VOID_TAGS:
            self.stack.append(new_tag)

    def handle_endtag(self, tag: str) -> None:
        """
        Handles a closing tag and pops the current tag from the stack.

        Parameters:
            - tag: tag name to close (str), no default
        """
        if len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        """
        Handles raw text between tags.

        Parameters:
            - data: textual data content (str), no default
        """
        if data.strip():
            text_node = Text(data)
            self.stack[-1].append(text_node)


def MySoup(html: str) -> Tag:
    """
    Parses an HTML string into a tree of Tag and Text nodes.

    Parameters:
        - html: the HTML content as a string (str), no default

    Returns:
        - Root tag of the parsed tree (Tag)
    """
    parser = MySoupParser()
    parser.feed(html)
    return parser.root
