from fastapi import APIRouter, HTTPException, Query, Request, status
from iconsdk.exception import JSONRPCException

from rhizome_contract_explorer import CONFIG, MODE, TEMPLATES
from rhizome_contract_explorer.app.icx import Icx
from rhizome_contract_explorer.app.utils import Utils

router = APIRouter(prefix="/contract")


@router.get("/{contract_address}/")
async def get_contract(
    request: Request,
    contract_address: str = None,
    block_height: int = None,
):
    # Raise HTTP exception if contract address is not valid.
    if Utils.validate_contract_address(contract_address) is False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{contract_address} is not a valid contract address.",
        )

    icx = Icx()

    try:
        score_status = icx.get_score_status(contract_address)
    except JSONRPCException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{contract_address} was not found on this network (api_endpoint: {CONFIG.api_endpoint}, network_id: {CONFIG.network_id}).",
        )

    # Check if SCORE has a name. If it doesn't, set score_name to None.
    try:
        score_name = icx.get_score_name(contract_address)
    except JSONRPCException:
        score_name = None

    return TEMPLATES.TemplateResponse(
        "contract/index.html",
        {
            "request": request,
            "mode": MODE,
            "contract_address": contract_address,
            "block_height": block_height,
            "score_name": score_name,
            "score_status": score_status,
        },
    )


@router.get("/{contract_address}/inspector/")
async def get_contract_methods(
    request: Request,
    type: str = Query(...),
    contract_address: str = None,
):

    # Raise HTTP exception if contract address is not valid.
    if Utils.validate_contract_address(contract_address) is False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{contract_address} is not a valid contract address.",
        )

    icx = Icx()
    abi = icx.get_score_api(contract_address)

    # Sort methods by alphabetical order.
    if type == "read":
        methods = [method for method in abi if method.get("readonly") == "0x1"]
    if type == "write":
        methods = [method for method in abi if method.get("readonly") != "0x1"]

    methods.sort(key=lambda x: x["name"].casefold())

    return TEMPLATES.TemplateResponse(
        "contract/inspector.html",
        {
            "request": request,
            "mode": MODE,
            "contract_address": contract_address,
            "methods": methods,
            "type": type,
        },
    )


@router.get("/{contract_address}/methods/")
async def get_contract_methods(
    request: Request,
    contract_address: str = None,
    filter: str = "all",
):
    # Raise HTTP exception if contract address is not valid.
    if Utils.validate_contract_address(contract_address) is False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{contract_address} is not a valid contract address.",
        )

    icx = Icx()
    abi = icx.get_score_api(contract_address)

    read_methods = [method for method in abi if method.get("readonly") == "0x1"]
    write_methods = [method for method in abi if method.get("readonly") != "0x1"]

    # Sort methods by alphabetical order.
    read_methods.sort(key=lambda x: x["name"].casefold())
    write_methods.sort(key=lambda x: x["name"].casefold())

    return TEMPLATES.TemplateResponse(
        "contract/methods_list.html",
        {
            "request": request,
            "contract_address": contract_address,
            "read_methods": read_methods,
            "write_methods": write_methods,
            "filter": filter,
        },
    )


@router.get("/{contract_address}/overview/")
async def get_contract_methods(
    request: Request,
    contract_address: str = None,
):
    # Raise HTTP exception if contract address is not valid.
    if Utils.validate_contract_address(contract_address) is False:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{contract_address} is not a valid contract address.",
        )

    icx = Icx()
    score_name = icx.get_score_name(contract_address)
    score_status = icx.get_score_status(contract_address)
    return TEMPLATES.TemplateResponse(
        "contract/overview.html",
        {
            "request": request,
            "score_name": score_name,
            "score_status": score_status,
        },
    )
