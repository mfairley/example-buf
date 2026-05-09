python_requirements(
    name="reqs",
    source="requirements.txt",
    overrides={
        # The `protovalidate` PyPI wheel only ships the validator runtime; its
        # bindings (`buf.validate.validate_pb2`) come from the BSR-generated
        # wheel. Declare that here so anything depending on `protovalidate`
        # transitively gets the bindings without each consumer having to know.
        "protovalidate": {
            "dependencies": ["3rdparty:reqs#bufbuild-protovalidate-protocolbuffers-python"],
        },
    },
)
