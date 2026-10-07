"""Дедлайны и таймауты. Используем concurrent.futures.Timeout для кросс-платформ."""

from __future__ import annotations

import concurrent.futures


def run_with_timeout(fn, timeout_s: float, *args, **kwargs):
    """Запускает fn в треде, ждёт timeout_s. Бросает TimeoutError при превышении."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(fn, *args, **kwargs)
        try:
            return fut.result(timeout=timeout_s)
        except concurrent.futures.TimeoutError as e:
            fut.cancel()
            raise TimeoutError(f"timed out after {timeout_s:.1f}s") from e
