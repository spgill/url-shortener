# <img src="/public/favicon.png?raw=true" style="height: 24px;" /> URL Shortener (API + UI)

## Installation

You can build the docker image yourself by cloning this repo and running a standard Docker build command;

```bash
docker build -t <TAG> .
```

This build will automatically install node and python dependencies, and build the web UI from source.

... or you can pull a pre-built image from my private Docker image repo at `docker.spgill.me` like so;

```bash
docker pull docker.spgill.me/url-shortener:latest
```

## Usage

This application is completely stateless; all of its behavior can be completely configured via environment variables, and all of the stateful information (the shortened URLs) will be stored in a MongoDB database.

This application runs an HTTP/1.1 server on **TCP port 5000**.

This application can read HTTP request headers from a reverse proxy to perform user and (optionally) group authentication. I personally run this app behind a Traefik reverse proxy with an Authelia middleware for authentication.

Example `docker run` command;

```bash
docker run --rm -e "SHORT_EXTERNAL_ADDRESS=https://example.com" -e "SHORT_MONGODB_URI=mongodb://user:pass@example.com/db_name" -p 5000:5000 docker.spgill.me/url-shortener
```

### Environment variables

| Name | Required? | Default value | Example value | Description |
| - | - | - | - | - |
| `SHORT_EXTERNAL_ADDRESS` | yes | | "https://example.com" | External root address for shortened links. Must include the URL scheme (http / https). |
| `SHORT_TOKEN_PREFIX` | no | "" | "lol" | Prefix to apply before every shortened URL token. |
| `SHORT_TOKEN_LENGTH` | no | "4" | "6" | Length of randomized token for shortened URL. |
| `SHORT_MONGODB_URI` | yes | | "mongodb://example.com?ssl=true&authSource=admin" | MongoDB connection URI for the database. |
| `SHORT_MONGODB_COLLECTION` | no | "urls" | "short_urls" | Name of collection in the database to use. Will be created if it does not exist. |
| `SHORT_AUTH_ENABLED` | no | "false" | "true" | Enable use of proxy authentication headers for tracking creation of shortened URLs. If enabled, API requests will fail when this header is not present. If not enabled, the `creator` field in the DB documents will be undefined. |
| `SHORT_AUTH_USER_HEADER` | no | "Remote-User" | "X-Proxy-User" | HTTP request header to parse for the authenticated username. |
| `SHORT_AUTH_GROUPS_HEADER` | no | "Remote-Groups" | "X-Proxy-Groups" | HTTP request header to parse for the authenticated user's groups. Value must be in the form of a comma-delimited list. |
| `SHORT_AUTH_GROUP` | no | "" | "admin" | Group name to check user's membership of in order to allow URLs to be shortened. If this value is not set, a group will not be required for the authenticated user. |
| `SHORT_UI_ENABLED` | no | "true" | "false" | If this value is set to `false`, the web UI will not be available. Only the API routes will respond to requests. |

### API syntax

URLs can be shortened directly via an HTTP request to the built-in API.

#### Shortening a URL
`PUT /api` with an `application/json` body in the format
```typescript
{
  url: string; // Required. URL to shorten.
  format?: "normal" | "noscheme" | "token"; // Optional. Defaults to "normal". Scheme of resulting shortened URL.
}
```

Example request in JavaScript;
```typescript
fetch("http://localhost:5000/api", {
  "method": "PUT",
  "headers": {
    "content-type": "application/json"
  },
  "body": JSON.stringify(
    {
      "url": "https://google.com"
    }
  )
});
```

----------

## Development

TBD
