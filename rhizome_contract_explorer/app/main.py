import json
import os
from decimal import Decimal
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from iconsdk.exception import JSONRPCException

from rhizome_contract_explorer import CONFIG, MODE, TEMPLATES
from rhizome_contract_explorer.app.icx import Icx
from rhizome_contract_explorer.app.routers import contract

app = FastAPI(docs_url=None)

app.include_router(contract.router)

# Mount /static folder
app.mount(
    "/assets",
    StaticFiles(
        directory=f"{os.path.dirname(__file__)}/static",
        html=True,
    ),
    name="static",
)


@app.get("/latest-block/")
async def get_latest_block(request: Request):
    icx = Icx()
    block_height = icx.get_block(height_only=True)
    return TEMPLATES.TemplateResponse(
        "latest_block.html",
        {
            "request": request,
            "block_height": f"{block_height:,}",
            "block_refresh": CONFIG.block_refresh,
        },
    )


@app.get("/call/")
async def get_call(
    request: Request,
    contract_address: str,
    method_name: str,
    block_height: int | str = None,
):
    # Convert block height from string None to a proper None instance.
    block_height = None if block_height == "None" else block_height

    icx = Icx()

    is_error = False

    try:
        result = icx.call(contract_address, method=method_name, height=block_height)
    except JSONRPCException as e:
        result = e.args[0]
        is_error = True

    is_json = False

    if isinstance(result, str):
        if result.startswith("0x"):
            try:
                result = int(result, 16)
            except ValueError:
                pass

    if isinstance(result, dict):
        result = json.dumps(result, indent=4)
        is_json = True

    return TEMPLATES.TemplateResponse(
        "call_result.html",
        {
            "request": request,
            "result": result,
            "is_json": is_json,
            "is_error": is_error,
        },
    )


@app.post("/call/")
async def post_call(
    request: Request,
    contract_address: str,
    method_name: str,
    block_height: int | str = None,
):
    # Convert block height from string None to a proper None instance.
    block_height = None if block_height == "None" else block_height

    # Parse form data.
    form_data = await request.form()

    # Only parse form data is there is form data to parse.
    if len(form_data) > 0:
        form_data_dict = form_data.items()

        # Build params object for transaction.
        params = {param[0]: param[1] for param in form_data_dict}

        # Perform validation on input values.
        for k, v in params.items():
            if not k.endswith(":type"):
                param_type = params[f"{k}:type"]
                try:
                    if param_type == "address":
                        if len(v) != 42 or v[:2] != "hx":
                            raise ValueError
                    elif param_type == "int":
                        params[k] = int(v)
                    elif param_type == "str":
                        params[k] = str(v)
                except ValueError:
                    return f"<p>ValueError - {k, v}</p>"

        # Strip :type items from params.
        params = {k: v for k, v in params.items() if not k.endswith(":type")}
    else:
        params = {}

    # Initialize Icx instance.
    icx = Icx()

    try:
        result = icx.call(
            contract_address,
            method=method_name,
            params=params,
            height=block_height,
        )
    except JSONRPCException as e:
        result = e.args[0]

    if isinstance(result, str):
        if result.startswith("0x"):
            try:
                result = int(result, 16)
            except ValueError:
                pass

    if isinstance(result, dict):
        result = json.dumps(result, indent=4)

    return TEMPLATES.TemplateResponse(
        "call_result.html",
        {
            "request": request,
            "result": result,
        },
    )


@app.post("/tx/")
async def post_tx(
    request: Request,
    contract_address: str,
    method_name: str,
    value: int = 0,
):
    if MODE != "RW":
        return TEMPLATES.TemplateResponse(
            "tx_result.html",
            {
                "request": request,
                "result": "ERROR: Transactions are disabled because no private key has been specified.",
            },
        )

    # Parse form data.
    form_data = await request.form()

    # Only parse form data is there is form data to parse.
    if len(form_data) > 0:
        form_data_dict = form_data.items()

        # Build params object for transaction.
        params = {param[0]: param[1] for param in form_data_dict}

        # Perform validation on input values.
        for k, v in params.items():
            if not k.endswith(":type"):
                param_type = params[f"{k}:type"]
                try:
                    if param_type == "address":
                        if len(v) != 42 or v[:2] != "hx":
                            raise ValueError
                    elif param_type == "int":
                        params[k] = int(v)
                    elif param_type == "str":
                        params[k] = str(v)
                except ValueError:
                    return f"<p>ValueError - {k, v}</p>"

        # Strip :type items from params.
        params = {k: v for k, v in params.items() if not k.endswith(":type")}
    else:
        params = {}

    # Initialize Icx instance.
    icx = Icx()

    # Build and send transaction.
    tx = icx.build_call_transaction(contract_address, value, method_name, params)
    tx_hash = icx.send_transaction(tx)

    return TEMPLATES.TemplateResponse(
        "tx_result.html",
        {
            "request": request,
            "result": tx_hash,
        },
    )
