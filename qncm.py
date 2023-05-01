#!python3
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
from time import time


start_time = time()

parser = ArgumentParser(prog="qncm", description="Qncm is Not a Config Manager")
parser.add_argument(
    "--from",
    dest="from_dir",
    type=Path,
    default=Path("/"),
    metavar="",  # PATH
    help="directory to copy from (%(default)s)",
)
parser.add_argument(
    "--to",
    dest="to_dir",
    type=Path,
    default=Path("qncm_save/"),
    metavar="",  # PATH
    help="directory to copy to (%(default)s)",
)
parser.add_argument(
    "-if",
    "--include_file",
    dest="include_file",
    type=Path,
    metavar="",  # FILE
    help="file with paths to copy (%(default)s)",
)
parser.add_argument(
    "-il",
    "--include_list",
    dest="include_list",
    nargs="*",
    metavar="",  # LIST
    help="space separated paths to copy (%(default)s)",
)
parser.add_argument(
    "-ef",
    "--exclude_file",
    dest="exclude_file",
    type=Path,
    metavar="",  # FILE
    help="file with paths to ignore (%(default)s)",
)
parser.add_argument(
    "-el",
    "--exclude_list",
    dest="exclude_list",
    nargs="*",
    metavar="",  # LIST
    help="space separated paths to ignore (%(default)s)",
)
parser.add_argument("--version", action="version", version="No version for now")

args = parser.parse_args()

if not args.from_dir.is_dir():
    parser.exit(
        1,
        message=f"Directory passed to '--from_dir' ({args.from_dir}) does not exist!\n",
    )
if not (args.include_file or args.include_list):
    parser.exit(
        1,
        message="'--include_file' or/and '--include_list' must be specified!\n",
    )
if args.include_file and not args.include_file.is_file():
    parser.exit(
        1,
        message=f"File passed to '--include_file' ({args.include_file}) does not exist!\n",
    )
if args.exclude_file and not args.exclude_file.is_file():
    parser.exit(
        1,
        message=f"File passed to '--exclude_file' ({args.exclude_file}) does not exist!\n",
    )


include = []
if args.include_file:
    include.extend(args.include_file.read_text(encoding="utf-8").splitlines())
if args.include_list:
    include.extend(["", "#From command line:"])
    include.extend(args.include_list)

exclude = []
if args.exclude_file:
    exclude.extend(args.exclude_file.read_text(encoding="utf-8").splitlines())
if args.exclude_list:
    exclude.extend(args.exclude_list)


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
        print_result("comment", line[1:])
        continue
    if line in exclude:
        print_result("exclude", line)
        continue

    path = args.from_dir / line
    if not path.exists():
        print_result("warning", path)
        warnings.append(f"'{path}' does not exist!")
        continue

    status = run(  # TODO: omit using subprocess
        # "echo test",
        f"rsync -aR {path} {args.to_dir}",
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
