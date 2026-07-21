import hashlib
import os

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

EMAIL = "24ds2000033@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP("Exam MCP Server")


@mcp.tool(
    name="solve_challenge",
    description="Solve the exam challenge."
)
def solve_challenge() -> str:
    """
    Reads X-Exam-Challenge from the incoming HTTP headers and returns
    the first 16 lowercase hex characters of

        SHA256(f"{challenge}:{EMAIL}")
    """

    headers = get_http_headers()

    # Header lookup is case-insensitive, but try both just in case.
    challenge = (
        headers.get("x-exam-challenge")
        or headers.get("X-Exam-Challenge")
    )

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    digest = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode("utf-8")
    ).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )
