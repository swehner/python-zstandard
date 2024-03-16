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
    Set,
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
backend_features: Set[str]
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
        level: int, source_size: int = ..., dict_size: int = ..., **kwargs
    ) -> "ZstdCompressionParameters": ...
    def __init__(
        self,
        format: int = ...,
        compression_level: int = ...,
        window_log: int = ...,
        hash_log: int = ...,
        chain_log: int = ...,
        search_log: int = ...,
        min_match: int = ...,
        target_length: int = ...,
        strategy: int = ...,
        write_content_size: int = ...,
        write_checksum: int = ...,
        write_dict_id: int = ...,
        job_size: int = ...,
        overlap_log: int = ...,
        force_max_window: int = ...,
        enable_ldm: int = ...,
        ldm_hash_log: int = ...,
        ldm_min_match: int = ...,
        ldm_bucket_size_log: int = ...,
        ldm_hash_rate_log: int = ...,
        threads: int = ...,
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
    def strategy(self) -> int: ...
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
    def threads(self) -> int: ...
    def estimated_compression_context_size(self) -> int: ...

class CompressionParameters(ZstdCompressionParameters): ...

class ZstdCompressionDict(object):
    k: int
    d: int
    def __init__(
        self,
        data: ByteString,
        dict_type: int = ...,
        k: int = ...,
        d: int = ...,
    ): ...
    def __len__(self) -> int: ...
    def dict_id(self) -> int: ...
    def as_bytes(self) -> bytes: ...
    def precompute_compress(
        self,
        level: int = ...,
        compression_params: ZstdCompressionParameters = ...,
    ): ...

class ZstdCompressionObj(object):
    def compress(self, data: ByteString) -> bytes: ...
    def flush(self, flush_mode: int = ...) -> bytes: ...

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
    def readline(self, limit: int = ...) -> bytes: ...
    def readlines(self, hint: int = ...) -> List[bytes]: ...
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
    def read(self, size: int = ...) -> bytes: ...
    def read1(self, size: int = ...) -> bytes: ...
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
    def readline(self, size: int = ...) -> bytes: ...
    def readlines(self, hint: int = ...) -> List[bytes]: ...
    def seek(self, offset: int, whence: int = ...): ...
    def seekable(self) -> bool: ...
    def truncate(self, size: int = ...): ...
    def writable(self) -> bool: ...
    def writelines(self, lines: Iterable[bytes]): ...
    def read(self, size: int = ...) -> bytes: ...
    def readall(self) -> bytes: ...
    def readinto(self, b): ...
    def write(self, data: ByteString) -> int: ...
    def flush(self, flush_mode: int = ...) -> int: ...
    def tell(self) -> int: ...

class ZstdCompressor(object):
    def __init__(
        self,
        level: int = ...,
        dict_data: Optional[ZstdCompressionDict] = ...,
        compression_params: Optional[ZstdCompressionParameters] = ...,
        write_checksum: Optional[bool] = ...,
        write_content_size: Optional[bool] = ...,
        write_dict_id: Optional[bool] = ...,
        threads: int = ...,
    ): ...
    def memory_size(self) -> int: ...
    def compress(self, data: ByteString) -> bytes: ...
    def compressobj(self, size: int = ...) -> ZstdCompressionObj: ...
    def chunker(
        self, size: int = ..., chunk_size: int = ...
    ) -> ZstdCompressionChunker: ...
    def copy_stream(
        self,
        ifh: IO[bytes],
        ofh: IO[bytes],
        size: int = ...,
        read_size: int = ...,
        write_size: int = ...,
    ) -> Tuple[int, int]: ...
    def stream_reader(
        self,
        source: Union[IO[bytes], ByteString],
        size: int = ...,
        read_size: int = ...,
        *,
        closefd: bool = ...,
    ) -> ZstdCompressionReader: ...
    def stream_writer(
        self,
        writer: IO[bytes],
        size: int = ...,
        write_size: int = ...,
        write_return_read: bool = ...,
        *,
        closefd: bool = ...,
    ) -> ZstdCompressionWriter: ...
    def read_to_iter(
        self,
        reader: Union[IO[bytes], ByteString],
        size: int = ...,
        read_size: int = ...,
        write_size: int = ...,
    ) -> Generator[bytes, None, None]: ...
    def frame_progression(self) -> Tuple[int, int, int]: ...
    def multi_compress_to_buffer(
        self,
        data: Union[
            BufferWithSegments,
            BufferWithSegmentsCollection,
            List[ByteString],
        ],
        threads: int = ...,
    ) -> BufferWithSegmentsCollection: ...

class ZstdDecompressionObj(object):
    def decompress(self, data: ByteString) -> bytes: ...
    def flush(self, length: int = ...) -> bytes: ...
    @property
    def unused_data(self) -> bytes: ...
    @property
    def unconsumed_tail(self) -> bytes: ...
    @property
    def eof(self) -> bool: ...

class ZstdDecompressionReader(BinaryIO):
    def __enter__(self) -> "ZstdDecompressionReader": ...
    def __exit__(self, exc_type, exc_value, exc_tb): ...
    def readable(self) -> bool: ...
    def writable(self) -> bool: ...
    def seekable(self) -> bool: ...
    def readline(self, size: int = ...): ...
    def readlines(self, hint: int = ...): ...
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
    def read(self, size: int = ...) -> bytes: ...
    def readinto(self, b) -> int: ...
    def read1(self, size: int = ...) -> bytes: ...
    def readinto1(self, b) -> int: ...
    def seek(self, pos: int, whence: int = ...) -> int: ...

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
    def readline(self, size: int = ...): ...
    def readlines(self, hint: int = ...): ...
    def seek(self, offset: int, whence: int = ...): ...
    def seekable(self) -> bool: ...
    def tell(self): ...
    def truncate(self, size: int = ...): ...
    def writable(self) -> bool: ...
    def writelines(self, lines: Iterable[bytes]): ...
    def read(self, size: int = ...): ...
    def readall(self): ...
    def readinto(self, b): ...
    def write(self, data: ByteString) -> int: ...

class ZstdDecompressor(object):
    def __init__(
        self,
        dict_data: Optional[ZstdCompressionDict] = ...,
        max_window_size: int = ...,
        format: int = ...,
    ): ...
    def memory_size(self) -> int: ...
    def decompress(
        self,
        data: ByteString,
        max_output_size: int = ...,
        read_across_frames: bool = ...,
        allow_extra_data: bool = ...,
    ) -> bytes: ...
    def stream_reader(
        self,
        source: Union[IO[bytes], ByteString],
        read_size: int = ...,
        read_across_frames: bool = ...,
        *,
        closefd=False,
    ) -> ZstdDecompressionReader: ...
    def decompressobj(
        self, write_size: int = ..., read_across_frames: bool = False
    ) -> ZstdDecompressionObj: ...
    def read_to_iter(
        self,
        reader: Union[IO[bytes], ByteString],
        read_size: int = ...,
        write_size: int = ...,
        skip_bytes: int = ...,
    ) -> Generator[bytes, None, None]: ...
    def stream_writer(
        self,
        writer: IO[bytes],
        write_size: int = ...,
        write_return_read: bool = ...,
        *,
        closefd: bool = ...,
    ) -> ZstdDecompressionWriter: ...
    def copy_stream(
        self,
        ifh: IO[bytes],
        ofh: IO[bytes],
        read_size: int = ...,
        write_size: int = ...,
    ) -> Tuple[int, int]: ...
    def decompress_content_dict_chain(
        self, frames: list[ByteString]
    ) -> bytes: ...
    def multi_decompress_to_buffer(
        self,
        frames: Union[
            BufferWithSegments,
            BufferWithSegmentsCollection,
            List[ByteString],
        ],
        decompressed_sizes: ByteString = ...,
        threads: int = ...,
    ) -> BufferWithSegmentsCollection: ...

class FrameParameters(object):
    content_size: int
    window_size: int
    dict_id: int
    has_checksum: bool

def estimate_decompression_context_size() -> int: ...
def frame_content_size(data: ByteString) -> int: ...
def frame_header_size(data: ByteString) -> int: ...
def get_frame_parameters(data: ByteString, format: Optional[int]) -> FrameParameters: ...
def train_dictionary(
    dict_size: int,
    samples: list[ByteString],
    k: int = ...,
    d: int = ...,
    f: int = ...,
    split_point: float = ...,
    accel: int = ...,
    notifications: int = ...,
    dict_id: int = ...,
    level: int = ...,
    steps: int = ...,
    threads: int = ...,
) -> ZstdCompressionDict: ...
def open(
    filename: Union[bytes, str, os.PathLike, BinaryIO],
    mode: str = ...,
    cctx: Optional[ZstdCompressor] = ...,
    dctx: Optional[ZstdDecompressor] = ...,
    encoding: Optional[str] = ...,
    errors: Optional[str] = ...,
    newline: Optional[str] = ...,
    closefd: bool = ...,
): ...
def compress(data: ByteString, level: int = ...) -> bytes: ...
def decompress(data: ByteString, max_output_size: int = ...) -> bytes: ...
