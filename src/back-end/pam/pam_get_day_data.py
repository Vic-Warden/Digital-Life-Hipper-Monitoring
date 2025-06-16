from services import DayDataDownload
import asyncio
downloader = DayDataDownload(filename="output/___11_06_2025__dayData_90245_experiment",
                days=10,
                label_id=90245)


asyncio.run(downloader.run())

