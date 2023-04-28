#!python3
from argparse import ArgumentParser
from os.path import isfile, exists
from subprocess import run
from time import time


start_time = time()

parser = ArgumentParser(prog="qncm", description="Qncm is Not a Config Manager")
parser.add_argument(
    "--from_dir",  # Can't use 'from' due to python limitations
    default="/",
    metavar="PATH",
    help="directory to copy FROM (%(default)s)",
)
parser.add_argument(
    "--to",
    default="qncm_save/",
    metavar="PATH",
    help="directory to copy TO (%(default)s)",
)
parser.add_argument(
    "--include",
    default="list",
    metavar="FILE",
    help="path to file which lists paths to copy (%(default)s)",
)
parser.add_argument(
    "--exclude",
    metavar="FILE",
    help="path to file which lists paths to not copy (%(default)s)",
)
parser.add_argument("--version", action="version", version="No version for now")

args = parser.parse_args()
if not isfile(args.include):
    parser.exit(1, message=f"Include file '{args.include}' does not exist!\n")
if args.exclude and not isfile(args.exclude):
    parser.exit(1, message=f"Exclude file '{args.exclude}' does not exist!\n")


with open(args.include, "r") as file:
    include = file.read().splitlines()

if args.exclude:
    with open(args.exclude, "r") as file:
        exclude = file.read().splitlines()


def print_result(status: str, msg: str = "") -> None:
    status = {
        "success": "✓",
        "error": "✕",
        "warning": "!",
        "comment": "#",
        "exclude": "-",
        "blank": "",
    }[status]
    print(f"\t{status} {msg}")


errors = []
warnings = []

print("Copying elements:")

for line in include:
    if not line:
        print_result("blank")
        continue
    if line[0] == "#":
        print_result("comment", line)
        continue
    if args.exclude and line in exclude:
        print_result("exclude", line)
        continue

    path = args.from_dir + line  # TODO: use pathlib
    if not exists(path):
        print_result("warning", path)
        warnings.append(f"'{path}' does not exist!")
        continue

    # print(path, "->", args.to + line)
    # continue
    status = run(  # TODO: use pathlib!
        # "echo test",
        f"rsync -aR {path} {args.to}",
        shell=True,
        capture_output=True,
        universal_newlines=True,
    )
    if status.returncode:
        print_result("error", line)
    else:
        print_result("success", line)


if warnings:
    print(f"\n Warning! ({len(warnings)}):")
    for warning in warnings:
        print("\t" + warning)

if errors:
    print(f"\nERROR! ({len(errors)}):")
    for error in errors:
        print("\t" + error, end="")


print(f"\nDone in {round(time()-start_time, 5)} seconds!")
