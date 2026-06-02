import json
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Callable


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


_current_run_id: ContextVar[str | None] = ContextVar("agent_run_id", default=None)
_event_sink: Callable[[str, str, dict], None] | None = None


def set_current_run_id(run_id: str | None):
    return _current_run_id.set(run_id)


def reset_current_run_id(token) -> None:
    _current_run_id.reset(token)


def get_current_run_id() -> str | None:
    return _current_run_id.get()


def set_event_sink(sink: Callable[[str, str, dict], None] | None) -> None:
    global _event_sink
    _event_sink = sink


@contextmanager
def run_context(run_id: str | None):
    token = set_current_run_id(run_id)
    try:
        yield
    finally:
        reset_current_run_id(token)


def log_event(logger: logging.Logger, event: str, **fields) -> None:
    payload = {"event": event, **fields}
    logger.info(json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str))
    run_id = get_current_run_id()
    if run_id and _event_sink is not None:
        try:
            _event_sink(run_id, event, fields)
        except Exception as exc:
            logger.debug("failed to persist run event %s: %s", event, exc)
