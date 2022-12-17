# RHIZOME Contract Explorer

RHIZOME Contract Explorer is a standalone web application for querying and interacting with smart contracts on the ICON blockchain. We recommend only using RHIZOME Contract Explorer in a safe and audited LOCAL ENVIRONMENT because it does not use a web wallet or keystore/password combination for signing transactions. Instead, RHIZOME Contract Explorer expects an ICX private key to be assigned to an environment variable – we specifically designed the application this way to optimize the user experience for interacting with smart contracts in a secure and controlled environment.

Architecturally speaking, RHIZOME Contract Explorer is a FastAPI web application that streams HTML to and from the server using HTMX and hyperscript. Unlike traditional blockchain application frontends, RHIZOME Contract Explorer does not make use of client-side JavaScript libraries such as React and Vue.

## Installation

```
poetry install
```

For users who prefer to use Docker, a barebones Dockerfile is included in the repository.

## Usage

```
bash run.sh
```

## Notes

* If no private key is set, RHIZOME Contract Explorer will operate in "read-only" mode. In this mode, the application can only query the blockchain.