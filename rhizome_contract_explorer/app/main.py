import json
import os
from decimal import Decimal

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from iconsdk.exception import JSONRPCException

from rhizome_contract_explorer import ENV, TEMPLATES
from rhizome_contract_explorer.app.icx import Icx

app = FastAPI(docs_url=None)

# Mount /static folder
app.mount(
    "/assets",
    StaticFiles(
        directory=f"{os.path.dirname(__file__)}/static",
        html=True,
    ),
    name="static",
)


@app.get("/")
async def get_index(
    request: Request,
    contract_address: str = None,
    block_height: int = None,
):
    # If API endpoint is not provided, check environment variable.
    api_endpoint = ENV.get("API_ENDPOINT")

    # If network is not provided, check environment variable.
    network_id = int(ENV.get("NID"))

    # Initialize Icx instance.
    icx = Icx()
    icx_balance = icx.get_balance(icx.wallet_address)

    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Home",
            "contract_address": contract_address,
            "block_height": block_height,
            "api_endpoint": api_endpoint,
            "network_id": network_id,
            "icx_address": icx.wallet_address,
            "icx_balance": round(Decimal(icx_balance) / Decimal(10**18), 4),
        },
    )


@app.post("/abi/")
async def post_abi(request: Request):

    if "PRIVATE_KEY" in ENV.keys():
        mode = "read-write"
    else:
        mode = "read-only"

    # Parse incoming form data.
    form_data = await request.form()

    # Get contract address from form data.
    try:
        block_height = int(form_data["block_height"])
    except:
        block_height = None

    contract_address = form_data["contract_address"]

    if len(contract_address) != 42 or not contract_address.startswith("cx"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid contract address.",
        )

    icx = Icx()

    try:
        abi = icx.get_score_api(contract_address, block_height)
    except JSONRPCException as e:
        return TEMPLATES.TemplateResponse(
            "error.html",
            {
                "request": request,
                "message": f"{contract_address} did not exist at Block #{block_height:,}",
            },
        )

    read_methods = [method for method in abi if method.get("readonly") == "0x1"]
    write_methods = [method for method in abi if method.get("readonly") != "0x1"]

    return TEMPLATES.TemplateResponse(
        "abi.html",
        {
            "request": request,
            "contract_address": contract_address,
            "block_height": block_height,
            "read_methods": sorted(read_methods, key=lambda x: x["name"]),
            "write_methods": sorted(write_methods, key=lambda x: x["name"]),
            "mode": mode,
        },
    )


@app.get("/latest-block/")
def get_latest_block(request: Request):
    icx = Icx()
    block_height = icx.get_block(height_only=True)
    return TEMPLATES.TemplateResponse(
        "block_height.html",
        {
            "request": request,
            "block_height": f"{block_height:,}",
        },
    )


@app.get("/validate-input/")
def validate_input(request: Request, type: str):
    return


@app.get("/call/")
def get_call(
    request: Request,
    contract_address: str,
    method_name: str,
    block_height: int | str = None,
):
    # Convert block height from string None to a proper None instance.
    block_height = None if block_height == "None" else block_height

    icx = Icx()

    try:
        result = icx.call(contract_address, method=method_name, height=block_height)
    except JSONRPCException:
        return "<p>ERROR!</p>"

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
        },
    )


@app.post("/tx/")
async def post_tx(
    request: Request,
    contract_address: str,
    method_name: str,
    value: int = 0,
):
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
            "tx_hash": tx_hash,
        },
    )
