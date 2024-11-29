def _indent(string: str, number_of_indents: int) -> str:
    """Add a specified number of indents to a string."""
    return "    " * number_of_indents + string


def _remove_empty_last_row(mdpa_content: list[str]) -> list[str]:
    if len(mdpa_content) != 0 and mdpa_content[-1] == "":
        return mdpa_content[:-1]
    return mdpa_content
