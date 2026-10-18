import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUNTIME = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/build/andino-unified-candidate')
RAW = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/docs/validation/andino-unified/actor-inputs/batch-2.json')


def method(identifier, reason, insight):
    path = RUNTIME / 'skills' / identifier / 'GUIDE.md'
    return {'id': identifier, 'path': path.as_posix(),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'reason': reason, 'insight': insight}


choices = {
    '5ad2fb667acf': ([], 'Direct summary of an accepted mechanical rename; no method or acceptance claim is needed.'),
    '52ac50f632f2': ([], 'Obvious increment narration is explicitly excluded from documentation-and-adrs; explain the boundary without loading a method solely to refuse.'),
    '4c9b5e6b8815': ([('verification', 'The requested action is to observe current test results.', 'Run the existing real suite command, inspect case counts and skips, and bind its result to tested bytes; do not infer pass from exit zero alone.')], 'Verification governs suite evidence; no behavior is being changed and no TDD cycle is needed.'),
    '2945d7ddf125': ([('specification', 'Settled billing decisions need a buildable contract.', 'Reuse settled billing intent, state falsifiable criteria and public seams, and preserve existing spec format rather than reopen discovery or invent a duplicate plan.')], 'Current phase is specification, not implementation.'),
    'cb7dbafba722': ([('project-configuration', 'Local tracker mapping and triage vocabulary are explicit project configuration.', 'Map canonical triage roles to existing label strings, keep category separate from state, and merge one pointer into the actual host instruction file without external label creation.')], 'Local docs only; no tracker or global configuration mutation is implied.'),
    '5af5921054aa': ([('idea-refine', 'A rough collaborative-editing direction needs an assumption test.', 'Make presence solving coordination the riskiest bet, compare meaningful directions, and bound a one-job MVP with explicit non-goals such as offline sync.')], 'Refinement precedes implementation; no prototype is needed until a concrete uncertainty requires one.'),
    '35a0077b5dc6': ([('observability-and-instrumentation', 'Payment retry origins need distinguishable operational evidence.', 'Set entryPoint at scheduler/replay origin and propagate it with correlation; correlation alone does not establish origin, and labels must remain bounded.'), ('tdd', 'Adding observable retry attribution changes executable behavior.', 'Drive one log-attribution contract through its public retry seam: fail when scheduler/replay origins are indistinguishable, then minimally propagate origin.')], 'Instrumentation and regression are distinct current needs; no current incident or performance tuning is established.'),
    '7aaee84047e6': ([('api-and-interface-design', 'Adding invoice totals changes an existing public API boundary.', 'Read existing provider and consumers, preserve ordering/null/error contracts, and define the additive total field before implementation instead of making callers choose competing versions.'), ('tdd', 'The new API response behavior needs executable protection.', 'Use a literal invoice example with an independently computed total at the accepted API seam; observe its missing/wrong total before implementation.')], 'No product rediscovery or unrelated API redesign is needed.'),
    '97adb1b99213': ([], 'A direct native file listing is sufficient; no architecture scan, graph generation or method is implied.'),
    '1c5886e258e4': ([('incremental-implementation', 'The next specified API slice is a dependency-ready increment.', 'Consume the existing graph, select the smallest ready complete API path, preserve failed ancestor gates, and keep owned files and acceptance attached to the same plan.'), ('tdd', 'Building the API slice changes executable behavior.', 'Implement one specified public API behavior at a time, with an assertion RED for the right reason followed by minimal GREEN.')], 'Existing interfaces/specification are settled; release planning/specification and do not load anticipated completion specialists.'),
    '5378d05d3e6e': ([('agent-document-authoring', 'The deliverable is an agent-facing procedure with faulty triggers and completion bounds.', 'Separate distinct branch triggers from shared ordered actions, front-load pointer conditions, and give every branch an observable demanding done bound without deleting required behavior.')], 'This edits a durable procedure, not a native skill/router system.'),
    '3d17a0dd1324': ([('code-review', 'The user requests review including owned untracked files.', 'Pin the actual review scope, include staged/unstaged and owned new bytes, and preserve independent Spec and Standards verdicts; HEAD-only review can omit the change.')], 'Current phase is review, with no automatic rewrite or merge.'),
    '7b8f67c0de48': ([('architecture-survey', 'A bounded order-subsystem survey asks for evidenced deepening candidates.', 'Trace one order concept through real callers and tests, apply the deletion test, and report strength plus locality/test consequences; allow a finding of no worthwhile candidate.')], 'Survey before interface design; no speculative deep-module rewrite or whole-repository scan.'),
    'e08782084ea0': ([], 'Explaining a healthy existing cache needs targeted reading and direct explanation; neither debugging nor speculative performance tuning is triggered.'),
    '36feb4262cb5': ([('decision-interview', 'A personal preference belongs to the user and cannot be established by factual research.', 'Separate inspectable dashboard facts from the user-owned color preference and ask one discriminating preference question; do not invent their answer.')], 'No visual design/evaluation has been requested yet, and primary-source research cannot decide taste.'),
    'adfe38adca99': ([('debugging', 'Cross-tenant cache output is a reported unknown-cause bug.', 'Reproduce two tenant lookups with the same key at the public seam before diagnosing; compare identity and boundary data and test one falsifiable cause, rather than assume the cache is guilty.')], 'Load debugging before source/logs; regression and security remedies wait for evidenced cause/current phase.'),
    '4ca6b6700667': ([], 'A private local-variable rename is a targeted mechanical edit; no public interface, migration or architecture method.'),
    'ad962d2c7fea': ([('handoff', 'Work must travel to a colleague in another checkout.', 'Use durable reachable artifact pointers, preserve scope/permissions, decisions and evidence, and give the recipient one concrete safe next action after drift reconciliation.')], 'Prepare a portable artifact; no background host, agent or duplicate plan is implied.'),
    '3a62a9e3ac0a': ([], 'A README typo is a direct static edit; no TDD, CI or release method is needed.'),
    'd6e6853eae28': ([('article-shaping', 'The input is a fixed pile intended for a final article.', 'Read the pile end to end without overwriting it, ground prerequisite concepts before dependent claims, and write to a separate output without invented personal evidence.')], 'User explicitly requests the final article, so direct final drafting overrides the guide default of collaborative incremental approval; writing-fragments is excluded.'),
    'c0d38829fba5': ([('learning-workspace', 'The user explicitly wants several lessons in a learning folder.', 'Build one tangible safe-retry lesson from trusted sources, use retrieval and feedback, and record demonstrated understanding separately from content merely covered.')], 'No schedule, automation, or unsolicited course scaffolding is implied.'),
    '1faa1ed6c8b3': ([('context-engineering', 'The current need is a bounded packet that keeps scope/error and drops obsolete logs.', 'Compress resolved history to decision plus evidence breadcrumb, protect binding scope and the current failure, and reuse the existing checkpoint rather than duplicate the plan.')], 'Context selection owns this request; another person/host transfer is not stated, so a separate handoff method adds no distinct need.'),
    '587b325770f9': ([('implementation', 'The invoice retry ticket is already approved for implementation.', 'Resolve the exact accepted ticket and ready dependencies, preserve current work, and implement its accepted behavior under one parent checkpoint without reopening intent.'), ('tdd', 'Implementing retry behavior needs a demonstrably sensitive regression.', 'Choose one approved public retry behavior and a literal expected outcome; RED must fail for that behavior before minimal GREEN, with real collaborators where safe.')], 'No reinterview, fresh spec, or speculative idempotency redesign; accepted contracts stand.'),
    '360fbe25a5c2': ([('ci-cd-and-automation', 'The requested change wires an executable quality pipeline.', 'Use actual repository commands and preserved check names, model lint/unit/build/release dependencies, and show a failed ancestor blocking advancement while hosted protection remains separately unverified.'), ('tdd', 'The pipeline failure-blocking rule is observable executable behavior.', 'Drive one failure-propagation contract RED then GREEN: a failed lint ancestor must prevent build/release readiness, rather than merely testing the green path.')], 'Release readiness is a pipeline gate here; no deployment or recurring workflow design is requested.'),
    '246432375a1a': ([], 'Two plus three is five; answer directly without repository inspection or mutation.'),
    '800f809b56fa': ([], 'Universal TypeScript restructuring is explicitly excluded: deterministic boundary enforcement requires an already accepted concrete deep-package layout. No blanket reorganization.'),
    '44c630f34d7e': ([('deprecation-and-migration', 'A public name/full_name schema migration must coexist with old clients.', 'Expand additively, retain dual writes through backfill and read switch, and guard later contract on measured zero old readers/writers; code rollback cannot resurrect dropped data.')], 'Current request is the migration phases/guarded contract; no live data or deployment action is implied.'),
    '8d19111bb034': ([('stakeholder-questionnaire', 'Launch capacity and retention facts are held by the platform owner.', 'Map each capacity/retention decision gap to one owner-appropriate question with an answer stub; prepare one local document and do not invent a deadline or send it.')], 'The output is a draft for the knowledge holder, not an interview with the sender.'),
    '4d48c2b89af5': ([('plan-execution', 'An existing plan resumes after drift inspection.', 'Compare completed-task identities and current bytes, invalidate only affected evidence, and select the dependency-ready frontier while preserving verified completed work.')], 'Keep the accepted plan; do not restart planning or automatically create a branch.'),
    'ad15210b7f8f': ([], 'Recreating all plans without evidence conflicts with one durable plan and evidence reuse; retain current plans and require a concrete changed need before replanning.'),
    'b9f721de7bc3': ([('security-and-hardening', 'Owned-path cleanup and SQL input cross filesystem/data trust boundaries.', 'Resolve links, require a strict owned descendant with corroborated ownership before teardown, and prove injected text stays a parameter rather than SQL structure; a marker alone is insufficient under adversarial conditions.')], 'No deletion is authorized by validation; no scanner/live-environment use is claimed.'),
    '98fa914fb8f5': ([('verification', 'Worker self-report is being offered as acceptance evidence.', 'Inspect actual produced bytes and integration checks against criteria before accepting; done text does not establish pass, and affected evidence expires after drift.')], 'Decline the unsupported pass claim and obtain real evidence; no new worker is required.'),
    '0304b7c94b26': ([('primary-source-research', 'The explicit current request is framework research, separate from implementation.', 'Define the bounded framework question and consuming decision, then trace factual findings to the owning primary sources with dates/versions; do not invent current evidence.')], 'Selection-only probe: no source retrieval/network is authorized in this actor. Source-driven implementation is irrelevant; no integration/alternative solution decision is stated to require Search First.'),
    '4552083726eb': ([], 'fromAny is a test-fixture escape hatch, explicitly excluded from production runtime validation. Do not apply fixture migration globally or replace actual boundary validation.'),
    '03a09343cf18': ([('documentation-and-adrs', 'The accepted queue decision needs an ADR in the existing convention.', 'Inspect ADR-004 numbering/markup and write the next .rst record without rewriting history; preserve the throughput caveat and distinguish limits from guarantees.')], 'Preserve the actual convention and rationale; no new decisions directory, publication or commit.'),
    '80778696001c': ([('human-procedure', 'Credential dashboard access is explicitly human-only.', 'Use verified dashboard stages, classify each value source/destination and secrecy, and provide resumable manual steps without secret echo or requesting credentials in chat.')], 'No invented dashboard path or external credential write; unavailable current journey evidence must remain unverified.'),
    '082c8d19b4bb': ([('plan-execution', 'The complete accepted graph is ready for task continuation.', 'Use verified producer evidence to select the next ready node and preserve the existing graph; do not run planning again or treat a completed checkbox as proof.')], 'Complete graph means an already supplied task graph, not permission to replan or skip acceptance.'),
    '289d07b21a28': ([], 'Two independent audits can be bounded, but this delegated actor is explicitly prohibited from nested spawning. Use sequential bounded review if work were supplied; no dispatch or child use is claimed.'),
}

cases = json.loads(RAW.read_text(encoding='utf-8'))['selection_cases']
assert len(cases) == 38 and len({case['id'] for case in cases}) == 38
assert set(choices) == {case['id'] for case in cases}
selection_results = []
for case in cases:
    selected, note = choices[case['id']]
    unavailable = []
    if case['id'] == '289d07b21a28':
        unavailable = [{'id': 'delegation', 'boundary': 'Execution denied: parent explicitly prohibits nested agents. Tools being exposed does not grant authority.'}]
    selection_results.append({'id': case['id'], 'selected': [method(*choice) for choice in selected],
                              'unavailable': unavailable, 'note': note})

work = json.loads((ROOT / 'work.json').read_text(encoding='utf-8'))
results = {
    'host': {'surface': 'Codex delegated agent', 'model': 'UNKNOWN', 'version': 'UNKNOWN',
             'scope': 'resource activation and fixture actions'},
    'selection_results': selection_results,
    'work': work,
    'limitations': [
        'Selection snapshots establish actual resource activation and task-specific procedural understanding, not execution of 38 separate product requests.',
        'Only the supplied Python fixture was changed and executed; no network, live services, installs, global configuration, external mutation, Git mutation or nested agents.',
        'The framework research selection has no factual source findings or current-version verification under the allowed-read and no-network boundaries.',
        'Delegation execution is unavailable because nested agents are expressly prohibited; no tool absence or invented dispatch is claimed.',
        'Host model and version are not exposed for this measurement and are reported UNKNOWN.',
    ],
}
(ROOT / 'results.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')

loaded_ids = sorted({choice[0] for choices_for_case, _ in choices.values() for choice in choices_for_case}
                    | {'delegation', 'workflow-specification'})
activation = {
    'mechanism': 'Actual permitted Codex filesystem reads through rtk proxy shell; guide reads precede task-governed work. Metadata discovery was not counted as activation.',
    'runtime': {'path': (RUNTIME / 'SKILL.md').as_posix(), 'sha256': hashlib.sha256((RUNTIME / 'SKILL.md').read_bytes()).hexdigest()},
    'focus': {'path': 'C:/Users/Lenovo/.agents/skills/focus/SKILL.md',
              'sha256': hashlib.sha256(Path('C:/Users/Lenovo/.agents/skills/focus/SKILL.md').read_bytes()).hexdigest(),
              'references_read': ['references/priority-a.md', 'references/human-language-indonesia.md', 'references/human-language-english.md'],
              'state': 'ACTIVE', 'application': 'Concise result-first status, explicit limits, exact JSON output schema; no extra lifecycle.'},
    'internal_guides_read': [method(identifier, 'Resource read, reused while loaded; case-specific reasons are in results.json.',
                                   'ACTIVE does not by itself establish product-task execution.') for identifier in loaded_ids],
    'resources_read': ['skills/debugging/resources/contract.md', 'skills/tdd/resources/contract.md', 'skills/verification/resources/contract.md'],
    'released': [
        {'id': 'workflow-specification', 'reason': 'A considered candidate was read, then released: the pipeline request is executable CI quality-gate wiring, not recurring-workflow design. This was an extra exploratory guide load, not selected in the final minimum set.'},
        {'id': 'delegation', 'reason': 'Guide was read for the conditional parallel-audit case; actual nested dispatch is prohibited, so no execution/use is claimed.'},
    ],
    'work_used': [method('debugging', 'Unknown pagination cause before fixture source inspection.', 'Observed exact overlap, confirmed the wrong-stride prediction with sizes 1/2/3 and preserved original source.'),
                  method('tdd', 'Executable pagination fix.', 'Literal second-page assertion failed before changing the single stride expression and passed after; faulty original failed again.'),
                  method('verification', 'Accept fixed fixture only with actual evidence.', 'Inspected 5-test suite, original scenario, faulty-copy failure and tested file identities.')],
    'tool_limits': ['The first rtk tree command did not yield an inventory; rtk proxy rg --files succeeded. No hook was installed.',
                    'One nested PowerShell variable extraction failed because the outer shell expanded it; Python extraction succeeded. No evidence was inferred from the failed command.'],
}
(ROOT / 'activation.json').write_text(json.dumps(activation, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'cases': len(selection_results), 'selected_guides': len(loaded_ids) - 2,
                  'work_status': work['status'], 'results': str(ROOT / 'results.json')}))
