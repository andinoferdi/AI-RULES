# Council

An AI-RULES decision-analysis skill. The **Council** takes a real high-stakes question through five viewpoints, anonymized peer review, and a decision with one practical first move.

Adapted as an independently written workflow inspired by [aiwithremy/claude-skills-llm-council](https://github.com/aiwithremy/claude-skills-llm-council). The original project credits Ole Lehmann and Andrej Karpathy's LLM Council approach. This is not a claim of upstream endorsement or a copy of upstream source text.

## Scope and coexistence

Council evaluates decisions; it does not execute changes, replace Andino Workflow's routing or lifecycle, or act as a communication-style override. **Focus** supplies the current A. PRIORITAS and Indonesian/English human-language references. `ai-rules setup` installs Focus as Council's dependency. Use the normal host activation mechanism; installing a skill does not prove that an agent loaded or used it.

Council is useful for competing technical approaches, a major product change, a hard research direction, or a consequential strategy. It is unnecessary for factual questions, minor preferences and ordinary text generation.

## Install through AI-RULES

From a clean checkout of the installer branch (`main`):

```sh
python -m pip install --editable .
ai-rules setup --capability council --host codex
```

Use `--host claude-code`, `opencode`, `antigravity-cli`, or `antigravity-ide` when appropriate. `ai-rules setup` also offers Council in **Custom** selection and the **Everything** profile. For project scope, add `--scope project --project-root <path>`. Re-running setup checks the configured latest Council branch; user-modified and unrecognized skill directories are preserved.

For manual installation of Council and its full folder (not just `SKILL.md`):

```sh
git clone --depth 1 --single-branch --branch council https://github.com/andinoferdi/AI-RULES.git ~/.agents/skills/council
```

Choose the host's actual skill directory. For Claude Code use `~/.claude/skills/council`, OpenCode uses `~/.config/opencode/skills/council`, Antigravity IDE uses `~/.gemini/config/skills/council`, and Antigravity CLI uses `~/.gemini/antigravity-cli/skills/council`. For project scope, use `.agents/skills/council` in supported agents or `.claude/skills/council` for Claude Code. Install Focus separately if you do not use the CLI.

## Invocation and limitations

- Codex: `$council <decision>`
- Claude Code: `/council <decision>`
- OpenCode or Antigravity: ask the agent to use `council` via its supported skill invocation

Example: `Council this: should we refactor the authentication service or replace it?`

A real independent Council needs a host that supports sub-agents. Without them the skill must disclose a **single-agent perspective review**; it cannot claim that five independent advisors or anonymous peer reviewers ran. The method does not require five different commercial models. The agent must use only authorized tools and material.

## Quick checks

**Positive:** Ask Council to compare three migration paths with cost, reversibility and time limits. Expect independent advice if supported, anonymized reviews, a justified verdict, and one next action.

**Positive (Indonesian):** `Council, lebih baik skripsi ini pakai pendekatan A atau B dengan data yang tersedia?` Expect natural Indonesian, the actual evidence limits, and preserved Andino/Fokus boundaries.

**Negative:** `Berapa 2 + 2?`, `ringkas artikel ini`, or `ganti warna tombol` should not invoke Council implicitly.

**Fidelity:** On a host without sub-agents, the response must not claim five agents or peer review ran.

## Package and verification

This distribution branch contains only `README.md` and `SKILL.md`. The source, tests, and packaging checks live in the [AI-RULES main branch](https://github.com/andinoferdi/AI-RULES/tree/main); the [family standard](https://github.com/andinoferdi/AI-RULES/blob/main/docs/agent-skill-family-standard.md) defines package and release quality expectations. CLI setup verifies installed artifacts; native host discovery and actual behavior require separate observation.
