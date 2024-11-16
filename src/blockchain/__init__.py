"""
Module used for blockchain

--- pws256/blockchain
"""
import hashlib

class _Block:
    def __init__(self, idx, data):
        self.idx = idx
        self.data = data
        self.hash = self.hash