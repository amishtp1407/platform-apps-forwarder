#!/usr/bin/env python3
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import tarfile
import warnings
import zipfile
from pathlib import Path

import click

here = Path(__file__).absolute().parent

TEMP_DIR = here / "build"
DIST_DIR = here / "dist"

@click.group(chain=True)
@click.option("--dirty", is_flag=True)
def cli(dirty):
    if dirty:
        print("Keeping temporary files.")
    else:
        print("Cleaning up temporary files...")
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
        if DIST_DIR.exists():
            shutil.rmtree(DIST_DIR)

        TEMP_DIR.mkdir()
        DIST_DIR.mkdir()

@cli.command()
def wheel():
    """Build the wheel for PyPI."""
    print("Building wheel...")
    subprocess.check_call(
        [
            "python",
            "-m",
            "build",
            "--outdir",
            DIST_DIR,
        ]
    )
    if os.environ.get("GITHUB_REF", "").startswith("refs/tags/"):
        ver = version()  # assert for tags that the version matches the tag.
    else:
        ver = "*"
    (whl,) = DIST_DIR.glob(f"forwarder-{ver}-py3-none-any.whl")
    print(f"Found wheel package: {whl}")
    subprocess.check_call(["tox", "-e", "wheeltest", "--", whl])


class ZipFile2(zipfile.ZipFile):
    # ZipFile and tarfile have slightly different APIs. Let's fix that.
    def add(self, name: str, arcname: str) -> None:
        return self.write(name, arcname)

    def __enter__(self) -> ZipFile2:
        return self

    @property
    def name(self) -> str:
        assert self.filename
        return self.filename


def archive(path: Path) -> tarfile.TarFile | ZipFile2:
    return tarfile.open(path.with_name(f"{path.name}.tar.gz"), "w:gz")


def version() -> str:
    return os.environ.get("GITHUB_REF_NAME", "").replace("/", "-") or os.environ.get(
        "BUILD_VERSION", "dev"
    )


def operating_system() -> str:
    match platform.system():
        case "Windows":
            system = "windows"
        case "Linux":
            system = "linux"
        case "Darwin":
            system = "macos"
        case other:
            warnings.warn("Unexpected system.")
            system = other
    match platform.machine():
        case "AMD64" | "x86_64":
            machine = "x86_64"
        case "arm64":
            machine = "arm64"
        case other:
            warnings.warn("Unexpected platform.")
            machine = other
    return f"{system}-{machine}"


def _pyinstaller(specfile: str) -> None:
    print(f"Invoking PyInstaller with {specfile}...")
    subprocess.check_call(
        [
            "pyinstaller",
            "--clean",
            "--workpath",
            TEMP_DIR / "pyinstaller/temp",
            "--distpath",
            TEMP_DIR / "pyinstaller/out",
            specfile,
        ],
        cwd=here / "specs",
    )


@cli.command()
def standalone_binaries():
    """Linux: Build the standalone binaries generated with PyInstaller"""
    with archive(DIST_DIR / f"forwarder-{version()}-{operating_system()}") as f:
        _pyinstaller("standalone.spec")

        _test_binaries(TEMP_DIR / "pyinstaller/out")

        for tool in ["forwarder"]:
            executable = TEMP_DIR / "pyinstaller/out" / tool

            f.add(str(executable), str(executable.name))
    print(f"Packed {f.name!r}.")


def _test_binaries(binary_directory: Path) -> None:
    for tool in ["forwarder"]:
        executable = binary_directory / tool

        print(f"> {tool} --version")
        subprocess.check_call([executable, "--version"])

        print(f"> {tool} -s selftest.py")
        subprocess.check_call([executable, "-s", here / "selftest.py"])


if __name__ == "__main__":
    cli()
