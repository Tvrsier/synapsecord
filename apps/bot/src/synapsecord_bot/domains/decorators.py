from functools import wraps
from typing import ParamSpec, TypeVar, Awaitable, Callable

from synapsecord_bot.context.base import SynapseContextMixin
from synapsecord_bot.domains import RequiredDomainMissingError

P = ParamSpec("P")
R = TypeVar("R")

def _find_context(args: tuple[object, ...]) -> SynapseContextMixin:
    for arg in args:
        if isinstance(arg, SynapseContextMixin):
            return arg

    raise RuntimeError(f"Synapse context not found in decorated callback")

def requires(*domain_types: type[object]) -> Callable[
    [Callable[P, Awaitable[R]]],
    Callable[P, Awaitable[R]]
]:
    def decorator(callback: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(callback)
        async def wrapper(*args: P.args, **words: P.kwargs) -> R:
            ctx = _find_context(args)

            for domain_type in domain_types:
                domain = await ctx.services.domain_resolution.resolve(ctx, domain_type)

                if domain is None:
                    raise RequiredDomainMissingError(domain_type)

            return await callback(*args, **words)
        return wrapper
    return decorator

def inject(*domain_types: type[object]) -> Callable[
    [Callable[P, Awaitable[R]]],
    Callable[P, Awaitable[R]]
]:
    def decorator(callback: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(callback)
        async def wrapper(*args: P.args, **words: P.kwargs) -> R:
            ctx = _find_context(args)

            for domain_type in domain_types:
                await ctx.services.domain_resolution.resolve(ctx, domain_type)

            return await callback(*args, **words)
        return wrapper
    return decorator