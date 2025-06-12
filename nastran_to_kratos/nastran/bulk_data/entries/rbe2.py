from __future__ import annotations

from dataclasses import dataclass

from ._bulk_data_entry import _BulkDataEntry


@dataclass
class Rbe2(_BulkDataEntry):
    """Defines a rigid body with independent degrees-of-freedom that are specified at a single grid point and with
    dependent degrees-of-freedom that are specified at an arbitrary number of grid points.
    """  # noqa: D205, E501

    eid: int
    "Element ID"

    gn: int
    "Independent grid point"

    cm: int
    "Component numbers (1-6) that are constrained"

    gmi: list[int]
    "Dependent grid points"

    alpha: float | None = None
    "Thermal expansion coefficient (optional)"

    tref: float | None = None
    "Reference temperature (optional)"

    @classmethod
    def from_file_content(cls, file_content: list[str]) -> Rbe2:
        """Parses an RBE2 card from Nastran input lines (supporting continuation lines)."""
        # Flatten and clean all fields
        flat_fields = []
        for line in file_content:
            fields = [f.strip() for f in line.split() if f.strip()]
            flat_fields.extend(fields)

        # Parse fixed fields
        eid = int(flat_fields[1])
        gn = int(flat_fields[2])
        cm = int(flat_fields[3])

        gmi = []
        alpha = None
        tref = None

        # Parse rest of the line
        for value in flat_fields[4:]:
            try:
                gmi.append(int(value))
            except ValueError:  # noqa: PERF203
                if alpha is None:
                    alpha = float(value)
                elif tref is None:
                    tref = float(value)
                else:
                    msg = f"Unexpected extra value in RBE2: {value}"
                    raise ValueError(msg)  # noqa: B904

        return cls(eid=eid, gn=gn, cm=cm, gmi=gmi, alpha=alpha, tref=tref)

    def to_file_content(self):  # noqa: ANN201, D102
        fields = ["RBE2", self.eid, self.gn, self.cm, *self.gmi]
        # Convert numeric fields to strings with appropriate formatting
        formatted_fields = []
        for field in fields:
            if isinstance(field, int):
                formatted_fields.append(f"{field:8d}")
            else:
                formatted_fields.append(f"{field:8}")
        # Handle alpha and tref with 8.1f format for floats
        if self.alpha is not None:
            formatted_fields.append(f"{self.alpha:8.1f}")
        if self.tref is not None:
            formatted_fields.append(f"{self.tref:8.1f}")
        # Join all fields into a single string and ensure correct length per line
        return "".join(formatted_fields).rstrip()

    def __hash__(self) -> int:
        """Return a hash of this instance."""
        return hash((self.eid, self.gn, self.cm, tuple(self.gmi), self.alpha, self.tref))
