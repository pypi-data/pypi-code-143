import circuitsvis
import circuitsvis.utils.render
from circuitsvis.tokens import colored_tokens


class TestAttention:
    def test_matches_snapshot(self, snapshot, monkeypatch):
        monkeypatch.setattr(circuitsvis.utils.render, "uuid4", lambda: "mock")
        monkeypatch.setattr(circuitsvis, "__version__", "1.0.0")

        res = colored_tokens(
            tokens=["a", "b"],
            values=[1, 2]
        )
        snapshot.assert_match(str(res))
