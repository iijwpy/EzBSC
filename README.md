> ⚠️ Please note that this code is for study purposes only and will not be maintained.

> 📢 Please note that the code does not perform any unauthorized transactions; you can verify this within the code. Furthermore, I am not responsible for any misuse of the program.

> 📚 Please note that this module is tightly coupled with the Web3 module, which might undergo modifications in the future, rendering this module unusable.

# EzBSC
EzBSC is a user-friendly python module designed to streamline the swapping/sell/buy and gathering of information from tokens on the Binance Smart Chain.

# Example of usage

## Importing the Module

To get started with the module, follow these steps:

1. Clone this repository or download the files.
2. Place them in the same directory as your project.
3. Import the module as shown in the example below in your Python code:

```python
from EzBSC import Wallet, TokenInfo
```

### Defining Classes
To utilize the code, you need to define classes. The code consists of two classes, allowing you to manage your BSC wallet using your mnemonic phrase and obtain token information using its address. Here's how you can instantiate these classes with example data:

```python
# Instantiate a BSC wallet using a mnemonic phrase.
mnemonic_phrase = "delay drastic warfare since library proud endorse half indicate armed say gospel"
myWallet = Wallet(mnemonic_phrase)

# Instantiate TokenInfo using a POOCOIN address.
token = TokenInfo("0xb27adaffb9fea1801459a1a81b17218288c097cc")
```

### [Wallet] Retrieving BNB balance from the wallet
To retrieve the BNB balance from the wallet, you can utilize the following code:

```python
# Get and print the BNB balance in the wallet
bnb_balance = myWallet.bnb_balance()
print(f"BNB balance in the wallet: {bnb_balance} BNB")
```

### [Wallet] Performing a buy/swap of BNB for token
To perform a buy/swap of BNB for token (POOCOIN in the example), you can utilize the following code:

```python
# Address of the POOCOIN token: 0xb27adaffb9fea1801459a1a81b17218288c097cc
poocoin_token_address = "0xb27adaffb9fea1801459a1a81b17218288c097cc"

# Perform a swap of 1 BNB for the POOCOIN token
transaction = myWallet.swap_bnb_to_token_by_address(
    token_address=poocoin_token_address,
    bnb_quantity=1
)
print(transaction)
```

### [Wallet] Retrieving any token balance from the wallet
To retrieve any token balance from the wallet (POOCOIN in the example), you can utilize the following code:

```python
# Get the balance of the POOCOIN token in the wallet
poocoin_balance = myWallet.token_balance_by_address(poocoin_token_address)
print(f"POOCOIN balance in the wallet: {poocoin_balance} POOCOIN")
```

### [Wallet] Performing a sell/swap of token for BNB
To perform a buy/swap of token for BNB (POOCOIN in the example), you can utilize the following code:

```python
# Perform a swap of the POOCOIN balance back to BNB
transaction = myWallet.swap_token_to_bnb_by_address(
    token_address=poocoin_token_address,
    token_quantity=0.12412312 # Just and example
)
print(transaction)
```

### [TokenInfo] Retrieving token symbol
To retrieve any token symbol by address (POOCOIN in the example), you can utilize the following code:

```python
# Get POOCOIN token symbol
print(f"Token symbol: {token.symbol()}")
```

### [TokenInfo] Retrieving token prince in BNB
To retrieve any token prince in BNB by address (POOCOIN in the example), you can utilize the following code:
> 💱 The code will return the price of 1 token in BNB

```python
# Get 1 token price in BNB
print(f"Token price: {token.bnb_price()} BNB")
```
