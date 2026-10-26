import runpy


def test_python_dash_m_starts_the_cli(monkeypatch, capsys):
    # Running the package as __main__ should start the loop; EOF ends it.
    def eof(prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", eof)
    runpy.run_module("calculator", run_name="__main__")
    assert "Calculator." in capsys.readouterr().out
