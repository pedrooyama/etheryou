from model.compression_algorithm import CompressionAlgorithm
import lzma
import zlib
import bz2


class Compressor:

    @staticmethod
    def compress(algorithm: CompressionAlgorithm, data: bytes) -> bytes:
        if algorithm is CompressionAlgorithm.NONE:
            return data
        if algorithm is CompressionAlgorithm.LZMA:
            compressor = lzma.LZMACompressor()
            compressed_data = compressor.compress(data)
            compressed_data += compressor.flush()
            return compressed_data
        if algorithm is CompressionAlgorithm.ZLIB:
            return zlib.compress(data)
        if algorithm is CompressionAlgorithm.BZ2:
            return bz2.compress(data)
        raise ValueError

    @staticmethod
    def compress_with_best_algorithm(data: bytes) -> (CompressionAlgorithm, bytes):
        best_algorithm: CompressionAlgorithm = CompressionAlgorithm.NONE
        best_compression = data
        for algorithm in CompressionAlgorithm:
            candidate_compression = Compressor.compress(algorithm=algorithm, data=data)
            if len(candidate_compression) < len(best_compression):
                best_compression = candidate_compression
                best_algorithm = algorithm

        return best_algorithm, best_compression

    @staticmethod
    def decompress(algorithm: CompressionAlgorithm, data: bytes) -> bytes:
        if algorithm is CompressionAlgorithm.NONE:
            return data
        if algorithm is CompressionAlgorithm.LZMA:
            return lzma.LZMADecompressor().decompress(data)
        if algorithm is CompressionAlgorithm.ZLIB:
            return zlib.decompress(data)
        if algorithm is CompressionAlgorithm.BZ2:
            return bz2.decompress(data)
        raise ValueError
