# Copyright (c) 2016-present, Gregory Szorc
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license. See the LICENSE file for details.

import os

from typing import (
    BinaryIO,
    ByteString,
    Generator,
    IO,
    Iterable,
    List,
    Optional,
    Tuple,
    Union,
)

FLUSH_BLOCK: int
FLUSH_FRAME: int

COMPRESSOBJ_FLUSH_FINISH: int
COMPRESSOBJ_FLUSH_BLOCK: int

CONTENTSIZE_UNKNOWN: int
CONTENTSIZE_ERROR: int

MAX_COMPRESSION_LEVEL: int

COMPRESSION_RECOMMENDED_INPUT_SIZE: int
COMPRESSION_RECOMMENDED_OUTPUT_SIZE: int

DECOMPRESSION_RECOMMENDED_INPUT_SIZE: int
DECOMPRESSION_RECOMMENDED_OUTPUT_SIZE: int

BLOCKSIZELOG_MAX: int
BLOCKSIZE_MAX: int

WINDOWLOG_MIN: int
WINDOWLOG_MAX: int

CHAINLOG_MIN: int
CHAINLOG_MAX: int
HASHLOG_MIN: int
HASHLOG_MAX: int
HASHLOG3_MAX: int
MINMATCH_MIN: int
MINMATCH_MAX: int
SEARCHLOG_MIN: int
SEARCHLOG_MAX: int
SEARCHLENGTH_MIN: int
SEARCHLENGTH_MAX: int
TARGETLENGTH_MIN: int
TARGETLENGTH_MAX: int
LDM_MINMATCH_MIN: int
LDM_MINMATCH_MAX: int
LDM_BUCKETSIZELOG_MAX: int

STRATEGY_FAST: int
STRATEGY_DFAST: int
STRATEGY_GREEDY: int
STRATEGY_LAZY: int
STRATEGY_LAZY2: int
STRATEGY_BTLAZY2: int
STRATEGY_BTOPT: int
STRATEGY_BTULTRA: int
STRATEGY_BTULTRA2: int

DICT_TYPE_AUTO: int
DICT_TYPE_RAWCONTENT: int
DICT_TYPE_FULLDICT: int

FORMAT_ZSTD1: int
FORMAT_ZSTD1_MAGICLESS: int

ZSTD_VERSION: Tuple[int, int, int]
FRAME_HEADER: bytes
MAGIC_NUMBER: int

backend: str
__version__: str

class ZstdError(Exception): ...

class BufferSegment(object):
    offset: int
    def __len__(self) -> int: ...
    def tobytes(self) -> bytes: ...

class BufferSegments(object):
    def __len__(self) -> int: ...
    def __getitem__(self, i: int) -> BufferSegment: ...

class BufferWithSegments(object):
    size: int
    def __init__(self, data: ByteString, segments: ByteString): ...
    def __len__(self) -> int: ...
    def __getitem__(self, i: int) -> BufferSegment: ...
    def segments(self): ...
    def tobytes(self) -> bytes: ...

class BufferWithSegmentsCollection(object):
    def __init__(self, *args): ...
    def __len__(self) -> int: ...
    def __getitem__(self, i: int) -> BufferSegment: ...
    def size(self) -> int: ...

class ZstdCompressionParameters(object):
    @staticmethod
    def from_level(
        level: int, source_size: int = 0, dict_size: int = 0, **kwargs
    ) -> "ZstdCompressionParameters": ...
    def __init__(
        self,
        format: int = 0,
        compression_level: int = 0,
        window_log: int = 0,
        hash_log: int = 0,
        chain_log: int = 0,
        search_log: int = 0,
        min_match: int = 0,
        target_length: int = 0,
        strategy: int = -1,
        compression_strategy: int = -1,
        write_content_size: int = 1,
        write_checksum: int = 0,
        write_dict_id: int = 0,
        job_size: int = 0,
        overlap_log: int = -1,
        overlap_size_log: int = -1,
        force_max_window: int = 0,
        enable_ldm: int = 0,
        ldm_hash_log: int = 0,
        ldm_min_match: int = 0,
        ldm_bucket_size_log: int = 0,
        ldm_hash_rate_log: int = -1,
        ldm_hash_every_log: int = -1,
        threads: int = 0,
    ): ...
    @property
    def format(self) -> int: ...
    @property
    def compression_level(self) -> int: ...
    @property
    def window_log(self) -> int: ...
    @property
    def hash_log(self) -> int: ...
    @property
    def chain_log(self) -> int: ...
    @property
    def search_log(self) -> int: ...
    @property
    def min_match(self) -> int: ...
    @property
    def target_length(self) -> int: ...
    @property
    def compression_strategy(self) -> int: ...
    @property
    def write_content_size(self) -> int: ...
    @property
    def write_checksum(self) -> int: ...
    @property
    def write_dict_id(self) -> int: ...
    @property
    def job_size(self) -> int: ...
    @property
    def overlap_log(self) -> int: ...
    @property
    def overlap_size_log(self) -> int: ...
    @property
    def force_max_window(self) -> int: ...
    @property
    def enable_ldm(self) -> int: ...
    @property
    def ldm_hash_log(self) -> int: ...
    @property
    def ldm_min_match(self) -> int: ...
    @property
    def ldm_bucket_size_log(self) -> int: ...
    @property
    def ldm_hash_rate_log(self) -> int: ...
    @property
    def ldm_hash_every_log(self) -> int: ...
    @property
    def threads(self) -> int: ...
    def estimated_compression_context_size(self) -> int: ...

class CompressionParameters(ZstdCompressionParameters): ...

class ZstdCompressionDict(object):
    k: int
    d: int
    def __init__(
        self, data: ByteString, dict_type: int = 0, k: int = 0, d: int = 0,
    ): ...
    def __len__(self) -> int: ...
    def dict_id(self) -> int: ...
    def as_bytes(self) -> bytes: ...
    def precompute_compress(
        self,
        level: int = 0,
        compression_params: ZstdCompressionParameters = None,
    ): ...

class ZstdCompressionObj(object):
    def compress(self, data: ByteString) -> bytes: ...
    def flush(self, flush_mode: int = 0) -> bytes: ...

class ZstdCompressionChunker(object):
    def compress(self, data: ByteString): ...
    def flush(self): ...
    def finish(self): ...

class ZstdCompressionReader(BinaryIO):
    def __enter__(self) -> "ZstdCompressionReader": ...
    def __exit__(self, exc_type, exc_value, exc_tb): ...
    def readable(self) -> bool: ...
    def writable(self) -> bool: ...
    def seekable(self) -> bool: ...
    def readline(self, limit: int = -1) -> bytes: ...
    def readlines(self, hint: int = -1) -> List[bytes]: ...
    def write(self, data: ByteString): ...
    def writelines(self, data: Iterable[bytes]): ...
    def isatty(self) -> bool: ...
    def flush(self): ...
    def close(self): ...
    @property
    def closed(self) -> bool: ...
    def tell(self) -> int: ...
    def readall(self) -> bytes: ...
    def __iter__(self): ...
    def __next__(self): ...
    def next(self): ...
    def read(self, size: int = -1) -> bytes: ...
    def read1(self, size: int = -1) -> bytes: ...
    def readinto(self, b) -> int: ...
    def readinto1(self, b) -> int: ...

class ZstdCompressionWriter(BinaryIO):
    def __enter__(self) -> "ZstdCompressionWriter": ...
    def __exit__(self, exc_type, exc_value, exc_tb): ...
    def memory_size(self) -> int: ...
    def fileno(self) -> int: ...
    def close(self): ...
    @property
    def closed(self) -> bool: ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    def readline(self, size: int = -1) -> bytes: ...
    def readlines(self, hint: int = -1) -> List[bytes]: ...
    def seek(self, offset: int, whence: int = 0): ...
    def seekable(self) -> bool: ...
    def truncate(self, size: int = None): ...
    def writable(self) -> bool: ...
    def writelines(self, lines: Iterable[bytes]): ...
    def read(self, size: int = -1) -> bytes: ...
    def readall(self) -> bytes: ...
    def readinto(self, b): ...
    def write(self, data: ByteString) -> int: ...
    def flush(self, flush_mode: int = 0) -> int: ...
    def tell(self) -> int: ...

class ZstdCompressor(object):
    def __init__(
        self,
        level: int = 3,
        dict_data: ZstdCompressionDict = None,
        compression_params: ZstdCompressionParameters = None,
        write_checksum: bool = None,
        write_content_size: bool = None,
        write_dict_id: bool = None,
        threads: int = 0,
    ): ...
    def memory_size(self) -> int: ...
    def compress(self, data: ByteString) -> bytes: ...
    def compressobj(self, size: int = -1) -> ZstdCompressionObj: ...
    def chunker(
        self, size: int = -1, chunk_size: int = -1
    ) -> ZstdCompressionChunker: ...
    def copy_stream(
        self,
        ifh: IO[bytes],
        ofh: IO[bytes],
        size: int = -1,
        read_size: int = -1,
        write_size: int = -1,
    ) -> Tuple[int, int]: ...
    def stream_reader(
        self,
        source: Union[IO[bytes], ByteString],
        size: int = -1,
        read_size: int = -1,
        *,
        closefd: bool = False,
    ) -> ZstdCompressionReader: ...
    def stream_writer(
        self,
        writer: IO[bytes],
        size: int = -1,
        write_size: int = -1,
        write_return_read: bool = None,
        *,
        closefd: bool = True,
    ) -> ZstdCompressionWriter: ...
    def read_to_iter(
        self,
        reader: Union[IO[bytes], ByteString],
        size: int = -1,
        read_size: int = -1,
        write_size: int = -1,
    ) -> Generator[bytes, None, None]: ...
    def frame_progression(self) -> Tuple[int, int, int]: ...
    def multi_compress_to_buffer(
        self,
        data: Union[
            BufferWithSegments, BufferWithSegmentsCollection, List[ByteString],
        ],
        threads: int = 0,
    ) -> BufferWithSegmentsCollection: ...

class ZstdDecompressionObj(object):
    def decompress(self, data: ByteString) -> bytes: ...
    def flush(self, length: int = 0): ...

class ZstdDecompressionReader(BinaryIO):
    def __enter__(self) -> "ZstdDecompressionReader": ...
    def __exit__(self, exc_type, exc_value, exc_tb): ...
    def readable(self) -> bool: ...
    def writable(self) -> bool: ...
    def seekable(self) -> bool: ...
    def readline(self, size: int = -1): ...
    def readlines(self, hint: int = -1): ...
    def write(self, data: ByteString): ...
    def writelines(self, lines: Iterable[bytes]): ...
    def isatty(self) -> bool: ...
    def flush(self): ...
    def close(self): ...
    @property
    def closed(self) -> bool: ...
    def tell(self) -> int: ...
    def readall(self) -> bytes: ...
    def __iter__(self): ...
    def __next__(self): ...
    def next(self): ...
    def read(self, size: int = -1) -> bytes: ...
    def readinto(self, b) -> int: ...
    def read1(self, size: int = -1) -> bytes: ...
    def readinto1(self, b) -> int: ...
    def seek(self, pos: int, whence: int = 0) -> int: ...

class ZstdDecompressionWriter(BinaryIO):
    def __enter__(self) -> "ZstdDecompressionWriter": ...
    def __exit__(self, exc_type, exc_value, exc_tb): ...
    def memory_size(self) -> int: ...
    def close(self): ...
    @property
    def closed(self) -> bool: ...
    def fileno(self) -> int: ...
    def flush(self): ...
    def isatty(self) -> bool: ...
    def readable(self) -> bool: ...
    def readline(self, size: int = -1): ...
    def readlines(self, hint: int = -1): ...
    def seek(self, offset: int, whence: int = None): ...
    def seekable(self) -> bool: ...
    def tell(self): ...
    def truncate(self, size: int = None): ...
    def writable(self) -> bool: ...
    def writelines(self, lines: Iterable[bytes]): ...
    def read(self, size: int = -1): ...
    def readall(self): ...
    def readinto(self, b): ...
    def write(self, data: ByteString) -> int: ...

class ZstdDecompressor(object):
    def __init__(
        self,
        dict_data: ZstdCompressionDict = None,
        max_window_size: int = 0,
        format: int = 0,
    ): ...
    def memory_size(self) -> int: ...
    def decompress(
        self, data: ByteString, max_output_size: int = 0
    ) -> bytes: ...
    def stream_reader(
        self,
        source: Union[IO[bytes], ByteString],
        read_size: int = 0,
        read_across_frames: bool = False,
        *,
        closefd=False,
    ) -> ZstdDecompressionReader: ...
    def decompressobj(self, write_size: int = 0) -> ZstdDecompressionObj: ...
    def read_to_iter(
        self,
        reader: Union[IO[bytes], ByteString],
        read_size: int = 0,
        write_size: int = 0,
        skip_bytes: int = 0,
    ) -> Generator[bytes, None, None]: ...
    def stream_writer(
        self,
        writer: IO[bytes],
        write_size: int = 0,
        write_return_read: bool = False,
        *,
        closefd: bool = True,
    ) -> ZstdDecompressionWriter: ...
    def copy_stream(
        self,
        ifh: IO[bytes],
        ofh: IO[bytes],
        read_size: int = 0,
        write_size: int = 0,
    ) -> Tuple[int, int]: ...
    def decompress_content_dict_chain(
        self, frames: list[ByteString]
    ) -> bytes: ...
    def multi_decompress_to_buffer(
        self,
        frames: Union[
            BufferWithSegments, BufferWithSegmentsCollection, List[ByteString],
        ],
        decompressed_sizes: ByteString = None,
        threads: int = 0,
    ) -> BufferWithSegmentsCollection: ...

class FrameParameters(object):
    content_size: int
    window_size: int
    dict_id: int
    has_checksum: bool

def estimate_decompression_context_size() -> int: ...
def frame_content_size(data: ByteString) -> int: ...
def frame_header_size(data: ByteString) -> int: ...
def get_frame_parameters(data: ByteString) -> FrameParameters: ...
def train_dictionary(
    dict_size: int,
    samples: list[ByteString],
    k: int = 0,
    d: int = 0,
    f: int = 0,
    split_point: float = 0.0,
    accel: int = 0,
    notifications: int = 0,
    dict_id: int = 0,
    level: int = 0,
    steps: int = 0,
    threads: int = 0,
) -> ZstdCompressionDict: ...
def open(
    filename: Union[bytes, str, os.PathLike, BinaryIO],
    mode: str = "rb",
    cctx: Optional[ZstdCompressor] = None,
    dctx: Optional[ZstdDecompressor] = None,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    closefd: bool = None,
): ...
