#!python3
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
from time import time


start_time = time()

parser = ArgumentParser(prog="qncm", description="Qncm is Not a Config Manager")
parser.add_argument(
    "--from_dir",  # Can't use 'from' due to python limitations
    type=Path,
    default=Path("/"),
    metavar="",  # "PATH",
    help="directory to copy from (%(default)s)",
)
parser.add_argument(
    "--to_dir",  # _dir suffix for symmetry with from_dir
    type=Path,
    default=Path("qncm_save/"),
    metavar="",  # "PATH",
    help="directory to copy to (%(default)s)",
)
parser.add_argument(
    "--include",
    type=Path,
    default=Path("list"),
    metavar="",  # "FILE",
    help="path to file which lists paths to copy (%(default)s)",
)
parser.add_argument(
    "--exclude",
    type=Path,
    metavar="",  # "FILE",
    help="path to file which lists paths to not copy (%(default)s)",
)
parser.add_argument("--version", action="version", version="No version for now")

args = parser.parse_args()

if not args.from_dir.is_dir():
    parser.exit(
        1,
        message=f"Directory passed to '--from_dir' ({args.from_dir}) does not exist!\n",
    )
if not args.include.is_file():
    parser.exit(
        1, message=f"File passed to '--include' ({args.include}) does not exist!\n"
    )
if args.exclude and not args.exclude.is_file:
    parser.exit(
        1, message=f"File passed to '--exclude' ({args.exclude}) does not exist!\n"
    )


include = args.include.read_text(encoding="utf-8").splitlines()

if args.exclude:
    exclude = args.exclude.read_text(encoding="utf-8").splitlines()


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

    path = args.from_dir / line
    if not path.exists():
        print_result("warning", path)
        warnings.append(f"'{path}' does not exist!")
        continue

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
