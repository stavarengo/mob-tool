# Mob-Tool: `mobt`

Mob-Tool is a command-line tool designed to facilitate mob programming sessions for remote teams. The tool provides
several features to help teams manage their sessions, including controlling the timer, switching the driver
role among team members, and simplifying the necessary Git commands to hand over the work to the next team member.

> Mob programming is a software development approach where a team of developers works together on the same task at the
> same time.

## What changes does the tool make to the repository?

- **No changes are made in the `main` branch:** All changes are made in a new feature branch, and you can choose the
  name of the branch when you start the mob session.
- **All Git commands executed by the tool are logged in the output:** This way, the team can easily see what changes are
  being made to their repository.
- **All commands are rolled back if any error occurs:** The commands to rollback are also logged in the output.

## Installation

```shell
pip install mob-tool
```

**Important!**
> Please note that some operating systems might be equipped with the `python3` and `pip3` commands instead of `python`
> and `pip` (but they should be equivalent). If you don’t have `pip` or `pip3` available in your system, please check
> out [pip installation docs](https://pip.pypa.io/en/latest/installation/).

## Usage

### Starting a new session

To start a new session, use the following command:

```shell
mobt start <branch-name>
```

Here's an example of the output of the `start` command:

![Example of mobt start output](https://raw.githubusercontent.com/stavarengo/mob-tool/main/docs/start-output.png)

### Handing over to the next driver

When your time is up, pass the driver role to the next team member with the following command:

```shell
mobt next
```

Here's an example of the output of the `next` command:

![Example of mobt next output](https://raw.githubusercontent.com/stavarengo/mob-tool/main/docs/next-output.png)

Note that you must call `mob next` even if you didn't make any changes in the code, so the Mob-Tool can manage whose
turn is next.

The next driver (in this example, Erik) can start working by running the same `mobt start <branch-name>` command.

### Finishing the session when the feature is done

When your feature is ready, you can end the session with the following command:

```shell
mobt done
```

This will squash all the commits and push all the changes to the remote. All Git hooks will be executed for this final
commit. The hooks are always ignored during the `start` and `next` commands.

Here's an example of the output of the `done` command:

![Example of mobt done output](https://raw.githubusercontent.com/stavarengo/mob-tool/main/docs/done-output.png)

## FAQ

### What happens if one of the Git commands fails?

If one of the Git commands fails, all changes made to the repository are rolled back. Here's an example of the output
with a rollback in action:

![Example of output with rollback](https://raw.githubusercontent.com/stavarengo/mob-tool/main/docs/rollback-example.png)
