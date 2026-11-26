# Visual Diagram Patterns for Architecture Surveys

Internal method ID: `architecture-survey`. Supporting resource for `skills/architecture-survey`.

This resource specifies the 5 canonical visual diagram patterns used in architecture survey reports. Diagrams carry the substantive weight of the report and prose stays minimal. If a diagram needs a paragraph of explanation to be understood, redraw the diagram.

Pick the pattern that fits each candidate and mix them across the report; when every diagram looks the same, the report reads as generic. Use Mermaid when the relationships are graph-shaped (call graphs, dependencies, sequences such as "before: 6 round-trips; after: 1") and hand-built HTML or SVG for the editorial visuals (deep-module boxes, cross-sections, mass diagrams, collapses). Draw at least one diagram per card by hand: Mermaid needs its CDN, and a hand-built diagram still renders offline. Label diagrams with the real module and file names from the code being surveyed.

---

## Visual standards

- **Style:** Editorial, clean, schematic (not a bloated corporate dashboard).
- **Typography:** Monospaced or clean sans-serif; `text-xs uppercase tracking-wider` for internal module labels so they read as schematic blueprints.
- **Color Palette:**
  - Backgrounds: Neutral light stone/slate (`#f8fafc`, `#f1f5f9`).
  - Deep Modules: Heavy slate/dark gradient (`#0f172a` to `#1e293b`).
  - Leakage / Anti-Patterns: Crimson red (`#dc2626`).
  - Justified Seams: Emerald green (`#059669`) or Indigo (`#4f46e5`).
  - Faded Internals: Light slate (`#94a3b8`, `#cbd5e1`).
- **Dimensions:** Keep all diagram panels approximately `320px` in height so side-by-side Before/After comparisons sit comfortably on desktop viewports without vertical scrolling.

---

## Pattern 1: Mermaid graph (dependencies and call flow)

**When to Use:** When illustrating complex call flows, messy dependency webs, or multi-step round trips.

### Before: Messy dependencies and leaky seams
```html
<div class="rounded-lg border border-slate-200 bg-white p-4 h-80 flex flex-col justify-between">
  <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">Before: pass-through modules</span>
  <div class="flex-1 flex items-center justify-center">
    <pre class="mermaid">
      flowchart TD
        Caller[OrderController] --> V[OrderValidator]
        Caller --> P[PricingService]
        Caller --> DB[DatabaseWrapper]
        Caller -.leak.-> TX[Raw DB Transaction]
        Caller --> N[NotificationDispatcher]
        classDef leak stroke:#dc2626,stroke-width:2px,stroke-dasharray: 4 4;
        class TX leak;
    </pre>
  </div>
</div>
```

### After: Consolidated behind a single public seam
```html
<div class="rounded-lg border border-slate-200 bg-white p-4 h-80 flex flex-col justify-between">
  <span class="text-xs font-semibold uppercase tracking-wider text-emerald-600">After: Deep Module Behind Seam</span>
  <div class="flex-1 flex items-center justify-center">
    <pre class="mermaid">
      flowchart TD
        Caller[OrderController] -->|submitOrder| Intake[OrderIntake Deep Module]
        subgraph IntakeInternals [Encapsulated Behind Seam]
          V[Validation]
          P[Pricing Invariants]
          TX[Tx Boundary]
        end
        Intake --> Repo[(OrderRepository Seam)]
        classDef deep fill:#0f172a,stroke:#0f172a,color:#ffffff;
        class Intake deep;
    </pre>
  </div>
</div>
```

---

## Pattern 2: Hand-built boxes and arrows (CSS / SVG)

**When to Use:** When Mermaid auto-layout fights the desired emphasis, or when representing a thick-bordered deep module enclosing greyed-out internal functions.

```html
<div class="grid grid-cols-2 gap-4 my-4">
  <!-- BEFORE -->
  <div class="border border-slate-300 rounded-lg p-4 bg-slate-50 h-80 relative flex flex-col justify-between">
    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Before: 4 shallow modules</span>
    <div class="space-y-2 my-auto">
      <div class="p-2 border border-dashed border-red-500 bg-red-50 rounded text-xs text-red-800">OrderValidator.ts: one boolean check</div>
      <div class="p-2 border border-dashed border-red-500 bg-red-50 rounded text-xs text-red-800">OrderPricing.ts: forwards to tax table</div>
      <div class="p-2 border border-dashed border-red-500 bg-red-50 rounded text-xs text-red-800">OrderDbWrapper.ts: begin, insert, commit</div>
      <div class="p-2 border border-dashed border-red-500 bg-red-50 rounded text-xs text-red-800">OrderNotifier.ts: forwards to mailer</div>
    </div>
    <span class="text-xs text-red-600 font-mono">Caller coordinates all 4 files</span>
  </div>

  <!-- AFTER -->
  <div class="border-2 border-slate-900 rounded-lg p-4 bg-white h-80 relative flex flex-col justify-between shadow-sm">
    <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">After: 1 Deep Module</span>
    <div class="border-2 border-slate-900 rounded-md p-4 bg-slate-900 text-white my-auto">
      <div class="text-xs font-bold tracking-wider uppercase mb-2 border-b border-slate-700 pb-1">
        Public Interface: submitOrder(cmd)
      </div>
      <div class="grid grid-cols-2 gap-2 text-[10px] text-slate-400">
        <div class="bg-slate-800 p-1.5 rounded">internal: validation</div>
        <div class="bg-slate-800 p-1.5 rounded">internal: pricing tax</div>
        <div class="bg-slate-800 p-1.5 rounded">internal: tx commit</div>
        <div class="bg-slate-800 p-1.5 rounded">internal: notify queue</div>
      </div>
    </div>
    <span class="text-xs text-emerald-600 font-mono">Caller hits 1 public seam</span>
  </div>
</div>
```

---

## Pattern 3: Cross-section (layered shallowness)

**When to Use:** When diagnosing architectural pass-through layers where each layer does almost nothing except pass arguments to the layer below.

```html
<div class="grid grid-cols-2 gap-4 my-4">
  <!-- BEFORE: 5 Thin Pass-through Layers -->
  <div class="border border-slate-200 rounded-lg p-4 bg-white h-80 flex flex-col justify-between">
    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Before: Pass-Through Layers</span>
    <div class="space-y-1.5 my-auto">
      <div class="h-8 border-l-4 border-amber-500 bg-amber-50 px-2 flex items-center text-xs font-mono">Controller.handle()</div>
      <div class="h-8 border-l-4 border-amber-400 bg-amber-50/70 px-2 flex items-center text-xs font-mono">OrderManager.process()</div>
      <div class="h-8 border-l-4 border-amber-400 bg-amber-50/70 px-2 flex items-center text-xs font-mono">OrderService.save()</div>
      <div class="h-8 border-l-4 border-amber-300 bg-amber-50/50 px-2 flex items-center text-xs font-mono">OrderDao.insert()</div>
      <div class="h-8 border-l-4 border-red-500 bg-red-50 px-2 flex items-center text-xs font-mono">Raw SQL Query</div>
    </div>
    <span class="text-xs text-amber-700">5 layers of identical parameter forwarding</span>
  </div>

  <!-- AFTER: 1 Deep Solid Layer -->
  <div class="border border-slate-200 rounded-lg p-4 bg-white h-80 flex flex-col justify-between">
    <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">After: Consolidated Band</span>
    <div class="my-auto">
      <div class="h-44 border-l-4 border-emerald-600 bg-slate-900 text-white p-3 rounded-r flex flex-col justify-between">
        <span class="text-xs font-bold font-mono text-emerald-400">OrderIntake.submitOrder()</span>
        <p class="text-xs text-slate-300">Absorbs validation, transaction boundaries, and line item persistence into a single coherent unit.</p>
        <span class="text-[10px] text-slate-400 font-mono">Eliminates 3 intermediate delegating layers</span>
      </div>
    </div>
    <span class="text-xs text-emerald-700">Direct leverage with zero boilerplate relay</span>
  </div>
</div>
```

---

## Pattern 4: Mass diagram (interface against hidden behaviour)

**When to Use:** Visualizing depth as leverage: a shallow module asks callers to learn nearly everything it does, whereas a deep module hides a lot of behaviour behind a small interface. Label the rectangles with what callers must know and what stays hidden, never with line counts.

```html
<div class="grid grid-cols-2 gap-4 my-4">
  <!-- BEFORE: Wide Interface, Shallow Implementation -->
  <div class="border border-slate-200 rounded-lg p-4 bg-white h-80 flex flex-col justify-between">
    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Before: Shallow Module Mass</span>
    <div class="my-auto flex flex-col items-center">
      <!-- Interface Rect: what callers must know (wide and tall) -->
      <div class="w-48 h-16 border-2 border-amber-500 bg-amber-100 flex items-center justify-center text-xs font-mono font-bold text-amber-900 text-center px-2">
        Callers learn: 14 methods + call order + tx handle
      </div>
      <!-- Implementation Rect: what stays hidden (thin) -->
      <div class="w-48 h-12 border-2 border-t-0 border-slate-400 bg-slate-200 flex items-center justify-center text-xs font-mono text-slate-700">
        Hidden: field mapping only
      </div>
    </div>
    <span class="text-xs text-amber-800 text-center">Callers know nearly everything it does</span>
  </div>

  <!-- AFTER: Tiny Interface, Deep Implementation -->
  <div class="border border-slate-200 rounded-lg p-4 bg-white h-80 flex flex-col justify-between">
    <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">After: Deep Module Mass</span>
    <div class="my-auto flex flex-col items-center">
      <!-- Interface Rect: what callers must know (narrow and short) -->
      <div class="w-28 h-8 border-2 border-emerald-600 bg-emerald-100 flex items-center justify-center text-xs font-mono font-bold text-emerald-900">
        submit(order)
      </div>
      <!-- Implementation Rect: what stays hidden (deep and solid) -->
      <div class="w-48 h-32 border-2 border-t-0 border-slate-900 bg-slate-900 flex items-center justify-center text-xs font-mono text-slate-200 text-center px-2">
        Hidden: validation, tax, transaction, confirmation email
      </div>
    </div>
    <span class="text-xs text-emerald-700 text-center">Leverage: one call, every rule behind it</span>
  </div>
</div>
```

---

## Pattern 5: Call-graph collapse

**When to Use:** Showing a deeply nested call tree collapsed into a single boundary module where internal invocations become invisible private methods.

```html
<div class="grid grid-cols-2 gap-4 my-4">
  <!-- BEFORE: Exposed Internal Call Tree -->
  <div class="border border-slate-200 rounded-lg p-4 bg-white h-80 flex flex-col justify-between">
    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Before: Nested Caller Exposure</span>
    <div class="my-auto font-mono text-xs space-y-1 pl-4 border-l-2 border-red-400">
      <div class="text-slate-900 font-bold">Caller</div>
      <div class="pl-4 text-red-600">↳ step1_validate()</div>
      <div class="pl-8 text-red-600">↳ step2_lockRows()</div>
      <div class="pl-12 text-red-600">↳ step3_calculateTax()</div>
      <div class="pl-16 text-red-600">↳ step4_insertAndCommit()</div>
    </div>
    <span class="text-xs text-red-600">Caller is coupled to all 4 internal steps</span>
  </div>

  <!-- AFTER: Collapsed Behind Single Seam -->
  <div class="border border-slate-200 rounded-lg p-4 bg-white h-80 flex flex-col justify-between">
    <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">After: Collapsed Single Seam</span>
    <div class="my-auto font-mono text-xs pl-4 border-l-2 border-emerald-500">
      <div class="text-slate-900 font-bold">Caller</div>
      <div class="pl-4 text-emerald-600 font-bold">↳ execute()</div>
      <div class="pl-8 text-slate-400 italic text-[11px]">(all 4 steps executed internally)</div>
    </div>
    <span class="text-xs text-emerald-700">Internal sequencing details completely encapsulated</span>
  </div>
</div>
```
