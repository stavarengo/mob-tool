import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

print(find_packages(where="src"))

setup(
    name="mob",
    version="0.1.0",  # Required
    description="Mob handover tool",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/stavarengo/mob",  # Optional
    author="rfst",  # Optional
    keywords="mob mob-programming timer mob-programming-timer cli-tool remote-mob-programming remote-mobs",
    package_dir={"": "src"},
    packages=find_packages(where="src"),  # Required
    python_requires=">=3.6",
    entry_points={  # Optional
        "console_scripts": [
            "mob=mob.commands:cli",
        ],
    },
    project_urls={  # Optional
        "Say Thanks!": "https://saythanks.io/to/faelsta",
        "Source": "https://github.com/stavarengo/stavarengo/",
    },
)
