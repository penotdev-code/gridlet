# Gridlet

Générateur de grilles de mots croisés (style Scrabble) où les mots se croisent
sur leurs lettres communes.

- **Front** : Svelte 5 + Vite — saisie d'une liste de mots, sens autorisé,
  écart minimum, tri esthétique des résultats, pagination et statistiques.
- **Moteur** : Rust compilé en **WebAssembly** — énumère les grilles possibles
  et leurs croisements, exécuté directement dans le navigateur (aucun serveur).

```
gridlet/
├── engine/              # Crate Rust → WASM (l'algorithme)
│   └── src/lib.rs       # Génération de grille + tests natifs
└── web/                 # Application Svelte
    └── src/
        ├── engine/      # Wrapper JS + sortie wasm-pack (pkg/, générée)
        ├── lib/         # Composants (WordRow, GridView)
        └── App.svelte   # Interface principale
```

## Prérequis

- [Rust](https://rustup.rs) avec la cible `wasm32-unknown-unknown`
  (`rustup target add wasm32-unknown-unknown`)
- [`wasm-pack`](https://rustwasm.github.io/wasm-pack/) (`cargo install wasm-pack`)
- Node.js 18+

## Démarrer

```bash
cd web
npm install
npm run dev      # compile le moteur Rust→WASM puis lance Vite
```

Ouvrir http://localhost:5173.

Les scripts `predev` / `prebuild` reconstruisent automatiquement le moteur
(`npm run build:engine`) avant de lancer Vite.

## Build de production

```bash
cd web
npm run build    # → web/dist/
npm run preview
```

## Tester le moteur (Rust)

```bash
cd engine
cargo test
```

## Comment fonctionne l'algorithme

L'entrée : une liste de mots, un sens autorisé global (`horizontal`, `vertical`
ou `both`) et un écart minimum entre mots parallèles (0–5).

Le moteur **énumère** des grilles (pas une seule) :

1. Les mots sont normalisés (majuscules, accents repliés) pour comparer les
   lettres lors des croisements.
2. **Chaque mot est testé comme pivot de départ**, placé horizontalement.
3. Un backtracking ajoute les autres mots en générant **tous les croisements
   possibles** via les lettres communes. À chaque étape on choisit le mot
   connectable le plus contraint (MRV) et on explore tous ses placements.
4. Chaque placement est validé : une case = une seule lettre (pas de conflit),
   croisements perpendiculaires uniquement, pas de mots « collés » bout à bout,
   et respect de l'écart minimum entre mots parallèles.
5. Les grilles complètes sont **dédupliquées** (signature normalisée). Si aucune
   grille ne place tous les mots, les meilleures grilles partielles sont gardées.

### Tri esthétique (côté JS)

Le moteur renvoie la liste brute ; le front calcule les métriques et trie selon
le critère choisi :

| Critère | Optimise |
| --- | --- |
| **Esthétique** (défaut) | score combiné (croisements, densité, équilibre, centrage, compacité) |
| Compacité | moins d'espace vide |
| Équilibre | dimensions proches du carré |
| Centrage | lettres bien centrées |
| Croisements | maximum de points de croisement |
| Densité | remplissage maximal |

### Limites & pistes

- La recherche est bornée (≤ 400 grilles, budget de nœuds) pour rester instantanée.
- Pistes : export PNG / impression, sélection/épinglage de grilles favorites,
  contraintes d'orientation par mot.
