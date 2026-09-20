# Quantitative foundations and planning

Use for quantitative design or analysis planning; explain technical terms in plain language. Start from the question and target quantity (estimand), not a software menu or a preferred statistical test.

## Fit and design

Determine whether the question needs magnitude/frequency/distribution, comparison, association, prediction, intervention effect or numerical evaluation. Experience/meaning/process may require a qualitative or integrated design. Return QUANTITATIVE_FIT, QUANTITATIVE_POSSIBLE, MIXED_METHOD_CANDIDATE, OTHER_DESIGN_BETTER or NEEDS_CLARIFICATION with rationale; these are fit outcomes, not field statuses.

Choose descriptive, cross-sectional associational, comparative observational, longitudinal observational, experimental, quasi-experimental or evaluation logic. State time structure, unit and inference limits. Survey is a collection/design strategy, not automatically a causal experiment. A pre/post measure alone does not establish random assignment, control or a counterfactual. Do not transform a descriptive question into a causal one for sophistication.

## Construct to measurement

Trace concept → defined construct → operational definition/indicator → recorded variable → interpretation limit. Specify response format, scale/data properties, unit, population/language/culture fit and scoring. Use predictor/outcome, treatment, mediator, moderator, confounder, covariate, grouping or time roles only when justified; descriptive studies can have measures without X/Y.

Choose or adapt instruments from the measurement need and actual source evidence. Do not generate valid-sounding questionnaire items from variable names alone. Inspect construct coverage, comprehensibility, response options, leading/double-barreled wording, ordering/burden, translation/adaptation, permissions and pilot needs. Validity/reliability from another context does not automatically transfer; an alpha coefficient alone is not proof of validity and reliability procedures are model-dependent. Do not fabricate pilot or measurement results.

Before analysis, build a variable dictionary: name/meaning, construct/source, coding, nominal/ordinal/continuous or other data properties, unit, role, missing-value convention and planned transformation. Distinguish single items from justified composite scores; select summaries from meaning/properties rather than software defaults.

## Survey and sampling

Link objective → target population/unit → sampling frame/access → strategy/sample rationale → questionnaire/measurement → mode/recruitment → pilot/administration → response/nonresponse/data quality → coding/analysis. Consider coverage, selection, nonresponse, recall/social-desirability, measurement and mode effects where applicable.

Explain inclusion/exclusion and how selection was or will be implemented. Probability and non-probability strategies have different inference limits; convenience access is not evidence of representativeness. Sample-size rationale depends on target precision/power or information need, effect assumptions, design/clustering, planned analysis, attrition/nonresponse and feasibility. Do not assert a universal 30/100/200 respondent threshold or compute a formula with invented assumptions.

## Experiment or quasi-experiment

Specify intervention, comparator, assignment mechanism/unit, outcomes/measurement, timing/repeated structure, implementation/fidelity, attrition/contamination, ethics and analysis. Distinguish random allocation from random sampling. Inspect baseline differences, confounding, maturation/history, testing/instrument changes and other design-relevant threats. Use the actual comparison/assignment to bound causal ambition; regression adjustment or a small p-value cannot independently repair unsupported causal design.

## Collection, cleaning and analysis plan

Plan access/consent, collector/training, procedure/timing, coding/data entry, quality checks, missingness and secure storage. Preserve original data and an auditable transformation record. Check ranges, impossible values, justified duplicates and coding errors. Never remove observations, recode categories, impute or trim outliers to obtain significance.

Quantify missing data by variable/pattern and inspect plausible collection/coding causes. Justify handling and consider bias/uncertainty and sensitivity; do not default to deleting all incomplete rows, mean filling or assuming missing completely at random.

Prespecify analysis before collection/inspection where possible. If already examined, distinguish retrospective/exploratory decisions from genuinely prior plans. Record RQ/objective, optional hypothesis, outcome/predictors/groups, estimand, design/sampling, repeated/clustered structure, sample size/sparsity, descriptive summaries, primary/secondary/exploratory analysis, assumptions/diagnostics, missingness, effect/interval reporting, multiplicity and sensitivity when relevant.

Describing this sample may need frequencies/proportions, center/spread, cross-tabulation or plots only. Estimating a population quantity requires an inference basis and uncertainty. Comparisons/associations/prediction require models fitting outcome, dependency structure and goal. Causal effects require design/identification reasoning before tests. Explain candidate analysis, rationale, required assumptions, checks, reporting and limitations; do not use 'two variables = correlation' as a universal lookup rule.

Hypotheses are optional, theory/design grounded and not rewritten after seeing outcomes while labeled a priori. Separate null/alternative, statistic, prespecified decision rule, estimate and uncertainty. No universal sequence of instrument tests → normality/classical assumptions → hypothesis tests; the sequence follows measurement/design/model. Unknown properties keep the plan provisional.

## Interpretation and readiness

A p-value assesses data compatibility with a specified null model under its assumptions; it is not the probability the hypothesis is true, effect magnitude or practical importance. Non-significance alone does not establish no effect. Report estimates, units, context-relevant magnitude and appropriate confidence/credible intervals where supported, with framework-specific interpretation. See the [ASA statement](https://www.amstat.org/docs/default-source/amstat-documents/p-valuestatement.pdf) for these interpretation cautions.

Check problem/quantitative fit, answerable RQ and causal scope, defined constructs/optional hypotheses, design/time structure, population/frame/access/sampling/sample rationale, instrument fit/adaptation/pilot evidence, collection/dictionary, ethics/privacy, analysis goal/model/diagnostics and effect/uncertainty reporting. Return QUANT_READY, QUANT_READY_WITH_OPEN_ITEMS, NEEDS_DESIGN_ALIGNMENT, NEEDS_MEASUREMENT_WORK, NEEDS_ANALYSIS_PLAN or BLOCKED with concrete dependencies. An unresolved material ethics/access decision prevents affected execution, even if statistical planning is ready. Use [quantitative templates](../assets/quantitative-templates.md) as adaptable records.
