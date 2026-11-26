# Hybrid HTML Report Scaffold and Delivery Protocol

Internal method ID: `architecture-survey`. Supporting resource for `skills/architecture-survey`.

This resource defines the self-contained HTML report architecture and the non-destructive delivery protocol for architectural surveys.

---

## 1. Storage and Delivery Protocol

To maintain complete repository cleanliness, architectural reports must never be written into the product codebase or Git working tree:

1. **Target Directory:** Resolve the operating system temporary directory:
   - Linux/macOS: `$TMPDIR` (falling back to `/tmp`).
   - Windows: `%TEMP%` or `os.environ.get("TEMP")`.
2. **File Naming:** Write to a uniquely stamped file:
   - Pattern: `<tmpdir>/architecture-survey-<timestamp>.html` (e.g. `architecture-survey-20261102-143000.html`).
3. **Execution Launcher:** Open the file via the host platform default handler, while providing the absolute path directly in chat:
   - Windows: `start <path>`
   - macOS: `open <path>`
   - Linux: `xdg-open <path>`
   - Remote / Headless Environments: Print the absolute path and terminal summary card without failing if a GUI browser is unavailable.

---

## 2. Terminal-Native Executive Summary Card (Chat Preview)

To prevent semantic split-brain and avoid stealing focus in remote environments, print an executive summary card in the chat session derived from the exact same candidate data:

```
+-----------------------------------------------------------------------------+
| ARCHITECTURE SURVEY CANDIDATE: Collapse Order Intake Pipeline               |
+-----------------------------------------------------------------------------+
| Recommendation: STRONG | Dependency: in-process                             |
| Affected Files: src/orders/OrderController.ts, OrderValidator.ts, ...       |
|                                                                             |
| Problem  : Every order caller sequences validation, tax, the transaction    |
|            and the email itself across 4 shallow modules.                   |
| Solution : Absorb the 4 pass-through modules into one order intake module   |
|            that owns the transaction.                                       |
|                                                                             |
| Wins:                                                                       |
|   - locality: tax rules in one module                                       |
|   - leverage: one interface, three callers                                  |
|   - tests hit one interface                                                 |
|                                                                             |
| Report: /tmp/architecture-survey-20261102-143000.html                       |
+-----------------------------------------------------------------------------+
```

Print one card per candidate, strongest first, then the "Also found" items one line each, then the report path, then the question "Which of these would you like to explore?". The cards and the HTML report come from the same candidate data, so they never disagree. Neither names a method or signature for the deepened module yet.

---

## 3. The Hybrid HTML Scaffold

The scaffold utilizes progressive enhancement: when an internet connection is available, Tailwind CSS and Mermaid.js render rich typography and flowcharts. When offline or air-gapped, embedded fallback styles and inline SVG geometry ensure the report remains completely legible.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Architecture Survey - {{repo_name}}</title>
  
  <!-- Online Progressive Enhancement via CDN -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" onerror="this.onerror=null;this.dataset.failed=true;">
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' });
  </script>

  <!-- Offline & Air-Gapped Fallback CSS -->
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #0f172a; margin: 0; padding: 2rem 1rem; line-height: 1.5; }
    .survey-container { max-width: 64rem; margin: 0 auto; }
    .candidate-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .badge-strong { background: #dcfce7; color: #166534; }
    .badge-explore { background: #fef3c7; color: #92400e; }
    .badge-speculative { background: #f1f5f9; color: #475569; }
    .badge-dep { background: #e0e7ff; color: #3730a3; margin-left: 0.5rem; }
    .diagram-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.25rem 0; }
    @media (max-width: 768px) { .diagram-grid { grid-template-columns: 1fr; } }
    .diagram-panel { border: 1px solid #cbd5e1; border-radius: 0.5rem; padding: 1rem; background: #f8fafc; min-height: 20rem; }
    .seam { stroke-dasharray: 4 4; stroke: #64748b; }
    .leak { stroke: #dc2626; }
    .deep { background: linear-gradient(135deg, #0f172a, #1e293b); color: #ffffff; }
    .adr-callout { background: #fffbeb; border-left: 4px solid #f59e0b; padding: 0.75rem 1rem; margin-top: 1rem; border-radius: 0 0.375rem 0.375rem 0; font-size: 0.875rem; color: #92400e; }
    .top-rec { background: #f0fdf4; border: 2px solid #22c55e; border-radius: 0.75rem; padding: 1.5rem; margin-top: 3rem; }
  </style>
</head>
<body class="bg-slate-50 text-slate-900 font-sans">
  <main class="survey-container space-y-8">
    
    <!-- Header with Compact Legend (No prose throat-clearing) -->
    <header class="border-b border-slate-200 pb-4">
      <h1 class="text-2xl font-bold tracking-tight text-slate-900">Architecture Survey: {{repo_name}}</h1>
      <p class="text-xs text-slate-500 font-mono mt-1">Generated: {{timestamp}} | Focus: Subsystem Friction & Deepening Opportunities</p>
      
      <!-- Compact Schematic Legend -->
      <div class="mt-4 flex flex-wrap gap-4 text-xs font-mono text-slate-600 bg-white p-3 rounded-md border border-slate-200">
        <span class="flex items-center"><span class="w-3 h-3 bg-slate-900 mr-1.5 rounded-sm"></span> Deep Module</span>
        <span class="flex items-center"><span class="w-3 h-3 bg-white border border-slate-400 mr-1.5 rounded-sm"></span> Shallow module</span>
        <span class="flex items-center"><span class="w-4 h-0 border-t-2 border-dashed border-slate-500 mr-1.5"></span> Seam</span>
        <span class="flex items-center"><span class="w-4 h-0 border-t-2 border-red-600 mr-1.5"></span> Leakage</span>
      </div>
    </header>

    <!-- Candidates Section -->
    <section id="candidates" class="space-y-6">
      
      <article id="{{candidate_id}}" class="candidate-card">
        <!-- Title and Badges -->
        <div class="flex items-center justify-between flex-wrap gap-2">
          <h2 class="text-lg font-bold text-slate-900">{{candidate_title}}</h2>
          <div>
            <span class="badge badge-strong">{{strength_badge}}</span>
            <span class="badge badge-dep">{{dependency_category}}</span>
          </div>
        </div>

        <!-- Affected Files -->
        <div class="mt-2 text-xs font-mono text-slate-600 bg-slate-100 p-2 rounded">
          <strong>Files:</strong> {{file_list}}
        </div>

        <!-- Before / After Diagram Grid -->
        <div class="diagram-grid">
          <div class="diagram-panel">
            <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">Before</span>
            <!-- Before diagram component (Mermaid or HTML/SVG) -->
          </div>
          <div class="diagram-panel">
            <span class="text-xs font-semibold uppercase tracking-wider text-emerald-600">After</span>
            <!-- After diagram component (Mermaid or HTML/SVG) -->
          </div>
        </div>

        <!-- Problem & Solution (Exactly 1 sentence each) -->
        <div class="space-y-2 text-sm mt-4">
          <p><strong class="text-slate-900">Problem:</strong> {{problem_sentence}}</p>
          <p><strong class="text-slate-900">Solution:</strong> {{solution_sentence}}</p>
        </div>

        <!-- Wins List (<= 6 words per bullet) -->
        <div class="mt-4">
          <span class="text-xs font-bold uppercase tracking-wider text-slate-700">Wins:</span>
          <ul class="list-disc list-inside text-xs text-slate-800 space-y-1 mt-1 font-mono">
            <li>{{win_1}}</li>
            <li>{{win_2}}</li>
            <li>{{win_3}}</li>
          </ul>
        </div>

        <!-- Optional ADR Callout -->
        {{#if adr_callout}}
        <div class="adr-callout">
          <strong>ADR Note:</strong> {{adr_callout_text}}
        </div>
        {{/if}}
      </article>

    </section>

    <!-- Also Found: findings not proposed, one line each -->
    <section id="also-found" class="text-sm text-slate-700">
      <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500">Also found</h3>
      <ul class="list-disc list-inside mt-1">
        <li>{{kept_module}}: kept, deletion test scatters its rules across callers</li>
        <li>{{untested_area}}: untested; {{what blocks testing through its interface}}</li>
      </ul>
    </section>

    <!-- Top Recommendation Section -->
    <section id="top-recommendation" class="top-rec">
      <h3 class="text-base font-bold text-emerald-900 uppercase tracking-wide">Top Recommendation</h3>
      <p class="text-sm text-slate-800 mt-2 font-medium"><a href="#{{top_rec_id}}">{{top_rec_name}}</a></p>
      <p class="text-xs text-slate-600 mt-1">{{top_rec_rationale}}</p>
    </section>

  </main>
</body>
</html>
```

---

## 4. Offline Behaviour and Final Checks

- The embedded `<style>` block styles every class the fallback needs, so the cards, badges, legend and top recommendation read without the Tailwind CDN.
- A Mermaid block shows its source text when the Mermaid CDN is unreachable. Draw at least one diagram per card as hand-built HTML or SVG (patterns 2-5 in the diagram resource) so each card keeps a picture offline.
- The header holds the repository name, the date and the legend, then goes straight into the candidates: no introduction paragraph.
- The only scripts are the Tailwind stylesheet and the Mermaid import; the report is otherwise static.
- Before handing over the path, open the file once or read it back and confirm every card has its files, problem, solution, wins, both diagram panels, strength badge and dependency category, and that the top recommendation links to a card id.
