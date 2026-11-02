# Answer one design question: procedure detail and bounded example

Worked logic module: empty -> add item -> checkout -> paid; checkout from empty returns an observable error without mutation. Walkthrough starts reset, add, checkout, and separately demonstrates illegal empty checkout. UI switcher pseudocode: read variant from router query, render A/B/C with unchanged data, replace only query; handler ignores editing targets, computes (index+direction+count)%count, and never intercepts typing.

## Run the example

Use only a fresh disposable directory. The Python standard-library block writes local artifacts. The main checker executes this exact block and independently verifies outputs. Optional browser interaction and dependency-cruiser execution are separate, honestly unverified claims.

```python
from pathlib import Path
import json
def transition(state,action):
 if action=="reset": return {"items":0,"status":"draft"}
 if action=="add" and state["status"]=="draft": return {"items":state["items"]+1,"status":"draft"}
 if action=="checkout" and state["items"]>0: return {"items":state["items"],"status":"paid"}
 return dict(state)
initial={"items":0,"status":"draft"}
illegal=transition(initial,"checkout")
paid=transition(transition(initial,"add"),"checkout")
html="""<!doctype html><html lang="en"><meta charset="utf-8"><title>Order state prototype</title>
<style>body{font:18px system-ui;max-width:45rem;margin:2rem auto;padding:1rem}button{font:inherit;margin:.3rem;padding:.6rem}pre{white-space:pre-wrap}</style>
<h1>PROTOTYPE: can an empty order be paid?</h1><p>Explore the order model. Empty checkout should keep the draft unchanged.</p>
<pre id="state" aria-live="polite"></pre>
<button data-action="add">Add item</button><button data-action="checkout">Checkout</button><button data-action="reset">Reset</button>
<h2>Guided walkthroughs</h2><button id="happy">Reset, add, checkout</button><button id="illegal">Reset, empty checkout</button>
<script>
const initial=()=>({items:0,status:'draft'});
function reduce(s,a){if(a==='reset')return initial();if(a==='add'&&s.status==='draft')return {...s,items:s.items+1};if(a==='checkout'&&s.items>0)return {...s,status:'paid'};return {...s};}
let state=initial();const view=()=>document.getElementById('state').textContent='Items: '+state.items+'; status: '+state.status;
function act(a){state=reduce(state,a);view();}
document.querySelectorAll('[data-action]').forEach(b=>b.addEventListener('click',()=>act(b.dataset.action)));
document.getElementById('happy').onclick=()=>{act('reset');act('add');act('checkout');};
document.getElementById('illegal').onclick=()=>{act('reset');act('checkout');};view();
</script></html>"""
Path("prototype.html").write_text(html,encoding="utf-8")
result={"empty_checkout":illegal,"paid":paid,"reset":transition(paid,"reset"),"live_mutations":[]}
Path("result.json").write_text(json.dumps(result,sort_keys=True),encoding="utf-8")
```

## What the observation establishes

The TypeScript example implements the five graph rules against literal valid and invalid import fixtures, including a dependency cycle; it does not execute the actual dependency-cruiser resolver. The prototype produces an offline runnable HTML with pure reducer, state display, free-play and guided scenarios. Its Python model is exercised; browser click behavior must be checked separately before claiming live interaction success.
