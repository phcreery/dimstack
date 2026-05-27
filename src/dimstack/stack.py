from typing import Any

from .display import display_df
from .dim import Basic, Reviewed


class Stack:
    def __init__(
        self,
        dims: list[Basic],
        name: str = "Stack",
        desc: str = "",
    ):
        self.name = name
        self.desc = desc
        self.dims = dims

    def __str__(self) -> str:
        dim_array = "\n".join([f"{dim}" for dim in self.dims])
        return f"{self.name} ({len(self.dims)} dims)\n{dim_array}"

    def _repr_html_(self):
        return display_df(self.dict, f"DIMENSION STACK: {self.name}", dispmode="html")

    def _display_(self):
        return display_df(self.dict, f"DIMENSION STACK: {self.name}")

    def show(self, expand=False):
        return display_df(self.dict, f"DIMENSION STACK: {self.name}")

    def append(self, measurement: Basic):
        """Append a measurement to the stack."""
        self.dims.append(measurement)

    @property
    def dict(self) -> list[dict[str, Any]]:
        return [dim.dict for dim in self.dims]


class ReviewedStack:
    def __init__(
        self,
        name: str = "Reviewed Stack",
        desc: str = "",
        dims: list[Reviewed] = [],
    ):
        self.name = name
        self.desc = desc

        # ensure all dims are Reviewed
        for dim in dims:
            if not isinstance(dim, Reviewed):
                raise ValueError("All dims must be Reviewed dimensions.")

        self.dims = dims

    def __str__(self) -> str:
        dim_array = "\n".join([f"{dim}" for dim in self.dims])
        return f"{self.name} ({len(self.dims)} dims)\n{dim_array}"

    def _repr_html_(self):
        return display_df(self.dict, f"REVIEWED DIMENSION STACK: {self.name}", dispmode="html")

    def _display_(self):
        return display_df(self.dict, f"REVIEWED DIMENSION STACK: {self.name}")

    def show(self, expand=False):
        return display_df(self.dict, f"REVIEWED DIMENSION STACK: {self.name}")

    def append(self, measurement: Reviewed):
        """Append a measurement to the stack."""
        self.dims.append(measurement)

    @property
    def dict(self) -> list[dict[str, Any]]:
        return [dim.dict for dim in self.dims]

    def to_basic_stack(self) -> Stack:
        """Convert the stack to a basic stack."""
        return Stack(
            name=self.name,
            desc=self.desc,
            dims=[rdim.dim for rdim in self.dims],
        )
