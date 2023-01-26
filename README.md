mob

This project aims to provide a command line tool for facilitating "mob programming" sessions. The tool, named `mob`, is
designed to automate the process of creating and switching between branches, as well as keeping track of session
participants.

Installation

mob requires pipenv to be installed in development environment. If you don't have pipenv installed, you can
install it by running:

```bash
pip install pipenv
```

After installing pipenv, you can clone the mob repository and create a virtual environment for it:

```bash
git clone https://github.com/stavarengo/mob.git
cd mob
pipenv install --dev
```

To install the package in development mode, so that changes made to the codebase are reflected in the app, run:

```bash
pipenv install -e .
```

You can now run the mob command directly from your terminal, by calling it via pipenv:

```bash
pipenv run mob
```

# TODO's (brainstorm)

This TODO's (brainstorm) and the diagrams are here only because of my colleague [@zsparal](https://github.com/zsparal).
Thanks
dude!
❤️

## The following is pretty much a draft of the idea for this project - Don't take it as written in stone

### Usage

To start a mob session, the user runs the command mob start branch_name.

- If the branch_name does not exist:
    - The branch is created based on the origin/master
    - A file called `.mob` with the app state is created in the root directory, containing the name of the branch and
      the name of the team participating in this session.
- If the branch_name already exists:
- The branch is downloaded and the mob session is continued using the `.mob` file created in the root directory.
    - When the session starts, a timer counting down 10 minutes is displayed in the terminal.
- When the timer is over, an alarm sounds
- To proceed to the next driver, the user types `mob next`.
    - This will commit all changes in the working directory with the message "WIP mob: next is driver FOO"

### Todos

- [ ] Implement the mob start command
- [ ] Handle the case where the specified branch does not exist and create it based on origin/master
- [ ] Create a file to save the state of the session in the root directory
- [ ] Implement a timer to track the duration of the session
- [ ] Implement the mob next command to commit changes with the message "WIP mob: next is driver FOO"
- [ ] Handle the case where the current working directory is not clean and display an appropriate error message
- [ ] Create functions to check for the existence of the .mob file and read its contents
- [ ] Implement a notification (e.g. sound) when the timer is over
- [ ] Test and debug the mob command and its functions.

[//]: # ()

[//]: # (### Brainstorming)

[//]: # ()

[//]: # (<!--![Diagram Image Link]&#40;./puml/mindmap.puml&#41;-->)

[//]: # (<!--![activity.mob-start.puml]&#40;./puml/activity.mob-start.puml&#41;-->)

[//]: # (<!--![activity.puml]&#40;./puml/activity.puml&#41;-->)

[//]: # (<!--![class.puml]&#40;./puml/class.puml&#41;-->)

[//]: # ()
