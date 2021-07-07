from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "shamrock_harvester shamrock_timelord_launcher shamrock_timelord shamrock_farmer shamrock_full_node shamrock_wallet".split(),
    "node": "shamrock_full_node".split(),
    "harvester": "shamrock_harvester".split(),
    "farmer": "shamrock_harvester shamrock_farmer shamrock_full_node shamrock_wallet".split(),
    "farmer-no-wallet": "shamrock_harvester shamrock_farmer shamrock_full_node".split(),
    "farmer-only": "shamrock_farmer".split(),
    "timelord": "shamrock_timelord_launcher shamrock_timelord shamrock_full_node".split(),
    "timelord-only": "shamrock_timelord".split(),
    "timelord-launcher-only": "shamrock_timelord_launcher".split(),
    "wallet": "shamrock_wallet shamrock_full_node".split(),
    "wallet-only": "shamrock_wallet".split(),
    "introducer": "shamrock_introducer".split(),
    "simulator": "shamrock_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
