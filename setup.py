from setuptools import setup

dependencies = [
    "blspy==1.0.2",  # Signature library
    "chiavdf==1.0.2",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.3",  # proof of space
    "clvm==0.9.7",
    "clvm_rs==0.1.8",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.7",  # Binary data management library
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the shamrock processes readable names
    "sortedcontainers==2.3.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspython==2.1.0",  # Query DNS seeds
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
]

kwargs = dict(
    name="shamrock-blockchain",
    author="Shamrock Network",
    author_email="shamrock@shamrock.network",
    description="Shamrock blockchain full node, farmer, timelord, and wallet.",
    url="https://shamrock.network/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="shamrock blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "shamrock",
        "shamrock.cmds",
        "shamrock.clvm",
        "shamrock.consensus",
        "shamrock.daemon",
        "shamrock.full_node",
        "shamrock.timelord",
        "shamrock.farmer",
        "shamrock.harvester",
        "shamrock.introducer",
        "shamrock.plotting",
        "shamrock.pools",
        "shamrock.protocols",
        "shamrock.rpc",
        "shamrock.server",
        "shamrock.simulator",
        "shamrock.types.blockchain_format",
        "shamrock.types",
        "shamrock.util",
        "shamrock.wallet",
        "shamrock.wallet.puzzles",
        "shamrock.wallet.rl_wallet",
        "shamrock.wallet.cc_wallet",
        "shamrock.wallet.did_wallet",
        "shamrock.wallet.settings",
        "shamrock.wallet.trading",
        "shamrock.wallet.util",
        "shamrock.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "shamrock = shamrock.cmds.shamrock:main",
            "shamrock_wallet = shamrock.server.start_wallet:main",
            "shamrock_full_node = shamrock.server.start_full_node:main",
            "shamrock_harvester = shamrock.server.start_harvester:main",
            "shamrock_farmer = shamrock.server.start_farmer:main",
            "shamrock_introducer = shamrock.server.start_introducer:main",
            "shamrock_timelord = shamrock.server.start_timelord:main",
            "shamrock_timelord_launcher = shamrock.timelord.timelord_launcher:main",
            "shamrock_full_node_simulator = shamrock.simulator.start_simulator:main",
        ]
    },
    package_data={
        "shamrock": ["pyinstaller.spec"],
        "shamrock.wallet.puzzles": ["*.clvm", "*.clvm.hex"],
        "shamrock.util": ["initial-*.yaml", "english.txt"],
        "shamrock.ssl": ["shamrock_ca.crt", "shamrock_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    use_scm_version={"fallback_version": "unknown-no-.git-directory"},
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)
