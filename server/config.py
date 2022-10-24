# stdlib imports
import os
import typing


def _getOptional(name: str, default: str) -> str:
    return os.environ.get(name, default)


def _getRequired(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise RuntimeError(f"'{name}' is a required environment variable!")
    return value


alphabet = "abcdefghjkmmnpqrstuvwxyzABCDEFGHJKMMNPQRSTUVWXYZ2346789"

externalAddress = _getOptional("SHORT_EXTERNAL_ADDRESS", "http://example.com")
tokenPrefix = _getOptional("SHORT_TOKEN_PREFIX", "")
tokenLength = int(_getOptional("SHORT_TOKEN_LENGTH", "4"))

mongoDbUri = _getRequired("SHORT_MONGODB_URI")
mongoDbCollection = _getOptional("SHORT_MONGODB_COLLECTION", "urls")

authEnabled = _getOptional("SHORT_AUTH_ENABLED", "false").lower() == "true"
authUserHeader = _getOptional("SHORT_AUTH_USER_HEADER", "Remote-User")
authGroupsHeader = _getOptional("SHORT_AUTH_GROUPS_HEADER", "Remote-Groups")
authRequiredGroup = _getOptional("SHORT_AUTH_GROUP", "")

print(f"Entropy level: {len(alphabet) ** tokenLength}")
