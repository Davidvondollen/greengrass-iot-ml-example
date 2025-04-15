python3 -m venv venv
source venv/bin/activate

# Install test dependencies
pip install --upgrade pip
pip install -r ./tests/requirements-test.txt

# Set PYTHONPATH so relative imports work
export PYTHONPATH=$(pwd)

# Run tests
pytest tests/

deactivate