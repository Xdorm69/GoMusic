import os
import pandas as pd
import asyncio
import subprocess
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn


async def run_command(cmd, progress, task_id, query):
    """Run a shell command asynchronously and update progress."""
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        progress.console.print(f"❌ Error downloading: {query}")
    progress.advance(task_id)

async def download_song(row, prefix, progress, task_id):
    artist = str(row['artist']).strip()
    title = str(row['title']).strip()
    language = str(row.get('language', '')).strip()

    query = f"{artist} {title} {language}".strip()
    output_name = f"{prefix}_{title.title()}_{artist.title()}" if prefix else f"{title.title()}_{artist.title()}"
    output_path = f"downloads/{output_name}.mp3"

    if os.path.exists(output_path):
        progress.console.print(f"⏩ Skipping already downloaded: {output_name}.mp3")
        progress.advance(task_id)
        return

    progress.console.print(f"🎵 Downloading: {query}")
    cmd = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "-f", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", f"downloads/{output_name}.%(ext)s",
    ]
    await run_command(cmd, progress, task_id, query)

async def download_songs_async(prefix=""):
    os.makedirs("downloads", exist_ok=True)
    download_list = pd.read_csv("./download_list.csv")

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
    ) as progress:
        task_id = progress.add_task("Downloading songs...", total=len(download_list))
        tasks = [download_song(row, prefix, progress, task_id) for _, row in download_list.iterrows()]
        await asyncio.gather(*tasks)

    print("\n✅ All downloads complete!")

def download_songs(prefix=""):
    asyncio.run(download_songs_async(prefix))

if __name__ == "__main__":
    download_songs("test")
