from aidbg.runner import run_program

def test_runner_no_crash(tmp_path):
    script = tmp_path / "ok.py"
    script.write_text("print('ok')")
    run_program(str(script))
