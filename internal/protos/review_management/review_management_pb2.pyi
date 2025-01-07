from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateReviewRequest(_message.Message):
    __slots__ = ("user_id", "product_id", "rate", "text")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    product_id: int
    rate: float
    text: str
    def __init__(self, user_id: _Optional[int] = ..., product_id: _Optional[int] = ..., rate: _Optional[float] = ..., text: _Optional[str] = ...) -> None: ...

class DeleteReviewRequest(_message.Message):
    __slots__ = ("user_id", "product_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    product_id: int
    def __init__(self, user_id: _Optional[int] = ..., product_id: _Optional[int] = ...) -> None: ...

class ReviewOperationResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
