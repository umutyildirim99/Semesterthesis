from dataclasses import dataclass

from ._nastran_entry import _NastranEntry


@dataclass
class Grid(_NastranEntry):
    """A geometric grid point."""

    id: int
    cp: int | None = None
    x1: float = 0.0
    x2: float = 0.0
    x3: float = 0.0
    cd: int | None = None
    ps: str | None = None
    seid: int = 0

    @classmethod
    def read(cls, raw_entry: list[str]) -> "Grid":
        return Grid(
            id=int(raw_entry[1]),
            cp=cls._read_cp(raw_entry),
            x1=float(raw_entry[3]),
            x2=float(raw_entry[4]),
            x3=float(raw_entry[5]),
            cd=cls._read_cd(raw_entry),
            ps=cls._read_ps(raw_entry),
            seid=cls._read_seid(raw_entry),
        )

    @classmethod
    def _read_cp(cls, raw_entry: list[str]) -> int | None:
        field_index = 2

        field_is_empty = raw_entry[field_index] == " " * 8
        if field_is_empty:
            return None
        else:
            return int(raw_entry[field_index])

    @classmethod
    def _read_cd(cls, raw_entry: list[str]) -> int | None:
        field_index = 6

        try:
            field_is_empty = raw_entry[field_index] == " " * 8
        except IndexError:
            field_is_empty = True

        if field_is_empty:
            return None
        else:
            return int(raw_entry[field_index])

    @classmethod
    def _read_ps(cls, raw_entry: list[str]) -> str | None:
        field_index = 7

        try:
            field_is_empty = raw_entry[field_index] == " " * 8
        except IndexError:
            field_is_empty = True

        if field_is_empty:
            return None
        else:
            return raw_entry[field_index].strip()

    @classmethod
    def _read_seid(cls, raw_entry: list[str]) -> int:
        field_index = 8

        try:
            field_is_empty = raw_entry[field_index] == " " * 8
        except IndexError:
            field_is_empty = True

        if field_is_empty:
            return 0
        else:
            return int(raw_entry[field_index])
