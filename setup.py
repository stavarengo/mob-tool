import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="mobt",
    version="0.1.2",
    description="Mob session management tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stavarengo/mob",
    author="rfst",
    keywords="mob mob-programming timer mob-programming-timer cli-tool remote-mob-programming remote-mobs",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "mob=mob.Controllers:cli",
        ],
    },
    project_urls={
        "Say Thanks!": "https://saythanks.io/to/faelsta",
        "Source": "https://github.com/stavarengo/stavarengo/",
    },
    install_requires=[
        'click==8.1.3',
        'injector==0.20.1',
        'dataclasses-json==0.5.7',
        'GitPython==3.1.30',
        'colorama==0.4.6',
    ],
)
