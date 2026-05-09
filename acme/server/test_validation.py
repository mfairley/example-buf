import pytest  # pants: no-infer-dep
from protovalidate import ValidationError, Validator

from acme.greeter.v1.greeter_pb2 import GreetRequest


@pytest.fixture
def validator() -> Validator:
    return Validator()


def test_valid_name_passes(validator: Validator) -> None:
    validator.validate(GreetRequest(name="Jane"))


def test_empty_name_rejected(validator: Validator) -> None:
    with pytest.raises(ValidationError):
        validator.validate(GreetRequest(name=""))
