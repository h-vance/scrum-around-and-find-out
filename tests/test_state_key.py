# SPDX-License-Identifier: Apache-2.0
"""The probe's state key depends on the session and on the local agents' endpoints, and on nothing else."""

from __future__ import annotations

from typing import Any

from agentsdata import agents_dict
from safo.agentsfile import parse_agents
from safo.hooks import state_key


def _key(data: dict[str, Any], session: str = "session-a") -> str:
    return state_key(session, parse_agents(data))


def test_editing_a_shape_description_keeps_the_key() -> None:
    before = _key(agents_dict())
    data = agents_dict()
    data["shapes"]["research"]["description"] = "a different description"
    assert _key(data) == before


def test_editing_a_non_ollama_role_keeps_the_key() -> None:
    before = _key(agents_dict())
    data = agents_dict()
    data["agents"]["claude-haiku"]["role"] = "a different role text"
    assert _key(data) == before


def test_changing_an_ollama_endpoint_url_changes_the_key() -> None:
    before = _key(agents_dict())
    data = agents_dict(a_url="http://127.0.0.1:9999")
    assert _key(data) != before


def test_changing_an_ollama_endpoint_models_changes_the_key() -> None:
    before = _key(agents_dict())
    data = agents_dict()
    endpoint = data["agents"]["ollama"]["endpoints"][0]
    endpoint["models"] = [*endpoint["models"], "extra-model"]
    endpoint["protected_models"] = [*endpoint["protected_models"], "extra-model"]
    endpoint["loaded_num_ctx"] = {**endpoint["loaded_num_ctx"], "extra-model": 8192}
    assert _key(data) != before


def test_a_different_session_changes_the_key() -> None:
    data = agents_dict()
    assert _key(data, "session-a") != _key(data, "session-b")
