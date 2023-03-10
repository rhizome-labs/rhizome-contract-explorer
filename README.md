# RHIZOME Contract Explorer

RHIZOME Contract Explorer is a standalone web application for querying and interacting with smart contracts on the ICON blockchain. We recommend only using RHIZOME Contract Explorer in a safe and audited LOCAL ENVIRONMENT because it does not use a web wallet or keystore/password combination for signing transactions. Instead, RHIZOME Contract Explorer expects an ICX private key to be assigned to an environment variable – we specifically designed the application this way to optimize the user experience for interacting with smart contracts in a secure and controlled environment.

Architecturally speaking, RHIZOME Contract Explorer is a FastAPI web application that streams HTML to and from the server using HTMX and hyperscript. Unlike traditional blockchain application frontends, RHIZOME Contract Explorer does not make use of client-side JavaScript libraries such as React and Vue.

## Installation

This project is set up to use Python 3.11 – the latest version of Python. If you do not have Python 3.11 installed on your computer, we recommend insalling pyenv to install and manage a new installation of Python 3.11.

```
poetry install
```

For users who prefer to use Docker, a barebones Dockerfile is included in the repository.

## Usage

If no private key is set, RHIZOME Contract Explorer will operate in "read-only" mode. In this mode, the application can only query the blockchain. To run RHIZOME Contract Explorer in "read-write" mode, create a `.env` file in the project's root directory, add a variable called `PRIVATE_KEY`, and set its value to a valid ICX private key.

To start the app, run the command below:

```
bash run.sh
```