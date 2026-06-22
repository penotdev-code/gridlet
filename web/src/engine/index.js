// Thin wrapper around the wasm-pack output. Initializes the WebAssembly module
// once and exposes a typed-ish `generateGrid` helper to the rest of the app.
import init, { generate_grid } from './pkg/gridlet_engine.js'
import wasmUrl from './pkg/gridlet_engine_bg.wasm?url'

let ready = null

/** Ensure the WASM module is initialized (idempotent). */
export function initEngine() {
  if (!ready) {
    ready = init({ module_or_path: wasmUrl })
  }
  return ready
}

/**
 * Generate crossword grids.
 * @param {{ words: string[],
 *           directions: 'horizontal'|'vertical'|'both',
 *           gap: number }} input
 * @returns {{ grids: any[], count: number, pivots_tested: number, truncated: boolean }}
 */
export async function generateGrid(input) {
  await initEngine()
  return generate_grid(input)
}
