# stdlib imports
import enum
import hashlib
import pathlib
import re
import secrets
import typing

# vendor imports
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse, PlainTextResponse
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.gzip import GZipMiddleware
import mongoengine

# local imports
from . import config, model


# Create the FastAPI application
app = fastapi.FastAPI()

staticDir = (pathlib.Path(__file__).parent / ".." / "build").resolve()
staticUrl = "/build"

# If the UI is enabled, mount the static directory and static redirect
if config.uiEnabled:
    print("UI is enabled...")
    # Mount static file server for UI build
    app.mount(staticUrl, StaticFiles(directory=staticDir), "static")

    # Default route redirect to build
    @app.get("/")
    def app_default():
        return FileResponse("build/index.html")

else:
    print("UI is disabled...")


# On startup, connect to mongo database
@app.on_event("startup")
def app_startup():
    print("Connecting to MongoDB...")
    mongoengine.connect(host=config.mongoDbUri)
    print("Done")


# On shutdown, close mongo connection
@app.on_event("shutdown")
def app_shutdown():
    print("Disconnecting from MongoDB...")
    mongoengine.disconnect_all()
    print("Done")


@app.get("/{token}")
def app_redirect(token: str):
    # Try to find a shortened url that matches the token, and redirect the client there
    try:
        document = model.ShortURL.objects(token=token).get()
        document.count += 1
        document.save()
        return RedirectResponse(document.resolution, status_code=301)

    # Else, return a 404
    except mongoengine.DoesNotExist:
        raise fastapi.HTTPException(status_code=404)


class ShortenFormat(enum.Enum):
    Normal = "normal"
    Schemeless = "noscheme"
    Token = "token"


class ShortenRequestBody(BaseModel):
    url: str
    format: ShortenFormat = ShortenFormat.Normal


@app.put("/api")
def app_create(request: fastapi.Request, body: ShortenRequestBody):
    url = body.url.strip()

    # Owner starts as None. If auth is enabled, we will resolve this to a username.
    creator = None

    # If auth is enabled, pull the owner from the username header
    if config.authEnabled:
        if config.authUserHeader not in request.headers:
            raise fastapi.HTTPException(status_code=407)
        creator = request.headers[config.authUserHeader]

        # If a particular group is required, check for it
        if config.authRequiredGroup:
            if config.authGroupsHeader not in request.headers:
                raise fastapi.HTTPException(status_code=403)
            groupList = request.headers[config.authGroupsHeader].split(",")
            if config.authRequiredGroup not in groupList:
                raise fastapi.HTTPException(status_code=403)

    # Don't allow empty URLs
    if len(body.url) == 0:
        raise fastapi.HTTPException(status_code=400)

    # Prepend a basic http protocol if none was provided
    if not re.match(r"(^\w+:)?//", url):
        url = "http://" + url

    # Create a hash of the URL
    urlHash = hashlib.blake2b(url.encode("utf8"), digest_size=64).digest()

    # Make sure there isn't already a shortened URL with this hash
    exists = model.ShortURL.objects(resolutionHash=urlHash).first()

    # If it exists, we already have the token
    token: typing.Optional[str]
    if exists:
        token = exists.token

    # Else, we have to create a new entry
    else:
        # Generate a new token and guarantee it doesn't already exist
        while True:
            token = config.tokenPrefix + "".join(
                [secrets.choice(config.alphabet) for n in range(config.tokenLength)]
            )
            if not model.ShortURL.objects(token=token).first():
                break

        # Create a new record for this token
        model.ShortURL(
            token=token,
            resolution=url,
            resolutionHash=urlHash,
            creator=creator,
        ).save()

    # Return only the token if token format is specified
    if body.format is ShortenFormat.Token:
        return PlainTextResponse(token)

    # If schemeless format, return the url without a scheme
    elif body.format is ShortenFormat.Schemeless:
        return PlainTextResponse(
            f"{config.externalAddressParsed.netloc or 'https'}/{token}"
        )

    # Else return the full URL with scheme
    else:
        return PlainTextResponse(
            f"{config.externalAddressParsed.scheme}://{config.externalAddressParsed.netloc or 'https'}/{token}"
        )
