sphinx-apidoc -f -o docs/source/docstring/reader reader_lib/willfs/
sphinx-apidoc -f -o docs/source/docstring/writer writer_lib/willfsemr/
cd docs
make html
