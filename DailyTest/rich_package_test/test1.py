from rich.progress import track
import time

for i in track(range(100)):
	time.sleep(1)


