import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/build/andino-unified-candidate-v3')
INPUT = Path('C:/Users/Lenovo/Downloads/AI-RULES-main/docs/validation/andino-unified/actor-inputs-v2/batch-2.json')
FOCUS = Path('C:/Users/Lenovo/.agents/skills/focus')
SEARCH = Path('C:/Users/Lenovo/.agents/skills/search-first/SKILL.md')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(id, path, state='ACTIVE', action=None):
    return {'id': id, 'path': str(path), 'sha256': sha(path), 'state': state,
            'activation': 'Full relevant instructions read via rtk-prefixed permitted file reader.',
            'action': action}


def selected(id, reason, insight):
    path = SEARCH if id == 'search-first' else BASE / 'skills' / id / 'GUIDE.md'
    return {**identity(id, path), 'reason': reason, 'insight': insight}


# Authored from raw requests and the actual loaded instructions, without answer keys.
choices = {
    '5ad2fb667acf': ([], 'Direct summary of an accepted mechanical rename; no changed behavior or consequential acceptance claim.'),
    '52ac50f632f2': ([], 'Obvious increment narration is excluded from documentation-and-adrs. Root scope/quality rules suffice; no scenario edit performed.'),
    '4c9b5e6b8815': ([('verification', 'The current activity is executing checks and accurately reporting their result.', 'Record the actual command, runtime, exit and cases; a suite name alone is no passing evidence.')], 'Selection only; no repository suite executed.'),
    '2945d7ddf125': ([('specification', 'Accepted billing decisions need a buildable artifact, not renewed intent discovery.', 'Reuse settled decisions and existing spec convention; each criterion needs a falsifiable public seam.')], ''),
    'cb7dbafba722': ([('project-configuration', 'The requested local artifacts are tracker mapping and triage vocabulary.', 'Map roles onto existing label strings, keep category and state separate, and preserve the host-read instruction pointer.')], ''),
    '5af5921054aa': ([('idea-refine', 'A rough collaborative-editing direction needs a focused assumption test.', 'Test the riskiest coordination assumption with a one-job MVP and explicit non-goals; extra features do not validate it.')], ''),
    '35a0077b5dc6': ([('observability-and-instrumentation', 'The requested result is distinguishing retry origins in a common telemetry sink.', 'Set entryPoint at the scheduler/replay origin and propagate it; request correlation alone does not establish origin.'), ('tdd', 'This is an authorized observable behavior change with settled telemetry intent.', 'Assert actual structured event fields at the public sink; fail when entryPoint is absent before implementation.')], 'No payment-system actions performed.'),
    '7aaee84047e6': ([('api-and-interface-design', 'Adding invoice total changes an existing public response boundary.', 'Preserve consumer-visible shape and compatibility; reuse accepted contracts rather than invent a new API version.'), ('tdd', 'The additive API behavior is ready for regression/implementation, with other facts and seams settled.', 'Use the accepted public API seam and independent literal invoice expectations; observe RED before adding the field.')], 'No product discovery/specification phase reopened.'),
    '97adb1b99213': ([], 'Native bounded file listing is sufficient; an inventory request does not justify graph generation or architecture survey.'),
    '1c5886e258e4': ([('incremental-implementation', 'The request is the next already specified dependency-ready slice.', 'Consume the existing graph, implement a complete small path, and block dependent progression when a gate fails.'), ('tdd', 'This scenario is already in executable API implementation, not design.', 'Reuse the agreed API seam; one observable behavior must fail before the minimal implementation.')], ''),
    '5378d05d3e6e': ([('agent-document-authoring', 'The requested artifact is an agent-facing procedure with branch and completion defects.', 'Define distinct triggers and demanding observable completion bounds; shorter prose must preserve required technique.')], ''),
    '3d17a0dd1324': ([('code-review', 'The current activity is reviewing changes, expressly including untracked files.', 'Pin staged, unstaged and owned new bytes, and preserve separate Spec and Standards verdicts.')], ''),
    '7b8f67c0de48': ([('architecture-survey', 'This is a bounded request for evidenced deepening candidates in the order subsystem.', 'Trace actual caller friction; offer source-backed candidates or none worthwhile before interface design.')], ''),
    'e08782084ea0': ([], 'A healthy existing-cache explanation needs only relevant source evidence; no bug, redesign or performance issue is established.'),
    '36feb4262cb5': ([], 'Personal preference belongs to the user. Root decision-support rules require an unresolved human preference, not an invented color choice or a UI design project.'),
    'adfe38adca99': ([('debugging', 'Tenant B receiving tenant A results is a reported wrong output with unknown cause.', 'Reproduce the actual two-tenant sequence and trace identity/state before choosing a cache or authorization repair.')], 'Diagnosis phase only; do not pre-load implementation or assume the cache is the cause.'),
    '4ca6b6700667': ([], 'Private local-variable rename is a direct mechanical edit; no migration or public-interface method.'),
    'ad962d2c7fea': ([('handoff', 'A colleague in another checkout needs portable continuation.', 'Persist current state, decisions, permissions, exact reachable artifact pointers and a first concrete action; recipient checks drift.')], ''),
    '3a62a9e3ac0a': ([], 'Single README typo is direct static text work; no TDD or specialist ceremony.'),
    'd6e6853eae28': ([('article-shaping', 'A fixed raw-material pile is ready for an article, rather than fragment exploration.', 'Keep raw material read-only and ground concept dependencies; direct final-article authorization governs collaboration pace.')], ''),
    'c0d38829fba5': ([('learning-workspace', 'The user explicitly wants a sequence of lessons in a learning folder.', 'Choose a bounded mission and short lesson, cite trusted sources, and record demonstrated understanding rather than exposure.')], 'No lessons or recurring automation created.'),
    '1faa1ed6c8b3': ([('context-engineering', 'The requested bounded context packet must preserve scope and current failure while trimming history.', 'Keep binding scope and active error; compress superseded logs into evidence breadcrumbs in the existing checkpoint.')], ''),
    '587b325770f9': ([('implementation', 'An already approved invoice retry ticket is authorized and ready to build.', 'Resolve the actual accepted task and dependency frontier, preserve one owner, and implement without restarting product ideation.'), ('tdd', 'Approved retry behavior needs executable regression support in the current implementation phase.', 'Use the accepted public seam and literal outcomes; a production mutation must make the test fail.')], 'No ticket or payment actions performed.'),
    '360fbe25a5c2': ([('ci-cd-and-automation', 'The requested deliverable is a check graph whose failed ancestors prevent advancement.', 'Use real repository commands and preserve required check names; failed gates block every dependent stage.'), ('tdd', 'Dependency-blocking pipeline behavior has an observable regression contract.', 'A planted failing ancestor must prevent downstream advancement; demonstrate failure before changing executable gate logic.')], 'Hosted CI, protection and deployment remain untested.'),
    '246432375a1a': ([], 'Two plus three is stable direct explanation; repository work is explicitly excluded.'),
    '800f809b56fa': ([], 'Universal default restructuring is excluded by typescript-boundary-enforcement, which requires an explicitly accepted deep-package layout. Root scope rules resolve this.'),
    '44c630f34d7e': ([('deprecation-and-migration', 'The request explicitly asks for coexistence-safe schema transition while old clients remain.', 'Expand, dual-write, bounded backfill, switch reads, then contract only after verified old-consumer zero use; rollback must preserve data.')], 'Current output is transition design/showing phases; no live migration or implementation assumed.'),
    '8d19111bb034': ([('stakeholder-questionnaire', 'Launch capacity and retention facts must be obtained from the named platform owner.', 'Map each decision gap to one focused question and answer stub; draft locally, do not send without authority.')], ''),
    '4d48c2b89af5': ([('plan-execution', 'The user asks to resume the existing accepted plan after checking drift.', 'Compare current artifacts to recorded evidence, invalidate only affected acceptance, and select the ready frontier without redoing verified tasks.')], 'Load root handoff/execution-plan references as relevant; no new plan or speculative implementation phase.'),
    'ad15210b7f8f': ([], 'Restarting all plans without a cause contradicts reuse and drift contracts; root lifecycle suffices to preserve completed decisions/evidence.'),
    'b9f721de7bc3': ([('security-and-hardening', 'The requested checks concern destructive derived paths and SQL input trust boundaries.', 'Resolve and verify a strict owned descendant before cleanup; parameterized SQL must keep injection text as data, and no broad fallback delete is safe.')], 'No cleanup, SQL service or user-project action executed.'),
    '98fa914fb8f5': ([], 'A one-sentence greeting explicitly has no change or acceptance claim; no verification method needed.'),
    '0304b7c94b26': ([('search-first', 'Explicit technical research into a new unfamiliar framework is a present research need.', 'Research-only work returns sourced applicability and uncertainty; installation is not research or use.')], 'Selection-only scope and no-network instruction prevent actual research. Skill ACTIVE; no USED or external-fact claim.'),
    '4552083726eb': ([], 'test-fixture-migration expressly excludes production runtime validation. Root boundary resolves the requested misuse; no fixture-only method selected.'),
    '03a09343cf18': ([('documentation-and-adrs', 'The task records an accepted architectural decision using an established ADR convention.', 'Inspect existing numbering/markup and preserve throughput caveats, limitations and history; no competing default format.')], ''),
    '80778696001c': ([('human-procedure', 'The credential dashboard step is explicitly human-only and needs exact manual instructions.', 'Use verified dashboard journeys, name source/destination/secrecy, keep secrets in the human environment, and label unverified UI paths.')], 'No dashboard/browser/credential operations performed.'),
    '082c8d19b4bb': ([('plan-execution', 'A complete accepted task graph is ready to continue; it needs execution rather than another planning artifact.', 'Check current accepted producer evidence, select the next ready task, and preserve completed outcomes instead of decomposing again.')], 'The raw request does not identify the next task behavior, so do not pre-load a speculative implementation domain.'),
    '289d07b21a28': ([('delegation', 'The task explicitly asks for a read-only safety assessment of an authorized parent delegating two independent audits.', 'Check ready producer evidence, benefit, exposed child tools, and normalized disjoint write scopes; parent verifies outputs, maximum three direct children and no nesting.')], 'This actor does not spawn. Assessing the parent scenario is permitted selection work; inherited no-nesting does not erase its planning need.')
}

raw = json.loads(INPUT.read_text(encoding='utf-8-sig'))
assert set(choices) == {case['id'] for case in raw['selection_cases']}
selection_results = []
for case in raw['selection_cases']:
    entries, note = choices[case['id']]
    selection_results.append({'id': case['id'], 'request': case['request'],
                              'phase_preserved': True, 'selection_only': True,
                              'selected': [selected(*entry) for entry in entries],
                              'unavailable': [], 'note': note,
                              'scenario_actions': []})

guide_ids = sorted({entry[0] for entries, _ in choices.values() for entry in entries if entry[0] != 'search-first'})
resources = [identity('andino-workflow', BASE / 'SKILL.md', 'USED', 'Applied root routing, scope boundaries and fixture lifecycle.'),
             identity('focus', FOCUS / 'SKILL.md', 'USED', 'Applied clear concise progress/result communication without changing execution scope.')]
resources += [identity('focus/' + filename, FOCUS / 'references' / filename, 'USED', 'Applied installed communication contract.') for filename in ('priority-a.md', 'human-language-indonesia.md', 'human-language-english.md')]
resources += [identity('andino/' + filename, BASE / 'references' / filename, 'USED', 'Applied capability identity, phase and lifecycle selection.') for filename in ('routing.md', 'invocation-adapter.md', 'internal-method-index.md', 'execution-plan.md', 'handoff.md')]
resources += [identity(id, BASE / 'skills' / id / 'GUIDE.md', 'USED' if id in ('debugging', 'tdd', 'verification') else 'ACTIVE', 'See work.json observed fixture actions.' if id in ('debugging', 'tdd', 'verification') else None) for id in guide_ids]
resources.append(identity('search-first', SEARCH, 'ACTIVE', None))
resources += [identity(id + '/supporting-contract', BASE / 'skills' / id / 'resources' / 'contract.md', 'USED', 'Applied fixture evidence, literal oracle and faulty-copy regression checks.') for id in ('debugging', 'tdd', 'verification')]

results = {'host': {'surface': 'Codex delegated agent', 'model': 'UNKNOWN', 'version': 'UNKNOWN',
                    'observed_runtime': 'Python 3.12.10 on current Windows host'},
           'scope': {'resource_activation': 'Frozen Andino root/routing/index/selected guides and actual installed Focus references; installed Search First selected for the explicit research case.',
                     'fixture_actions': 'Only supplied pagination reproduction, isolated cause probe, local fix, regression and faulty-copy sensitivity within this batch directory.',
                     'selection_cases': 'Selection only; no scenario execution and no nested agents.'},
           'andino_content': {'path': str(BASE), 'root_sha256': sha(BASE / 'SKILL.md'), 'routing_sha256': sha(BASE / 'references/routing.md'), 'index_sha256': sha(BASE / 'references/internal-method-index.md')},
           'selection_results': selection_results, 'resource_activation': resources,
           'work': {'record': str(OUT / 'work.json'), 'status': 'DONE',
                    'methods_used': ['debugging', 'tdd', 'verification'],
                    'evidence': 'Exact reproduction, intended RED, isolated one-variable hypothesis confirmation, GREEN, fixture suite, faulty-copy failure and corrected original scenario recorded with commands and hashes.'},
           'unavailable': [],
           'limits': ['No native skill-picker invocation, cross-host parity, external research, live service or publication claim.',
                      'Resource reading establishes ACTIVE; selection-only cases do not establish scenario use.',
                      'The allowed raw fixture includes source; diagnostic actions began only after Focus and debugging instructions were loaded.'],
           'errors': [{'kind': 'output_truncation', 'detail': 'Some initial combined resource-read outputs were truncated; relevant instructions were re-read in smaller full outputs before their use.'},
                      {'kind': 'environment_notice', 'detail': 'rtk prints no-hook-installed notices; no global setup attempted. Child-process stderr captures the notice with Windows encoding artifacts; test assertion and exits remained legible.'}]}
(OUT / 'results.json').write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps({'selection_cases': len(selection_results), 'active_resources': len(resources), 'results': str(OUT / 'results.json'), 'results_sha256': sha(OUT / 'results.json')}, indent=2))
