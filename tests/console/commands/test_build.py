from __future__ import annotations

import shutil
import tarfile

from pathlib import Path
from typing import TYPE_CHECKING

from poetry.factory import Factory


if TYPE_CHECKING:
    from poetry.utils.env import VirtualEnv
    from tests.types import CommandTesterFactory


def test_build_with_multiple_readme_files(
    tmp_path: Path, tmp_venv: VirtualEnv, command_tester_factory: CommandTesterFactory
):
    source_dir = (
        Path(__file__).parent.parent.parent / "fixtures" / "with_multiple_readme_files"
    )
    target_dir = tmp_path / "project"
    shutil.copytree(str(source_dir), str(target_dir))

    poetry = Factory().create_poetry(target_dir)
    tester = command_tester_factory("build", poetry, environment=tmp_venv)

    tester.execute()

    build_dir = target_dir / "dist"
    assert build_dir.exists()

    sdist_file = build_dir / "my_package-0.1.tar.gz"
    assert sdist_file.exists()
    assert sdist_file.stat().st_size > 0

    (wheel_file,) = build_dir.glob("my_package-0.1-*.whl")
    assert wheel_file.exists()
    assert wheel_file.stat().st_size > 0

    sdist_content = tarfile.open(sdist_file).getnames()
    assert "my_package-0.1/README-1.rst" in sdist_content
    assert "my_package-0.1/README-2.rst" in sdist_content
