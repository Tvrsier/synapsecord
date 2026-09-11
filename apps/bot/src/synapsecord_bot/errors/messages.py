from synapsecord_bot.domains import RequiredDomainMissingError


def get_error_message(error: Exception) -> str | None:
    if isinstance(error, RequiredDomainMissingError):
        return(
            f"Required domain "
            f"{error.domain_type.__name__} "
            "cloud not be resolved"
        )

    return None