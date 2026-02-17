from __future__ import annotations
from fastmcp import FastMCP 

# create MCP server instance
mcp = FastMCP("arith")


def _as_number(x):
    """
    Accept ints/floats or numeric strings.
    Raise clean errors otherwise.
    """
    if isinstance(x, (int, float)):
        return float(x)

    if isinstance(x, str):
        try:
            return float(x.strip())
        except ValueError:
            pass

    raise TypeError("Expected a number (int/float or numeric string)")


# ---------------- TOOLS ---------------- #

@mcp.tool()
async def add(a: float, b: float) -> float:
    """Return a + b."""
    return _as_number(a) + _as_number(b)


@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """Return a - b."""
    return _as_number(a) - _as_number(b)


@mcp.tool()
async def multiply(a: float, b: float) -> float:
    """Return a * b."""
    return _as_number(a) * _as_number(b)


@mcp.tool()
async def divide(a: float, b: float) -> float:
    """Return a / b."""
    b = _as_number(b)
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return _as_number(a) / b


@mcp.tool()
async def power(base: float, exponent: float) -> float:
    """Return base ** exponent."""
    return _as_number(base) ** _as_number(exponent)


@mcp.tool()
async def percentage(value: float, percent: float) -> float:
    """Return percent% of value."""
    return (_as_number(value) * _as_number(percent)) / 100.0


# --------------- RUN SERVER --------------- #

if __name__ == "__main__":
    mcp.run()
