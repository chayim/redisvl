import os
import nbformat
import pytest

from nbconvert.preprocessors import ExecutePreprocessor


def list_ipynb_files(path):
    """Return a generator of .ipynb files in the given directory and its subdirectories."""
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.ipynb'):
                full_path = os.path.join(dirpath, filename)
                yield full_path

@pytest.mark.parametrize("notebook", list(list_ipynb_files("docs")))
def test_notebook_exec(notebook):
  with open(notebook) as f:
      nb = nbformat.read(f, as_version=4)
      ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
      try:
        assert ep.preprocess(nb) is not None, f"Got empty notebook for {notebook}"
      except Exception:
          assert False, f"Failed executing {notebook}"