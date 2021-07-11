from shamrock.util.ints import uint64

from .constants import ConsensusConstants

testnet_kwargs = {
    "SLOT_BLOCKS_TARGET": 512,
    "MIN_BLOCKS_PER_CHALLENGE_BLOCK": 200,  # Must be less than half of SLOT_BLOCKS_TARGET
    "MAX_SUB_SLOT_BLOCKS": 2048,  # Must be less than half of SUB_EPOCH_BLOCKS
    "NUM_SPS_SUB_SLOT": 16,  # Must be a power of 2
    # "SUB_SLOT_ITERS_STARTING": 2 ** 27,
    "SUB_SLOT_ITERS_STARTING": 2 ** 7,
    # DIFFICULTY_STARTING is the starting difficulty for the first epoch, which is then further
    # multiplied by another factor of DIFFICULTY_CONSTANT_FACTOR, to be used in the VDF iter calculation formula.
    # "DIFFICULTY_CONSTANT_FACTOR": 2 ** 67,
    "DIFFICULTY_CONSTANT_FACTOR": 2,
    "DIFFICULTY_STARTING": 7,
    # "DIFFICULTY_STARTING": 30,
    "DIFFICULTY_CHANGE_MAX_FACTOR": 3,  # The next difficulty is truncated to range [prev / FACTOR, prev * FACTOR]
    # These 3 constants must be changed at the same time
    # "SUB_EPOCH_BLOCKS": 384,  # The number of blocks per sub-epoch, mainnet 384
    "SUB_EPOCH_BLOCKS": 4096,   # The number of blocks per sub-epoch, mainnet 384
    # "EPOCH_BLOCKS": 4608,  # The number of blocks per epoch, mainnet 4608. Must be multiple of SUB_EPOCH_SB
    "EPOCH_BLOCKS": 49152,  # The number of blocks per epoch, mainnet 4608. Must be multiple of SUB_EPOCH_SB
    "SIGNIFICANT_BITS": 8,  # The number of bits to look at in difficulty and min iters. The rest are zeroed
    "DISCRIMINANT_SIZE_BITS": 1024,  # Max is 1024 (based on ClassGroupElement int size)
    "NUMBER_ZERO_BITS_PLOT_FILTER": 9,  # H(plot signature of the challenge) must start with these many zeroes
    "MIN_PLOT_SIZE": 32,  # 32 for mainnet
    "MAX_PLOT_SIZE": 50,
    "SUB_SLOT_TIME_TARGET": 600,  # The target number of seconds per slot, mainnet 600
    "NUM_SP_INTERVALS_EXTRA": 2,  # The number of sp intervals to add to the signage point
    "MAX_FUTURE_TIME": 5 * 60,  # The next block can have a timestamp of at most these many seconds in the future
    "NUMBER_OF_TIMESTAMPS": 11,  # Than the average of the last NUMBER_OF_TIMESTAMPS blocks
    # Used as the initial cc rc challenges, as well as first block back pointers, and first SES back pointer
    # We override this value based on the chain being run (testnet0, testnet1, mainnet, etc)
    # Default used for tests is std_hash(b'')
    # "GENESIS_CHALLENGE": bytes.fromhex("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "GENESIS_CHALLENGE": bytes.fromhex("0cad4b3ea1e76ec15c2fe8470482e37804a2eb6f1ab1586c509a7a1fa8fd1032"),
    # Forks of shamrock should change this value to provide replay attack protection. This is set to mainnet genesis chall
    # "AGG_SIG_ME_ADDITIONAL_DATA": bytes.fromhex("ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb"),
    "AGG_SIG_ME_ADDITIONAL_DATA": bytes.fromhex("7e846aee6d59856df623f2a16f96f4af65cac3493b89212ff534f9bdc55161a4"),
    "GENESIS_PRE_FARM_POOL_PUZZLE_HASH": bytes.fromhex(
        # "d23da14695a188ae5708dd152263c4db883eb27edeb936178d4d988b8f3ce5fc"
        "6e95df6cad92e52ac0cac6d71be4daef0302ecbcfb7168747d12a53faed69079"
    ),
    "GENESIS_PRE_FARM_FARMER_PUZZLE_HASH": bytes.fromhex(
        # "3d8765d3a597ec1d99663f6c9816d915b9f68613ac94009884c4addaefcce6af"
        "92c8beaf58ee8df3c736e9ff95551161ad9bcfe2d3a13934864b2787a1d2ff02"
    ),
    "MAX_VDF_WITNESS_SIZE": 64,
    # Size of mempool = 50x the size of block
    "MEMPOOL_BLOCK_BUFFER": 1000,
    # Max coin amount, fits into 64 bits
    "MAX_COIN_AMOUNT": uint64((1 << 64) - 1),
    # Max block cost in clvm cost units
    "MAX_BLOCK_COST_CLVM": 11000000000,
    # The cost per byte of generator program
    "COST_PER_BYTE": 12000,
    "WEIGHT_PROOF_THRESHOLD": 2,
    "BLOCKS_CACHE_SIZE": 49152 + (2048 * 4),
    "WEIGHT_PROOF_RECENT_BLOCKS": 1000,
    "MAX_BLOCK_COUNT_PER_REQUESTS": 512,  # Allow up to 32 blocks per request
    "INITIAL_FREEZE_END_TIMESTAMP": 1625997875,
    "NETWORK_TYPE": 0,
    "MAX_GENERATOR_SIZE": 1000000,
    "MAX_GENERATOR_REF_LIST_SIZE": 512,  # Number of references allowed in the block generator ref list
    "POOL_SUB_SLOT_ITERS": 37600000000,  # iters limit * NUM_SPS
}


DEFAULT_CONSTANTS = ConsensusConstants(**testnet_kwargs)  # type: ignore
