"""Build two portable MiniCheck archives for Masterskilla."""

import argparse
import gzip
import hashlib
import platform
import subprocess
import tarfile
import tempfile
from pathlib import Path

SOURCE = Path(__file__).with_name("minicheck.c")
VERSIONS = ("1.0.0",)


def build(destination):
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        raise SystemExit("MiniCheck wird auf einem Linux-x86-64-Rechner gebaut.")
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="minicheck-build-") as directory:
        binary = Path(directory) / "minicheck"
        for version in VERSIONS:
            subprocess.run(
                ["cc", "-std=c11", "-Wall", "-Wextra", "-O2", "-march=x86-64", "-s",
                 f'-DMINICHECK_VERSION="{version}"', str(SOURCE), "-o", str(binary)],
                check=True,
            )
            archive = destination / f"minicheck-{version}-linux-x86_64.tar.gz"
            with archive.open("wb") as stream, gzip.GzipFile(fileobj=stream, mode="wb", mtime=0) as compressed:
                with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.USTAR_FORMAT) as tar:
                    member = tarfile.TarInfo(f"minicheck-{version}/minicheck")
                    member.mode = 0o755
                    member.size = binary.stat().st_size
                    with binary.open("rb") as executable:
                        tar.addfile(member, executable)
            with archive.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            archive.with_name(archive.name + ".sha256").write_text(f"{digest}  {archive.name}\n")
            print(archive.resolve())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", nargs="?", type=Path, default=SOURCE.parent / "dist")
    build(parser.parse_args().destination)
