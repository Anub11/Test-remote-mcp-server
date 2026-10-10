import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "todos.db"


async def initialize_database():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def add_todo(title: str) -> dict:
    title = title.strip()

    if not title:
        raise ValueError("Todo title cannot be empty.")

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "INSERT INTO todos (title) VALUES (?)",
            (title,),
        )
        await db.commit()

        todo_id = cursor.lastrowid

        cursor = await db.execute(
            "SELECT * FROM todos WHERE id = ?",
            (todo_id,),
        )
        row = await cursor.fetchone()

        return dict(row)


async def list_todos() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "SELECT * FROM todos ORDER BY id DESC"
        )
        rows = await cursor.fetchall()

        return [dict(row) for row in rows]


async def get_todo(todo_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "SELECT * FROM todos WHERE id = ?",
            (todo_id,),
        )
        row = await cursor.fetchone()

        return dict(row) if row else None


async def complete_todo(todo_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        await db.execute(
            "UPDATE todos SET completed = 1 WHERE id = ?",
            (todo_id,),
        )
        await db.commit()

        cursor = await db.execute(
            "SELECT * FROM todos WHERE id = ?",
            (todo_id,),
        )
        row = await cursor.fetchone()

        return dict(row) if row else None


async def delete_todo(todo_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM todos WHERE id = ?",
            (todo_id,),
        )
        await db.commit()

        return cursor.rowcount > 0


async def main():
    await initialize_database()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())