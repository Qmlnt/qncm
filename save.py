#!python3
from time import time
from os.path import exists
from subprocess import run

start_time = time()

copy_to = "./save_dir/"
errors = []
warnings = []

with open("list", "r") as file:
    lines = file.read().splitlines()
print("Copying elements:")


for line in lines:
    if not line:
        print()
        continue
    if line[0] == "#":
        print("\t-", line.strip("# "))
        continue
    if not exists(line):
        print("\t!", line)
        warnings.append(f"'{line}' does not exist!")
        continue

    status = run(
        # "echo test",
        f"rsync -aR {line} ./save_dir",
        shell=True,
        capture_output=True,
        universal_newlines=True,
    )
    if status.returncode:
        print("\t✕", line)
        errors.append(status.stderr)
    else:
        print("\t✓", line)

if warnings:
    print(f"\n Warning! ({len(warnings)}):")
    for warning in warnings:
        print("\t" + warning)

if errors:
    print(f"\nERROR! ({len(errors)}):")
    for error in errors:
        print("\t" + error, end="")


print(f"\nDone in {round(time()-start_time, 5)} seconds!")
