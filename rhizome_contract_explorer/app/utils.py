class Utils:
    @staticmethod
    def validate_contract_address(contract_address: str) -> bool:
        if len(contract_address) == 42 and contract_address.startswith("cx"):
            return True
        else:
            return False
