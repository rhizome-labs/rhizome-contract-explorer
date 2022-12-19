from fastapi import APIRouter, Request
from iconsdk.exception import JSONRPCException

from rhizome_contract_explorer import TEMPLATES
from rhizome_contract_explorer.app.icx import Icx

router = APIRouter(prefix="/contract")


@router.get("/{contract_address}/")
async def get_index(
    request: Request,
    contract_address: str = None,
    block_height: int = None,
):
    icx = Icx()
    try:
        score_name = icx.get_score_name(contract_address)
    except JSONRPCException:
        score_name = None
    score_status = icx.get_score_status(contract_address)
    return TEMPLATES.TemplateResponse(
        "contract/index.html",
        {
            "request": request,
            "contract_address": contract_address,
            "block_height": block_height,
            "score_name": score_name,
            "score_status": score_status,
        },
    )


@router.get("/{contract_address}/inspector/")
async def get_contract_methods(
    request: Request,
    type: str,
    contract_address: str = None,
):
    icx = Icx()
    abi = icx.get_score_api(contract_address)

    read_methods = [method for method in abi if method.get("readonly") == "0x1"]
    write_methods = [method for method in abi if method.get("readonly") != "0x1"]

    # Sort methods by alphabetical order.
    read_methods.sort(key=lambda x: x["name"].casefold())
    write_methods.sort(key=lambda x: x["name"].casefold())

    return TEMPLATES.TemplateResponse(
        "contract/inspector.html",
        {
            "request": request,
            "contract_address": contract_address,
            "read_methods": read_methods,
            "write_methods": write_methods,
            "type": type,
        },
    )


@router.get("/{contract_address}/methods/")
async def get_contract_methods(
    request: Request,
    contract_address: str = None,
    filter: str = "all",
):
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