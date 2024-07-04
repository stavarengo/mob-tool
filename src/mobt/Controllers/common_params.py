import functools
import logging
import os
import sys
from dataclasses import dataclass

import click
from click import Context

class AppContext(object):

    def __init__(self):
        self.verbose = 0
        self.silent = 0

    @property
    def log_level(self)->int:
        log_level = logging.WARNING

        if self.silent == 1:
            log_level = logging.ERROR
        elif self.silent == 2:
            log_level = logging.CRITICAL
        elif self.silent >= 3:
            log_level = logging.CRITICAL + 1
        elif self.verbose == 0:
            # Default value set before the if
            pass
        elif self.verbose == 1:
            log_level = logging.INFO
        elif self.verbose == 2:
            log_level = logging.DEBUG

        return log_level

pass_state = click.make_pass_decorator(AppContext, ensure=True)

def verbosity_option(f):
    def callback(ctx: Context, param, value):
        state = ctx.ensure_object(AppContext)
        state.verbose = value
        return value
    return click.option('-v', '--verbose', count=True,
                        help='Enables verbose mode. The more -v options, the more verbose, up to -vv',
                        is_eager=False,
                        expose_value=False,
                        callback=callback)(f)

def silent_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(AppContext)
        state.silent = value
        return value
    return click.option('-s', '--silent', count=True,
                        help='Disable all output except errors. To disable errors, use -sss',
                        is_eager=True,
                        expose_value=False,
                        callback=callback)(f)

def common_options(f):
    f = verbosity_option(f)
    f = silent_option(f)
    return f


# def pass_custom_context(f):
#     @click.pass_context
#     def new_func(ctx: Context, *args, **kwargs):
#         if ctx.obj is None:
#             ctx.obj = CustomContext()
#         return ctx.invoke(f, ctx.obj, *args, **kwargs)
#
#     return new_func


# @dataclass
# class CustomContext(object):
#     verbose: int = 0
#     silent: int = 0
#     @property
#     def log_level(self)->int:
#         log_level = logging.WARNING
#
#         if self.silent == 1:
#             log_level = logging.ERROR
#         elif self.silent == 2:
#             log_level = logging.CRITICAL
#         elif self.silent >= 3:
#             log_level = logging.CRITICAL + 1
#         elif self.verbose == 0:
#             # Default value set before the if
#             pass
#         elif self.verbose == 1:
#             log_level = logging.INFO
#         elif self.verbose == 2:
#             log_level = logging.DEBUG
#
#         return log_level




ORIGINAL_STDOUT = sys.stdout
ORIGINAL_STDERR = sys.stderr
DEVNULL_STDOUT = click.open_file(os.devnull, 'w')
DEVNULL_STDERR = click.open_file(os.devnull, 'w')

def common_params(func):
    # @pass_custom_context
    @common_options
    @functools.wraps(func)
    @pass_state
    def wrapper(state: AppContext, *args, **kwargs):
        from mobt.Logging.logging_utils import set_log_level
        log_level = state.log_level
        set_log_level(log_level)

        if log_level > logging.CRITICAL:
            sys.stdout = DEVNULL_STDOUT
            sys.stderr = DEVNULL_STDERR
        else:
            sys.stdout = ORIGINAL_STDOUT
            sys.stderr = ORIGINAL_STDERR

        return func(*args, **kwargs)

    return wrapper
