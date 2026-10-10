from contextlib import asynccontextmanager

from fastmcp import FastMCP

from remote_mcp import todos


@asynccontextmanager
async def lifespan(server):
    await todos.initialize_database()
    yield


mcp = FastMCP(
    "Remote Todo Server",
    lifespan=lifespan,
)


@mcp.tool()
async def add_todo(title: str) -> dict:
    """Add a new todo."""
    return await todos.add_todo(title)


@mcp.tool()
async def list_todos() -> list[dict]:
    """List all todos."""
    return await todos.list_todos()


@mcp.tool()
async def get_todo(todo_id: int) -> dict | None:
    """Get a todo by its ID."""
    return await todos.get_todo(todo_id)


@mcp.tool()
async def complete_todo(todo_id: int) -> dict | None:
    """Mark a todo as completed."""
    return await todos.complete_todo(todo_id)


@mcp.tool()
async def delete_todo(todo_id: int) -> bool:
    """Delete a todo."""
    return await todos.delete_todo(todo_id)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
    )