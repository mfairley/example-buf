python_sources(
    sources=["*.py", "!test_*.py"],
)

python_tests(
    name="tests",
    sources=["test_*.py"],
)

pex_binary(
    name="server-bin",
    entry_point="server.py",
)
