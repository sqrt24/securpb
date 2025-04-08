from jinja2 import Environment

from core.utils.text import price2human, round_value

env = None


def environment(**options) -> Environment:
    env = Environment(
        **options,
        comment_start_string="{=",
        comment_end_string="=}",
    )

    env.globals.update(price2human=price2human, round_value=round_value)
    return env


def render_jinja_string(string: str, **context):
    global env
    if env is None:
        env = environment()
    try:
        return env.from_string(string).render(**context)
    except Exception:
        return string
