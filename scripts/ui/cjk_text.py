"""Chinese wrapping support for the pinned pygame-gui 0.6.13 text layout.

The upstream layout treats a Chinese sentence as one long word and adds hyphens.
Add break opportunities without inserting characters into saved/displayed text.
"""

from functools import wraps


def is_cjk(character):
    return "\u3400" <= character <= "\u9fff"


def cjk_break_points(text):
    closing = "，。！？；：、）》】」』…％%"
    opening = "（《【「『"
    return [
        index
        for index in range(1, len(text))
        if text[index] not in closing
        and text[index - 1] not in opening
        and (
            text[index - 1] == " "
            or is_cjk(text[index - 1])
            or is_cjk(text[index])
            or text[index - 1] in closing
        )
    ]


def install_cjk_wrapping():
    from pygame_gui.core.text.text_line_chunk import TextLineChunkFTFont

    original = TextLineChunkFTFont.split
    if getattr(original, "_clangen_cjk", False):
        return

    @wraps(original)
    def split(self, requested_x, line_width, row_start_x, allow_split_dashes=True):
        if any(is_cjk(char) for char in self.text):
            self.split_points = cjk_break_points(self.text)
            allow_split_dashes = False
        return original(self, requested_x, line_width, row_start_x, allow_split_dashes)

    split._clangen_cjk = True
    TextLineChunkFTFont.split = split
