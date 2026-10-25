# SPDX-License-Identifier: Apache-2.0
"""No hidden work, the no-issue marker: a brief with no tracking item may say why, when the operator set a marker."""

from __future__ import annotations

from typing import Any

from agentsdata import agents_dict
from safo.agentsfile import parse_agents
from safo.hooks import check_dispatch
from safo.tracking import Ref, State

MARKER = "issue: none -"


def dispatch(prompt: str, **hooks_over: Any) -> tuple[tuple[str, ...], list[Ref]]:
    """The rules a brief gets, and every reference the resolver was asked about."""
    data = agents_dict()
    data["hooks"] = {**data.get("hooks", {}), **hooks_over}
    seen: list[Ref] = []

    def resolve(ref: Ref) -> State:
        seen.append(ref)
        return "open"

    verdict = check_dispatch(parse_agents(data), {"prompt": prompt, "model": "sonnet"}, False, resolve, lambda: None)
    return verdict.rules, seen


def test_the_marker_is_off_by_default() -> None:
    rules, _ = dispatch("issue: none - a throwaway script", no_issue_marker="")
    assert rules == ("no-issue",)


def test_a_marker_with_a_reason_satisfies_the_rule_without_a_lookup() -> None:
    rules, seen = dispatch("issue: none - a throwaway script", no_issue_marker=MARKER)
    assert rules == ()
    assert seen == [], "a brief that gives a reason for no item is never looked up"


def test_a_marker_with_no_reason_does_not_satisfy_the_rule() -> None:
    rules, _ = dispatch(f"Summarise it.\n{MARKER}", no_issue_marker=MARKER)
    assert rules == ("no-issue",)


def test_the_marker_is_parsed_trimmed_and_lowercased() -> None:
    assert parse_agents({**agents_dict(), "hooks": {"no_issue_marker": "  Issue: None -  "}}).hooks.no_issue_marker == (
        MARKER
    )
