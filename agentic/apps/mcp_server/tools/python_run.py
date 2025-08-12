import io
import runpy
import sys
import uuid
from pathlib import Path
from packages.schema.tool_models import PythonRunIn, PythonRunOut
from packages.common.validation import manifest_dir


def run(input: PythonRunIn) -> PythonRunOut:
    call_dir = Path("/tmp") / "pyexec" / str(uuid.uuid4())
    work = call_dir / "work"
    outdir = call_dir / "out"
    work.mkdir(parents=True, exist_ok=True)
    outdir.mkdir(parents=True, exist_ok=True)
    for f in input.files:
        dest = work / f["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f.get("content", ""))
    entry = work / ("main.py" if input.entrypoint == "inline" else input.entrypoint)
    if input.entrypoint == "inline" and input.code:
        (work / "main.py").write_text(input.code)
    stdout = io.StringIO()
    stderr = io.StringIO()
    rc = 0
    with redirect(stdout, stderr):
        try:
            sys.argv = [str(entry), *input.args]
            runpy.run_path(str(entry), run_name="__main__")
        except SystemExit as e:
            rc = int(e.code)
        except Exception as e:  # pragma: no cover - best effort
            rc = 1
            print(e, file=stderr)
    produced = manifest_dir(outdir)
    return PythonRunOut(return_code=rc, stdout=stdout.getvalue(), stderr=stderr.getvalue(), produced_files=produced, metrics={})


class redirect:
    def __init__(self, out, err):
        self.out = out
        self.err = err

    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = self.out
        sys.stderr = self.err

    def __exit__(self, exc_type, exc, tb):
        sys.stdout = self._stdout
        sys.stderr = self._stderr
