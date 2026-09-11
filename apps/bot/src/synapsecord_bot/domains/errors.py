from __future__ import annotations

from discord import ApplicationCommandError
from discord.ext.commands import CommandError


class MissingDomainError(LookupError):
    def __init__(self, domain_type: type[object]) -> None:
        self.domain_type = domain_type

        super().__init__(
            f"Domain {domain_type.__name__} is not available in this context."
        )


class DomainResolverNotRegisteredError(LookupError):
    def __init__(self, domain_type: type[object]) -> None:
        self.domain_type = domain_type

        super().__init__(
            f"No resolver registered for domain {domain_type.__name__}."
        )


class DomainResolverAlreadyRegisteredError(ValueError):
    def __init__(self, domain_type: type[object]) -> None:
        self.domain_type = domain_type

        super().__init__(
            f"A resolver for domain {domain_type.__name__} is already registered."
        )


class CircularDomainResolutionError(RuntimeError):
    def __init__(self, domain_type: type[object]) -> None:
        self.domain_type = domain_type

        super().__init__(
            f"Circular resolution detected for domain {domain_type.__name__}."
        )


class RequiredDomainMissingError(CommandError, ApplicationCommandError):
    def __init__(self, domain_type: type[object]) -> None:
        self.domain_type = domain_type
        super().__init__(
            f"Required domain {domain_type.__name__} could not be resolved."
        )