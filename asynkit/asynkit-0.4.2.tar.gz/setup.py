# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asynkit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asynkit',
    'version': '0.4.2',
    'description': 'Async toolkit for advanced scheduling',
    'long_description': '# asynkit: a toolkit for coroutines\n\n[![CI](https://github.com/kristjanvalur/py-asynkit/actions/workflows/ci.yml/badge.svg)](https://github.com/kristjanvalur/py-asynkit/actions/workflows/ci.yml)\n\nThis module provides some handy tools for those wishing to have better control over the\nway Python\'s `asyncio` module does things\n\n## Installation\n\n```bash\n$ pip install asynkit\n```\n\n## Coroutine Tools\n\n### `eager()` - lower latency IO\n\nDid you ever wish that your _coroutines_ started right away, and only returned control to\nthe caller once they become blocked?  Like the way the `async` and `await` keywords work in the __C#__ language?\n\nNow they can.  Just decorate or convert them with `acynkit.eager`:\n\n```python\n@asynkit.eager\nasync def get_slow_remote_data():\n    result = await execute_remote_request()\n    return result.important_data\n\nasync def my_complex_thing():\n    # kick off the request as soon as possible\n    future = get_slow_remote_data()\n    # The remote execution may now already be in flight. Do some work taking time\n    intermediate_result = await some_local_computation()\n    # wait for the result of the request\n    return compute_result(intermediate_result, await future)\n```\n\nBy decorating your function with `eager`, the coroutine will start executing __right away__ and\ncontrol will return to the calling function as soon as it _suspends_, _returns_, or _raises_\nan exception.  In case it is suspended, a _Task_ is created and returned, ready to resume\nexecution from that point.\n\nNotice how, in either case, control is returned __directly__ back to the\ncalling function, maintaining synchronous execution.  In effect, conventional code\ncalling order is maintained as much as possible.  We call this _depth-first-execution_.\n\nThis allows you to prepare and dispatch long running operations __as soon as possible__ while\nstill being able to asynchronously wait for the result.\n\n`asynckit.eager` can also be used directly on the returned coroutine:\n```python\nlog = []\nasync def test():\n    log.append(1)\n    await asyncio.sleep(0.2) # some long IO\n    log.append(2)\n\nasync def caller(convert):\n    del log[:]\n    log.append("a")\n    future = convert(test())\n    log.append("b")\n    await asyncio.sleep(0.1) # some other IO\n    log.append("c")\n    await future\n\n# do nothing\nasyncio.run(caller(lambda c:c))\nassert log == ["a", "b", "c", 1, 2]\n\n# Create a Task\nasyncio.run(caller(asyncio.create_task))\nassert log == ["a", "b", 1, "c", 2]\n\n# eager\nasyncio.run(caller(asynkit.eager))\nassert log == ["a", 1, "b", "c", 2]\n```\n\n`eager()` is actually a convenience function, invoking either `coro_eager()` or `async_eager()` (see below) depending on context.\nDecorating your function makes sense if you __always__ intend\nTo _await_ its result at some later point. Otherwise, just apply it at the point\nof invocation in each such case. \n\n### `coro_eager()`, `async_eager()`\n\n`coro_eager()` is the magic coroutine wrapper providing the __eager__ behaviour:\n\n1. It runs `CoroStart.start()` on the coroutine.\n2. It returns `CoroStart.as_future()`.\n\nIf the coroutine finished in step 1 above, the Future is a plain future and the\nresult is immediately available.  Otherwise, a Task is created continuing from\nthe point where the coroutine initially suspended.  In either case, the result\nis an _awaitable_.\n\n`async_eager()` is a decorator which automatically applies `coro_eager()` to the coroutine returned by an async function.\n\n### `CoroStart`\n\nThis class manages the state of a partially run coroutine and is what what powers the `coro_eager()` function.  It has\nthe following methods:\n\n- `start()` runs the coroutine until it either suspends, returns, or raises an exception. It is usually automatically\n  invoked by the class Initializer\n- `resume()` is an async function which continues the execution of the coroutine from the initial state.\n- `is_suspended()` returns true if the coroutine start resulted in it becoming suspended.\n- `as_future()` returns a _future_ with the coroutine\'s results.  If it finished, this is just a plain `Future`,\n  otherwise, it is a `Task`.\n\n## Event loop tools\n\nAlso provided is a mixin for the built-in event loop implementations in python, providing some primitives for advanced\nscheduling of tasks.\n\n### `SchedulingMixin` mixin class\n\nThis class adds some handy scheduling functions to the event loop.  They primarily\nwork with the _ready queue_, a queue of callbacks representing tasks ready\nto be executed.\n\n- `ready_len(self)` - returns the length of the ready queue\n- `ready_pop(self, pos=-1)` - pops an entry off the queue\n- `ready_insert(self, pos, element)` - inserts a previously popped element into the queue\n- `ready_rotate(self, n)` - rotates the queue\n- `call_insert(self, pos, ...)` - schedules a callback at position `pos` in the queue\n\n### Concrete event loop classes\n\nConcrete subclasses of Python\'s built-in event loop classes are provided.\n\n- `SchedulingSelectorEventLoop` is a subclass of `asyncio.SelectorEventLoop` with the `SchedulingMixin`\n- `SchedulingProactorEventLoop` is a subclass of `asyncio.ProactorEventLoop` with the `SchedulingMixin` on those platforms that support it.\n\n### Event Loop Policy\n\nA policy class is provided to automatically create the appropriate event loops.\n\n- `SchedulingEventLoopPolicy` is a subclass of `asyncio.DefaultEventLoopPolicy` which instantiates either of the above event loop classes as appropriate.\n\nUse this either directly:\n\n```python\nasyncio.set_event_loop_policy(asynkit.SchedulingEventLoopPolicy())\nasyncio.run(myprogram())\n```\n\nor with a context manager:\n\n```python\nwith asynkit.event_loop_policy():\n    asyncio.run(myprogram())\n```\n\n## Scheduling functions\n\nA couple of functions are provided making use of these scheduling features.\nThey require a `SchedulingMixin` event loop to be current.\n\n### `sleep_insert(pos)`\n\nSimilar to `asyncio.sleep()` but sleeps only for `pos` places in the runnable queue.\nWhereas `asyncio.sleep(0)` will place the executing task at the end of the queue, which is\nappropriate for fair scheduling, in some advanced cases you want to wake up sooner than that, perhaps\nafter a specific task.\n\n### `task_reinsert(task, pos)`\n\nTakes a _runnable_ task (for example just created with `asyncio.create_task()` or similar) and\nreinserts it at a given position in the queue.  \nSimilarly as for `sleep_insert()`, this can be useful to achieve\ncertain scheduling goals.\n\n### `task_switch(task, result=None, sleep_pos=None)`\n\nImmediately moves the given task to the head of the ready queue and switches to it, assuming it is runnable.\nWhen this call returns, returns `result`.  if `sleep_pos is not None`, the current task will be\nput to sleep at that position, using `sleep_insert()`.  Otherwise the current task is put at the end\nof the ready queue.\n\n### `task_is_blocked(task)`\n\nReturns True if the task is waiting for some awaitable, such as a Future or another Task, and is thus not\non the ready queue.\n\n### `task_is_runnable(task)`\n\nRoughly the opposite of `task_is_blocked()`, returns True if the task is neither `done()` nor __blocked__ and\nawaits execution.\n\n### `create_task_descend(coro)`\n\nImplements depth-first task scheduling.\n\nSimilar to `asyncio.create_task()` this creates a task but starts it running right away, and positions the caller to be woken\nup right after it blocks.  The effect is similar to using `asynkit.eager()` but\nit achieves its goals solely by modifying the runnable queue.  A `Task` is always\ncreated, unlike `eager`, which only creates a task if the target blocks.\n\n## Runnable task helpers\n\nA few functions are added to help working with tasks.\nThey require a `SchedulingMixin` event loop to be current.\n\nThe following identity applies:\n```python\nasyncio.all_tasks(loop) = asynkit.runnable_tasks(loop) | asynkit.blocked_tasks(loop) | {asyncio.current_task(loop)}\n```\n\n### `runnable_tasks(loop=None)`\n\nReturns a set of the tasks that are currently runnable in the given loop\n\n### `blocked_tasks(loop=None)`\n\nReturns a set of the tasks that are currently blocked on some future in the given loop.\n\n## Coroutine helpers\n\nA couple of functions are provided to introspect the state of coroutine objects.  They\nwork on both regular __async__ coroutines, __classic__ coroutines (using `yield from`) and\n__async generators__.  \n\n### `coro_is_new(coro)`\n\nReturns true if the object has just been created and hasn\'t started executing yet\n\n### `coro_is_suspended(coro)`\n\nReturns true if the object is in a suspended state.\n\n### `coro_is_done(coro)`\n\nReturns true if the object has finished executing, e.g. by returning or raising an exception.\n\n### `coro_get_frame(coro)`\n\nReturns the current frame object of the coroutine, if it has one, or `None`.\n',
    'author': 'Kristján Valur Jónsson',
    'author_email': 'sweskman@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kristjanvalur/py-asynkit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
