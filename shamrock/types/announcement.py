from dataclasses import dataclass

from shamrock.types.blockchain_format.sized_bytes import bytes32
from shamrock.util.hash import std_hash


@dataclass(frozen=True)
class Announcement:
    origin_info: bytes32
    message: bytes

    def name(self) -> bytes32:
        return std_hash(bytes(self.origin_info + self.message))
