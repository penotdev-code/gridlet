// Per-grid metrics + aesthetic sorting, computed in JS so the combined score can
// be normalized across the whole result set.

/** Raw geometric metrics for a single grid. */
export function computeMetrics(grid) {
  const area = grid.rows * grid.cols
  const letters = grid.letters
  const empty = area - letters
  const fill = area > 0 ? letters / area : 0
  const balance =
    Math.min(grid.rows, grid.cols) / Math.max(grid.rows, grid.cols || 1)

  let sumR = 0
  let sumC = 0
  for (const c of grid.cells) {
    sumR += c.row
    sumC += c.col
  }
  const n = grid.cells.length || 1
  const centroidR = sumR / n
  const centroidC = sumC / n
  const centerDist = Math.hypot(
    centroidR - (grid.rows - 1) / 2,
    centroidC - (grid.cols - 1) / 2
  )

  return { area, letters, empty, fill, balance, centerDist, crossings: grid.crossings }
}

const normalize = (val, min, max) => (max > min ? (val - min) / (max - min) : 1)

/**
 * Attach `.m` (metrics) and `.aesthetic` (0–1 combined score) to every grid.
 * The aesthetic score blends crossings, fill, balance, centering and compactness.
 */
export function annotate(grids) {
  const annotated = grids.map((g) => ({ ...g, m: computeMetrics(g) }))
  if (annotated.length === 0) return annotated

  const ranges = (sel) => {
    const vals = annotated.map(sel)
    return [Math.min(...vals), Math.max(...vals)]
  }
  const [xMin, xMax] = ranges((g) => g.m.crossings)
  const [fMin, fMax] = ranges((g) => g.m.fill)
  const [bMin, bMax] = ranges((g) => g.m.balance)
  const [dMin, dMax] = ranges((g) => g.m.centerDist)
  const [eMin, eMax] = ranges((g) => g.m.empty)

  for (const g of annotated) {
    const crossings = normalize(g.m.crossings, xMin, xMax)
    const fill = normalize(g.m.fill, fMin, fMax)
    const balance = normalize(g.m.balance, bMin, bMax)
    const centering = 1 - normalize(g.m.centerDist, dMin, dMax)
    const compact = 1 - normalize(g.m.empty, eMin, eMax)
    g.aesthetic =
      0.3 * crossings + 0.25 * fill + 0.2 * balance + 0.15 * centering + 0.1 * compact
  }
  return annotated
}

/** Comparators for each sort criterion (best grid first). */
export const SORTERS = {
  esthetique: (a, b) => b.aesthetic - a.aesthetic,
  compacite: (a, b) => a.m.empty - b.m.empty || a.m.area - b.m.area,
  equilibre: (a, b) => b.m.balance - a.m.balance,
  centrage: (a, b) => a.m.centerDist - b.m.centerDist,
  croisements: (a, b) => b.m.crossings - a.m.crossings || a.m.empty - b.m.empty,
  densite: (a, b) => b.m.fill - a.m.fill,
}

export const SORT_OPTIONS = [
  { value: 'esthetique', label: 'Esthétique', hint: 'Score combiné optimal' },
  { value: 'compacite', label: 'Compacité', hint: "Moins d'espace vide" },
  { value: 'equilibre', label: 'Équilibre', hint: 'Proche du carré' },
  { value: 'centrage', label: 'Centrage', hint: 'Lettres bien centrées' },
  { value: 'croisements', label: 'Croisements', hint: 'Maximum de croisements' },
  { value: 'densite', label: 'Densité', hint: 'Remplissage maximal' },
]
