# Visual Diagram Patterns for Architecture Surveys

Internal method ID: `architecture-survey`. Supporting resource for `skills/architecture-survey`.

This resource specifies the 5 canonical visual diagram patterns used in architecture survey reports. Diagrams carry the substantive weight of the report. Prose must remain minimal. If a diagram requires a paragraph of explanation to be understood, redesign the diagram.

---

## 1. Visual Standards and Aesthetics

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

## 2. Pattern 1: Mermaid Graph (Dependencies and Call Flow)

**When to Use:** When illustrating complex call flows, messy dependency webs, or multi-step round trips.

### Before: Messy dependencies and leaky seams
```html
<div class="rounded-lg border border-slate-200 bg-white p-4 h-80 flex flex-col justify-between">
  <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">Before: Fragmented Wrappers</span>
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

## 3. Pattern 2: Hand-Built Boxes and Arrows (CSS / SVG)

**When to Use:** When Mermaid auto-layout fights the desired emphasis, or when representing a thick-bordered deep module enclosing greyed-out internal functions.

```html
<div class="grid grid-cols-2 gap-4 my-4">
  <!-- BEFORE -->
  <div class="border border-slate-300 rounded-lg p-4 bg-slate-50 h-80 relative flex flex-col justify-between">
    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Before: 4 Shallow Files</span>
    <div class="space-y-2 my-auto">
      <div class="p-2 border border-dashed border-red-500 bg-red-50 rounded text-xs text-red-800">OrderValidator.ts (15 lines)</div>
      <div class="p-2 border border-dashed border-red-500 bg-red-50 rounded text-xs text-red-800">OrderPricing.ts (22 lines)</div>
      <div class="p-2 border border-dashed border-red-500 bg-red-50 rounded text-xs text-red-800">OrderDbWrapper.ts (30 lines)</div>
      <div class="p-2 border border-dashed border-red-500 bg-red-50 rounded text-xs text-red-800">OrderNotifier.ts (18 lines)</div>
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

## 4. Pattern 3: Cross-Section (Layered Shallowness)

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

## 5. Pattern 4: Mass Diagram (Interface Width vs Implementation Depth)

**When to Use:** Visualizing the core definition of depth: a shallow module has an interface nearly as large as its implementation, whereas a deep module has a tiny interface surface covering a massive implementation volume.

```html
<div class="grid grid-cols-2 gap-4 my-4">
  <!-- BEFORE: Wide Interface, Shallow Implementation -->
  <div class="border border-slate-200 rounded-lg p-4 bg-white h-80 flex flex-col justify-between">
    <span class="text-xs font-bold text-slate-500 uppercase tracking-wider">Before: Shallow Module Mass</span>
    <div class="my-auto flex flex-col items-center">
      <!-- Interface Rect: Wide and Tall -->
      <div class="w-48 h-16 border-2 border-amber-500 bg-amber-100 flex items-center justify-center text-xs font-mono font-bold text-amber-900">
        Interface: 14 Methods
      </div>
      <!-- Implementation Rect: Shallow -->
      <div class="w-48 h-12 border-2 border-t-0 border-slate-400 bg-slate-200 flex items-center justify-center text-xs font-mono text-slate-700">
        Impl: 40 Lines Logic
      </div>
    </div>
    <span class="text-xs text-amber-800 text-center">Interface is 50% of the cognitive surface area</span>
  </div>

  <!-- AFTER: Tiny Interface, Deep Implementation -->
  <div class="border border-slate-200 rounded-lg p-4 bg-white h-80 flex flex-col justify-between">
    <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">After: Deep Module Mass</span>
    <div class="my-auto flex flex-col items-center">
      <!-- Interface Rect: Narrow and Short -->
      <div class="w-28 h-8 border-2 border-emerald-600 bg-emerald-100 flex items-center justify-center text-xs font-mono font-bold text-emerald-900">
        1 Method
      </div>
      <!-- Implementation Rect: Deep and Solid -->
      <div class="w-48 h-32 border-2 border-t-0 border-slate-900 bg-slate-900 flex items-center justify-center text-xs font-mono text-slate-200 text-center px-2">
        Impl: 220 Lines Encapsulated Rules & Invariants
      </div>
    </div>
    <span class="text-xs text-emerald-700 text-center">High leverage: massive power behind tiny seam</span>
  </div>
</div>
```

---

## 6. Pattern 5: Call-Graph Collapse

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
