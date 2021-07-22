from typing import Dict

# The rest of the codebase uses clovers everywhere.
# Only use these units for user facing interfaces.
units: Dict[str, int] = {
    "shamrock": 10 ** 12,  # 1 shamrock (SRN) is 1,000,000,000,000 clover (1 trillion)
    "clover:": 1,
    "colouredcoin": 10 ** 3,  # 1 coloured coin is 1000 colouredcoin clovers
}
