class BlockchainMessageBlock:

    def __init__(self, timestamp: int, block_hash: bytes, data: bytes):
        self.timestamp = timestamp
        self.block_hash = block_hash
        self.data = data
