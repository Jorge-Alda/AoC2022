import datetime
from pathlib import Path

start_date = datetime.date(2022, 11, 30)
today = datetime.date.today()

if __name__ == '__main__':
    with open("Python/README.md", "wt") as f:
        f.write("# Advent of Code 2022 - Python 🐍\n\n")
        if today > start_date:
            f.write("AoC already started!\n\n")
            delta = today - start_date
            days = min(delta.days, 25)
            puzzles = 0
            complete_days = 0
            for i in range(1, days+1):
                f.write(f"* [Day {i:02d}](Day{i:02d})")
                path = Path(f"./Python/Day{i:02d}/status")
                if path.exists():
                    with path.open("rt") as fs:
                        status = fs.read()
                    if status == '2':
                        f.write("🟩\n")
                        puzzles += 2
                        complete_days += 1
                    elif status == '1':
                        f.write("🟨\n")
                        puzzles += 1
                    else:
                        f.write("🟥\n")
                else:
                    f.write("🟦\n")
            f.write(
                f"\nPuzzles completed: {puzzles}/{2*days} ({50*puzzles/days:.2f}%)")
            f.write(
                f"\nDays completed: {complete_days}/{days} ({100*complete_days/days:.2f}%)\n")
        else:
            delta = start_date - today
            f.write(
                f"AoC hasn't started yet. It will start in {delta.days + 1} days!\n")
