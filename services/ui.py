from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def show_table(title, columns, rows):
    table = Table(title=title, show_lines=True)
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*[str(i) for i in row])
    console.print(table)

def show_progress(task_name, items, callback):
    """Show progress while processing."""
    with Progress(SpinnerColumn(), TextColumn("[bold green]{task.description}")) as progress:
        task = progress.add_task(task_name, total=len(items))
        for item in items:
            callback(item)
            progress.advance(task)
