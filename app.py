import hashlib
import os

from fastmcp import FastMCP

EMAIL = "24ds2000033@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP("Exam MCP Server")


@mcp.tool(name="solve_challenge")
def solve_challenge():
    """
    Reads the challenge from the incoming HTTP headers and returns
    the first 16 lowercase hex chars of

        SHA256(f"{challenge}:{EMAIL}")
    """

    # FastMCP exposes the current request through context
    from fastmcp.server.context import get_context

    ctx = get_context()
    request = ctx.request

    challenge = request.headers.get("X-Exam-Challenge")

    if not challenge:
        return "missing challenge"

    digest = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode()
    ).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )
