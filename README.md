# mob

This project aims to provide a command line tool for facilitating "mob programming" sessions. The tool, named `mob`, is
designed to automate the process of creating and switching between branches, as well as keeping track of session
participants.

## Installation in development mode

To install mob in development mode, you will need to have Python 3.7 or later and pip installed on your system. Then,
you can run the following command:

```bash
pip install -e .
````

This command will install the package in editable mode, which means that you will be able to make changes to the code
and see the results immediately without having to re-install the package.

Once the installation is complete, you should be able to run the mob command from the command line.

> The `-e` option is used to install the package in "editable" or "develop" mode. This means that any changes made to
> the package's source code will be immediately reflected in the installed package without the need to re-install it.
> This is useful during development because it allows you to make changes to the package and test them without having to
> go through the process of uninstalling and reinstalling the package every time.

## Installation in production mode

(NOT PUBLISHED YET)

To install the package, you need to have python 3.7 or later installed.

```bash
pip install mob
```

## What changes does the tool make in my repository?

- It creates a file called `.mob.last_team.json` and marks it to be ignored by Git (`.git/info/exclude`). This does not
  affect the repository in any way, but it allows the tool to keep track of the team members that were used in the last
  session.

It's work mentioning that the tool will never change anything in the main branch. It will always create a new branch
where the mob team will be working on.

The tool keeps tracks of the changes made in the repository (eg, checkout, commit, etc) and reverts all the changes
in case of an error. This means that the tool will never leave the repository in a dirty state. See the
file `src/mob/GitCli/GitCliWithAutoRollback.py` for more details.

## How will this work (when the app is finished)

A developer can start a Mob Programming session by typing `mob start BRANCH_NAME teammember1,teammember2,...` in the
command line. This will create a new branch with the specified name, create a file called `.mob.json` in the root of the
repository, and push it to the remote repository with the message `WIP mob: start session`.

A timer will appear on the terminal, counting down 10 minutes. Underneath the timer, the name of the current driver (the
person who executed `mob start`) and the name of the current navigator will be displayed. When the driver's timer is up,
they will execute the command `mob next`. This will commit everything in the working directory with the
message `WIP mob:
next driver is teammember2` and push it to the remote repository.

In the terminal, a message of success will appear with a message indicating who the next driver is. The next driver will
then execute `mob start BRANCH_NAME` on their machine. The names of the team members are no longer necessary as the tool
will load the contents from the `.mob.json` file in the repository. The timer starts again and the process repeats until
the team finishes the development of the feature.

When they are finished, the last driver will execute `mob done COMMIT_MESSAGE`. This will delete the `.mob.json` file
and
squash all the commits into one, with the message `COMMIT_MESSAGE`. At this point, git hooks will be allowed to execute,
as they were skipped when running `mob next`, for the sake of speed and simplicity. The work is then force pushed to the
remote `BRANCH_NAME` where the feature was developed.

The tool never changes anything on the main branch and will also take care of controlling when it's time for a break and
reminding the team when the time arrives.

## The `.mob.json` file

The `.mob.json` file contains information about the Mob Programming session. The file's content will be a JSON like
this (not confirmed yet):

- `version`: The version of the mob programming tool that created the file.
    - `session`:
        - `branch`: The branch name where the feature is being developed.
        - `team`:
            - `driver`: The current driver.
            - `navigator`: The current navigator.
            - `restOfTheTeam`: The rest of the team members.
        - `rotation`:
            - `driverInMinutes`: The number of minutes the driver will drive before switching.
            - `breakInMinutes`: The number of minutes of the break.
            - `howManyRotationsBeforeBreak`: The number of rotations before the break.

Example of the Python classes to represent this JSON structure (this is not confirmed yet, just a draft)

```python
from dataclasses import dataclass
from typing import Optional
from typing import Tuple, TypedDict


@dataclass(frozen=True)
class MobDataRotation(TypedDict):
    driverInMinutes: int
    breakInMinutes: int
    howManyRotationsBeforeBreak: int


@dataclass(frozen=True)
class TeamMembers(TypedDict):
    driver: str
    navigator: str
    restOfTheTeam: Tuple[str, ...]


@dataclass(frozen=True)
class MobDataSession(TypedDict):
    branch: Optional[str]
    team: TeamMembers
    rotation: MobDataRotation


@dataclass(frozen=True)
class SessionSettings(TypedDict):
    version: int
    session: MobDataSession


initial_state: SessionSettings = {
    "version": 1,
    "session": {
        "branch": "mob/feature-1",
        "team": {
            "driver": "member1",
            "navigator": "member2",
            "restOfTheTeam": ("member3", "member4"),
        },
        "rotation": {
            "driverInMinutes": 10,
            "breakInMinutes": 15,
            "howManyRotationsBeforeBreak": 6,
        },
    },
}
```