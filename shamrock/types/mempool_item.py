from dataclasses import dataclass
from typing import List

from shamrock.consensus.cost_calculator import NPCResult
from shamrock.types.blockchain_format.coin import Coin
from shamrock.types.blockchain_format.program import SerializedProgram
from shamrock.types.blockchain_format.sized_bytes import bytes32
from shamrock.types.spend_bundle import SpendBundle
from shamrock.util.ints import uint64
from shamrock.util.streamable import Streamable, streamable


@dataclass(frozen=True)
@streamable
class MempoolItem(Streamable):
    spend_bundle: SpendBundle
    fee: uint64
    npc_result: NPCResult
    cost: uint64
    spend_bundle_name: bytes32
    additions: List[Coin]
    removals: List[Coin]
    program: SerializedProgram

    def __lt__(self, other):
        return self.fee_per_cost < other.fee_per_cost

    @property
    def fee_per_cost(self) -> float:
        return int(self.fee) / int(self.cost)

    @property
    def name(self) -> bytes32:
        return self.spend_bundle_name
