from decimal import Decimal
from functools import lru_cache
from getpass import getpass
from time import sleep
from typing import Tuple

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import (
    CallTransactionBuilder,
    TransactionBuilder,
)
from iconsdk.exception import JSONRPCException, KeyStoreException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction, Transaction
from iconsdk.wallet.wallet import KeyWallet

from rhizome_contract_caller import ENV


class Icx:
    def __init__(self) -> None:
        self.icon_service = self._get_icon_service(ENV["API_ENDPOINT"])
        self.nid = int(ENV["NID"])
        self.wallet = self._load_wallet()
        self.wallet_address = self.wallet.get_address()

    def call(
        self,
        to: str,
        method: str,
        params: dict = {},
        height: int = None,
    ) -> dict:
        call = CallBuilder().to(to).method(method).params(params).height(height).build()
        result = self.icon_service.call(call)
        return result

    def get_block(
        self,
        block_height: int = "latest",
        height_only: bool = False,
    ) -> dict | int:
        block = self.icon_service.get_block(block_height)
        if height_only is True:
            return block["height"]
        return block

    def get_score_api(
        self,
        contract_address: str,
        block_height: int = None,
    ) -> dict:
        """
        Returns the ABI for a SCORE on the ICON blockchain.

        Args:
            contract_address: The contract to get the ABI for.
            block_height: The block height to query.
        """
        result = self.icon_service.get_score_api(contract_address, block_height)
        return result

    def _get_icon_service(self, api_endpoint: str) -> IconService:
        icon_service = IconService(HTTPProvider(api_endpoint, 3))
        return icon_service

    def build_transaction(
        self,
        to: str,
        value: int,
    ) -> Transaction:
        tx = (
            TransactionBuilder()
            .from_(self.wallet_address)
            .to(to)
            .value(int(value * 10**18))
            .nid(self.nid)
            .build()
        )
        return tx

    def build_call_transaction(
        self,
        to: str,
        value: int = 0,
        method: str = None,
        params: dict = {},
    ):
        transaction = (
            CallTransactionBuilder()
            .from_(self.wallet_address)
            .to(to)
            .value(int(value))
            .nid(self.nid)
            .method(method)
            .params(params)
            .build()
        )
        return transaction

    def send_transaction(
        self,
        tx: Transaction,
        verify_result: bool = True,
    ) -> str:
        signed_tx = SignedTransaction(tx, self.wallet, 100_000_000)
        tx_hash = self.icon_service.send_transaction(signed_tx)
        if verify_result is True:
            for _ in range(10):
                tx_result = self.is_transaction_successful(tx_hash)
                if tx_result is True:
                    return tx_hash
                else:
                    sleep(1)
                    continue
        return tx_hash

    def is_transaction_successful(self, tx_hash: str) -> bool:
        try:
            result = self.icon_service.get_transaction_result(tx_hash)
            print(result)
            tx_status = result["status"]
            if tx_status == 1:
                return True
            else:
                return False
        except JSONRPCException:
            return False

    def _load_wallet(self) -> KeyWallet:
        wallet = KeyWallet.load(bytes.fromhex(ENV["PRIVATE_KEY"]))
        return wallet
