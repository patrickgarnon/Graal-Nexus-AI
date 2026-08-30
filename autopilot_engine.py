import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable, Coroutine, List, Optional, Tuple


@dataclass
class TaskSpec:
    """Describe a unit of work for the AutopilotEngine.

    Attributes:
        name: Identifier for the task; used in error reporting.
        func: Callable or coroutine function representing the work.
        mode: Selects the execution strategy. Accepted values are
            ``"async"`` for native coroutines, ``"thread"`` for I/O
            bound callables and ``"process"`` for CPU bound callables.
        args: Positional arguments forwarded to ``func``.
        kwargs: Keyword arguments forwarded to ``func``.
    """

    name: str
    func: Callable[..., Any] | Coroutine[Any, Any, Any]
    mode: str = "async"
    args: Tuple[Any, ...] = ()
    kwargs: dict[str, Any] = None

    def __post_init__(self) -> None:
        if self.kwargs is None:
            self.kwargs = {}


@dataclass
class TaskResult:
    """Result object returned for each executed task."""

    name: str
    success: bool
    result: Any = None
    error: Optional[BaseException] = None


class AutopilotEngine:
    """Execute tasks concurrently using asyncio or executor pools.

    The engine selects the most appropriate execution model for each
    :class:`TaskSpec` based on its ``mode`` attribute. Errors are captured
    per task and returned in :class:`TaskResult` objects, ensuring
    isolated error tracking.
    """

    def __init__(self, max_workers: Optional[int] = None) -> None:
        self.loop = asyncio.get_event_loop()
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=max_workers)

    async def _run_async(self, spec: TaskSpec) -> TaskResult:
        try:
            result = await spec.func(*spec.args, **spec.kwargs)
            return TaskResult(name=spec.name, success=True, result=result)
        except BaseException as exc:  # pylint: disable=broad-except
            return TaskResult(name=spec.name, success=False, error=exc)

    async def _run_in_executor(self, spec: TaskSpec, executor: ThreadPoolExecutor | ProcessPoolExecutor) -> TaskResult:
        try:
            bound = lambda: spec.func(*spec.args, **spec.kwargs)
            result = await self.loop.run_in_executor(executor, bound)
            return TaskResult(name=spec.name, success=True, result=result)
        except BaseException as exc:  # pylint: disable=broad-except
            return TaskResult(name=spec.name, success=False, error=exc)

    async def run(self, tasks: List[TaskSpec]) -> List[TaskResult]:
        """Execute all provided tasks concurrently.

        Args:
            tasks: A list of :class:`TaskSpec` describing the work to run.

        Returns:
            A list of :class:`TaskResult` instances in the same order as
            the supplied ``tasks`` list.
        """

        coros: List[Coroutine[Any, Any, TaskResult]] = []
        for spec in tasks:
            if spec.mode == "async":
                coros.append(self._run_async(spec))
            elif spec.mode == "thread":
                coros.append(self._run_in_executor(spec, self.thread_pool))
            elif spec.mode == "process":
                coros.append(self._run_in_executor(spec, self.process_pool))
            else:
                raise ValueError(f"Unknown task mode: {spec.mode}")

        return await asyncio.gather(*coros)

    def shutdown(self) -> None:
        """Release all executor resources."""
        self.thread_pool.shutdown(wait=False)
        self.process_pool.shutdown(wait=False)
