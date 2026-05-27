import logging
from contextlib import contextmanager
from typing import Any, Iterator

import config

logger = logging.getLogger(__name__)

_INITIALIZED = False
_TRACING_ENABLED = False
_TRACER = None


def initialize_tracing() -> bool:
    global _INITIALIZED, _TRACING_ENABLED, _TRACER

    if _INITIALIZED:
        return _TRACING_ENABLED

    _INITIALIZED = True
    if not config.PHOENIX_ENABLED:
        return False

    try:
        from opentelemetry import trace
        from phoenix.otel import register

        kwargs: dict[str, Any] = {
            "project_name": config.PHOENIX_PROJECT_NAME,
            "protocol": config.PHOENIX_PROTOCOL,
            "batch": True,
            "verbose": False,
        }
        if config.PHOENIX_COLLECTOR_ENDPOINT:
            kwargs["endpoint"] = config.PHOENIX_COLLECTOR_ENDPOINT
        if config.PHOENIX_API_KEY:
            kwargs["api_key"] = config.PHOENIX_API_KEY

        register(**kwargs)
        _TRACER = trace.get_tracer(config.PHOENIX_PROJECT_NAME)
        _TRACING_ENABLED = True
        logger.info(
            "Phoenix tracing active — project=%s endpoint=%s",
            config.PHOENIX_PROJECT_NAME,
            config.PHOENIX_COLLECTOR_ENDPOINT,
        )
        return True
    except Exception as exc:
        logger.warning("Could not initialize Phoenix tracing: %s", exc)
        _TRACING_ENABLED = False
        _TRACER = None
        return False


def is_tracing_enabled() -> bool:
    return _TRACING_ENABLED


@contextmanager
def start_span(name: str, **attributes: Any) -> Iterator[Any]:
    if not _TRACING_ENABLED or _TRACER is None:
        yield None
        return

    with _TRACER.start_as_current_span(name) as span:
        for key, value in attributes.items():
            if value is not None:
                span.set_attribute(key, value)
        try:
            yield span
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(
                __import__("opentelemetry.trace", fromlist=["Status", "StatusCode"]).Status(
                    __import__("opentelemetry.trace", fromlist=["StatusCode"]).StatusCode.ERROR,
                    str(exc),
                )
            )
            raise


def add_span_attributes(span: Any, **attributes: Any) -> None:
    if span is None:
        return
    for key, value in attributes.items():
        if value is not None:
            span.set_attribute(key, value)
