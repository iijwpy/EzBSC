from modules import utils
from web3 import Web3
from eth_account import Account
import time


class Wallet(object):

    def __init__(self, mnemonic: str) -> None:
        Account.enable_unaudited_hdwallet_features()
        self.__private_key = Account.from_mnemonic(mnemonic)._private_key.hex()
        self.__web3 = Web3(Web3.HTTPProvider(utils.BSC))
        self.__private_wallet = self.__web3.eth.account.from_key(self.__private_key).address

    def bnb_balance(self) -> float:
        return float(self.__web3.from_wei(
            self.__web3.eth.get_balance(
                self.__web3.to_checksum_address(self.__private_wallet)
            ),
            'ether'
        ))

    def token_balance_by_address(self, token_address: str) -> float:
        token_data = self.__web3.eth.contract(
            address=self.__web3.to_checksum_address(token_address),
            abi=utils.TOKENNAME_ABI
        )

        balance = token_data.functions.balanceOf(
            self.__web3.to_checksum_address(self.__private_wallet)
        ).call()

        if token_data.functions.decimals().call() == 8:
            return float(self.__web3.from_wei(balance, 'ether') * (10 ** 10))

        return float(self.__web3.from_wei(
            balance,
            utils.get_token_decimal(token_data.functions.decimals().call())
        ))

    def swap_bnb_to_token_by_address(
            self,
            token_address: str,
            bnb_quantity: float,
            transaction_revert_time: int = 100000,
            gas_amount: int = 300000,
            gas_price: int = 5
    ) -> str | None:
        token_to_buy = self.__web3.to_checksum_address(token_address)
        spend = self.__web3.to_checksum_address(utils.WBNB_CONTRACT)
        contract = self.__web3.eth.contract(
            address=self.__web3.to_checksum_address(utils.PANCAKE_SWAP_ROUTER_ADDRESS),
            abi=utils.PANCAKE_ABI
        )
        nonce = self.__web3.eth.get_transaction_count(self.__web3.to_checksum_address(self.__private_wallet))

        pancakeswap2_txn = contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            0,
            [spend, token_to_buy],
            self.__private_wallet,
            (int(time.time()) + transaction_revert_time)
        ).build_transaction({
            'from': self.__private_wallet,
            'value': self.__web3.to_wei(float(bnb_quantity), 'ether'),
            'gas': gas_amount,
            'gasPrice': self.__web3.to_wei(gas_price, 'gwei'),
            'nonce': nonce,
        })

        tx_token_swap = False

        try:
            signed_txn = self.__web3.eth.account.sign_transaction(pancakeswap2_txn, self.__private_key)
            tx_token_swap = self.__web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        except Exception as error:
            print(error)
            return None

        if tx_token_swap:
            time.sleep(15)
            tx_hash = str(self.__web3.to_hex(tx_token_swap))
            return tx_hash

        return None

    def swap_token_to_bnb_by_address(self, token_address: str, token_quantity: float, gas_price: int = 5) -> str | None:
        contract = self.__web3.eth.contract(
            address=self.__web3.to_checksum_address(
                utils.PANCAKE_SWAP_ROUTER_ADDRESS),
            abi=utils.PANCAKE_ABI
        )
        spend = self.__web3.to_checksum_address(utils.WBNB_CONTRACT)
        sell_token_contract = self.__web3.eth.contract(address=self.__web3.to_checksum_address(token_address),
                                                       abi=utils.TOKENNAME_ABI)
        token_quantity = utils.adjust_quantity(token_quantity, sell_token_contract.functions.decimals().call())

        try:
            approve = sell_token_contract.functions.approve(utils.PANCAKE_SWAP_ROUTER_ADDRESS,
                                                            token_quantity).build_transaction({
                'from': self.__private_wallet,
                'gasPrice': self.__web3.to_wei(gas_price, 'gwei'),
                'nonce': self.__web3.eth.get_transaction_count(self.__web3.to_checksum_address(self.__private_wallet)),
            })
        except Exception as error:
            print(error)
            return None

        try:
            signed_txn = self.__web3.eth.account.sign_transaction(approve, private_key=self.__private_wallet)
            tx_token_approve = self.__web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        except Exception as error:
            print(error)
            return None

        if tx_token_approve:
            time.sleep(5)
            pancakeswap2_txn = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                token_quantity, 0,
                [self.__web3.to_checksum_address(token_address), spend],
                self.__private_wallet,
                (int(time.time()) + 1000000)
            ).build_transaction({
                'from': self.__private_wallet,
                'gasPrice': self.__web3.to_wei(gas_price, 'gwei'),
                'nonce': self.__web3.eth.get_transaction_count(self.__web3.to_checksum_address(self.__private_wallet)),
            })

            tx_token_swap = False

            try:
                signed_txn = self.__web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=self.__private_key)
                tx_token_swap = self.__web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            except Exception as error:
                print(error)
                return None

            if tx_token_swap:
                time.sleep(15)
                tx_hash = str(self.__web3.to_hex(tx_token_swap))
                return tx_hash

            return None


class TokenInfo(object):

    def __init__(self, token_address: str) -> None:
        self.__web3 = Web3(Web3.HTTPProvider(utils.BSC))
        self.token_address = token_address
        self.__token_contract = self.__web3.eth.contract(address=self.__web3.to_checksum_address(token_address),
                                                         abi=utils.TOKENNAME_ABI)

    def bnb_price(self) -> float:
        bnb_token = Web3.to_checksum_address(utils.WBNB_CONTRACT)
        token_decimals = self.__token_contract.functions.decimals().call()
        amount_in = self.__web3.to_wei(1, utils.get_token_decimal(token_decimals))
        router = self.__web3.eth.contract(address=Web3.to_checksum_address(utils.PANCAKE_SWAP_ROUTER_ADDRESS),
                                          abi=utils.PANCAKE_ABI)
        amount_out = router.functions.getAmountsOut(amount_in,
                                                    [Web3.to_checksum_address(self.token_address), bnb_token]).call()
        amount_out = self.__web3.from_wei(amount_out[1], 'ether')

        return amount_out

    def symbol(self):
        return self.__token_contract.functions.symbol().call()
