Title: Silverpoint, article 29: how silverpoint was built
Date: 2026-11-11 23:30
Category: Tutorial Silverpoint
Tags: silverpoint, react, vue, angular, reflex, IA, Visualización
lang: en
translation: true
Slug: silverpoint_serie_29
Authors: Ernesto Crespo
Summary: The last article of the series tells how silverpoint was made, from what its repository keeps: the specification with EARS requirements, changes as deltas, the architecture decisions, the CI gates, nine releases in seven weeks, the part AI assistants played and what was hard.

The previous 28 articles explained how to use [silverpoint](https://github.com/ecrespo/silverpoint). This one, the last of the series, tells how it was made. There are no recollections in it: every fact comes from the repository, its specifications, its git history or its CI. The numbers are from 1 November 2026, the day of release 0.9.2.

## The numbers

| What | How much |
|---|---|
| From the first commit to 0.9.2 | From 12 September to 1 November 2026 |
| Commits up to 1 November | 250 |
| Versions published on npm | 10, from 0.1.0 to 0.9.2 |
| Packages, all on the same version | 9 |
| Requirements in the PRD | 369: 343 MUST, 23 SHOULD, 3 COULD |
| Technical design decisions | 60, from DD-001 to DD-060 |
| Diagnostic codes | 29, from `SP001` to `SP029` |
| Test files | 237 |
| Files under `fixtures/` | 8,708 |
| Lines of the core, `@silverpoint/core` | About 20,800 |
| Lines of each adapter | 3,907 in React, 5,065 in Vue, 5,894 in Angular |

The lines count the source files without the tests, comments included. The gap between the core and the adapters is no accident: it is the rule that weighs most in the project, and it is further down.

## Specification first

The repository starts with `specs/`, not with the code. The [context file for agents](https://github.com/ecrespo/silverpoint/blob/main/CLAUDE.md) says so in its first line: before proposing or writing code, read the constitution.

The methodology is what the repository itself calls *Spec-Driven Design*: the specification is the standing truth, and the code implements it. There are seven documents:

| Document | What it settles |
|---|---|
| `constitution.md` | Nine articles that bind everything else |
| `prd.md` | What the library does, as requirements with a `REQ-NNN` identifier |
| `api-spec.md` | The public contract: packages, props, events, diagnostics |
| `technical-design.md` | How it is built: the 60 `DD-NNN` decisions |
| `data-model.md` | The shape of each chart's data and its invariants |
| `implementation-plan.md` | The phases, from 0 to 10 |
| `tasks.md` | The tasks, each with the requirement it fulfils |

The [constitution](https://github.com/ecrespo/silverpoint/blob/main/specs/constitution.md) was ratified on 12 September, the day of the first commit. Its nine articles are the ideas this series kept showing: the geometry of the data is exact (1), there is a single geometry engine (2), the four adapters draw the same thing (3), the render is deterministic (4), there is a `precision` mode and an accessible alternative (5), tone is made with hatch density (6), grounds are data (7), no CSS framework is imposed (8) and the specification is the source (9).

### The requirements in EARS

Every requirement in the [PRD](https://github.com/ecrespo/silverpoint/blob/main/specs/prd.md) is written in EARS (*Easy Approach to Requirements Syntax*): one template per kind of requirement. Of the 309 that are not rows of the chart catalog, 189 are ubiquitous (always in force), 48 unwanted-behaviour, 45 event-driven, 23 optional and 4 state-driven.

Article 28 showed an `SP002` warning labelled `REQ-008`. This is the requirement, of the unwanted-behaviour kind:

> IF a datum contains `null`, `undefined` or `NaN`, THEN THE SYSTEM SHALL omit that point from the stroke, honour the declared `connectNulls` policy and warn only in development builds.

And this one, ubiquitous, is `REQ-124`, the one that keeps hatching from being the only way to read a datum:

> No chart SHALL encode information solely by hatch style.

Phases 1 to 4 each closed with a chart-by-chart review of `REQ-124`, kept in `changes/`. The Phase 2 one lists every visual channel of the fourteen charts and the datum it carries, and every finding has a test that draws the chart in `precision`, with no hatching, and reads the datum from another channel.

### Analyze: reviewing the specification before the code

`specs/analyze.md` is a read-only cross-check of the seven documents. Its fourth run, on 13 September, counted 105 requirements, no identifier cited without a definition and no task without a requirement. And it writes the rule down: “Analyze presents findings; approval and correction are human decisions.”

That run also records a change of scope before any code was written. The third run had been triggered by a misstated question: the framework to add was Vue, not Vite. The specification absorbed both changes in a row, Vite as a validated integration and Vue as a third framework.

## Changes: deltas and features

Once approved, the specification is not edited by hand. A change goes into `changes/` and is folded into `specs/` when it is approved. There are two sizes:

* **Deltas**, 15, for changes to something already specified. For instance, `delta-007` widened `SP002` to any value a chart cannot draw as given, and `delta-015` changed how the agent catalog pins the Reflex version.
* **Features**, 6, for new work: the dashboard, the UI components, the second chart catalog, the composed components, agent access and decks.

Every feature goes through approval gates. The decks one, [`feature-006-deck`](https://github.com/ecrespo/silverpoint/tree/main/changes/feature-006-deck), has this sequence:

| Gate | Document | What it decides |
|---|---|---|
| 0 | `research.md` | What exists to build on; Marpit measured; risks |
| 1 | `prd-delta.md` | The what: requirements `REQ-570` to `REQ-628` |
| 2 | `api-delta.md` | The contract: `@silverpoint/marp`, `SpDeck` in the three adapters, directives, fences |
| PoC | `poc.md` | How to scale the slides in Chromium, Firefox and WebKit |
| 3 | `technical-design-delta.md` and `data-model-delta.md` | The how: `DD-051` to `DD-060` |
| 4 | `plan-and-tasks.md` | Tasks `T-252` to `T-289` |

All of them were approved on 31 October, the same day Phase 10 was implemented and folded into `specs/`. That day has 51 commits. 0.9.0 shipped the next day.

## The architecture decisions

Four decisions explain almost everything the series showed.

**An engine without a DOM.** All the geometry is computed in `@silverpoint/core`, which knows neither the DOM nor any framework. An adapter translates what the core gives into its framework's nodes and nothing more: it computes no scales, axes, arcs or paths. CI fails if an adapter imports `d3-*` or `roughjs`. That is why the core has about 20,800 lines and each adapter between 3,900 and 5,900. Article 2 of the constitution gives the reason: two implementations of the same drawing always end up diverging.

**Grounds are data.** A ground is a set of tokens: substrate, inks, inking parameters, typography and tonal mechanism. Adding one touches the code of no chart. `cyanotype`, the second, arrived in 0.2.0 with a tonal mechanism of its own: line weight instead of hatching.

**The adapters are compared with a canonical render.** Each adapter is compared with the canonical serialisation stored with each test case, not with the other adapters. Adding a framework costs one comparison, not one per pair.

**Determinism.** There is no `Math.random()` and no `Date.now()` on the render path. The hand-inked stroke comes from a public seed, derived from the `id`. Without that there would be no visual comparison at all, and no server render matching the browser's.

## The CI gates

Every push to `develop` and every PR goes through the [CI workflow](https://github.com/ecrespo/silverpoint/blob/main/.github/workflows/ci.yml). The release runs all of it again before uploading anything to npm. The main gates:

| Gate | What it checks | Requirements |
|---|---|---|
| Contrast | Every ink of every ground against every substrate | `REQ-126`, `REQ-127` |
| SVG string | Every adapter against the canonical render of every case, with zero tolerance | `REQ-180` |
| Pixels | Three image comparisons, with fixed thresholds, in a browser pinned by digest | `REQ-181` |
| Weight | Every package within its size budget | `REQ-164` |
| Agent catalog | It regenerates with no diff and matches what the adapters export | `REQ-535`, `REQ-536` |
| Generated code | The reference files of `generate_code` compile in the example apps | `REQ-557` |
| Traceability | Every MUST requirement has at least one test that cites it | `REQ-183`, `REQ-184` |

The pixel gate has three thresholds, written in the constitution: against the canonical render of the same commit, against the stored golden image, and a ceiling for any single pixel. The comparisons only hold with a pinned browser, scale 1, animations off and the fonts loaded.

The [traceability report](https://github.com/ecrespo/silverpoint/blob/main/reports/traceability.md) is generated from 237 test files: 342 of the 343 MUST have a test, and the missing one, `REQ-564`, is deferred to another repository. None blocks.

Path weight has its own [report](https://github.com/ecrespo/silverpoint/blob/main/reports/path-weight.md): a budget of 40,000 bytes of path data per chart.

## The release history

![Commits per silverpoint release: 82 up to 0.1.1, 39 in 0.2.0, 15 in 0.3.0, 12 in 0.6.0, 25 in 0.7.0, 16 in 0.8.0, 53 in 0.9.0, 4 in 0.9.1 and 3 in 0.9.2](./images/silverpoint-serie-29.png)

The chart was drawn by the `render_chart` tool from article 28, with the commits between each tag and the previous one. The call:

```json
{"chart":"bar-chart","props":{"xKey":"release","valueKey":"commits","title":"Commits per release","footerLeft":"2026-09-12 to 2026-11-01","footerRight":"249 commits"},"data":[{"release":"0.1.1","commits":82},{"release":"0.2.0","commits":39},{"release":"0.3.0","commits":15},{"release":"0.6.0","commits":12},{"release":"0.7.0","commits":25},{"release":"0.8.0","commits":16},{"release":"0.9.0","commits":53},{"release":"0.9.1","commits":4},{"release":"0.9.2","commits":3}],"width":720,"height":280,"id":"commits","embedFonts":true}
```

The releases, with their npm dates:

| Version | Date | What it brought |
|---|---|---|
| 0.1.0 | 25 September | The first catalog, 33 charts, in React, Vue and Angular |
| 0.1.1 | 25 September | A README per package; from here on, published from CI only |
| 0.2.0 | 26 September | The `Dashboard`, the `cyanotype` ground and `@silverpoint/tailwind` |
| 0.3.0 | 1 October | The 17 UI components |
| 0.6.0 | 10 October | The second catalog: 27 more charts |
| 0.7.0 | 20 October | Palettes, composed components, overlays and the timeline |
| 0.8.0 | 21 October | Agent access: `@silverpoint/mcp`, the catalog and the skill |
| 0.9.0 | 1 November | Decks: `@silverpoint/marp` and `SpDeck` |
| 0.9.1 | 1 November | React `SpDeck` under `<StrictMode>` (issues #7 and #8) |
| 0.9.2 | 1 November | The Reflex catalog with `sp_deck` (issue #10) |

There was no 0.4.0 and no 0.5.0. The second catalog was built in three waves, and the decision was to publish them together as 0.6.0. 1.0.0 is parked on purpose: it would put the API specification in force as a stable contract. Its changeset waits in `changes/release-1.0.0-changeset.md`.

Since 0.1.1, releases are published by CI through *npm Trusted Publishing* with provenance, without a token. The nine packages share one version.

## The Reflex wrapper and the documentation

There are two more repositories.

[`reflex-silverpoint-react`](https://github.com/ecrespo/reflex-silverpoint-react) started on 25 September and has ten releases, from 0.1.0 to 0.9.1. It wraps the components of `@silverpoint/react` as Python builders. It has a curious history: the palettes, the composed components and the timeline were drawn there first, in its 0.7, outside the parity contract. silverpoint's constitution records it as the source of the 0.7.0 inventory, where they were rewritten on the core. Since the wrapper's 0.7.1, they are the npm components behind the builders.

The [documentation site](https://silverpointweb.vercel.app/) is built in Reflex with that same wrapper ([`silverpoint_web`](https://github.com/ecrespo/silverpoint_web)). It is frontend only: it is exported statically to Vercel, with no backend, and its controls are silverpoint components. Its `vercel.json` also publishes the MCP server from article 28: it rewrites `/mcp` to the Vercel project that deploys it from `apps/mcp-vercel`.

## The AI assistants

The repository does not hide it. 244 of silverpoint's 250 commits carry Claude's `Co-Authored-By` line. In the wrapper it is 27 of 59, and in the documentation site, 13 of 49.

The specification explains why it is built this way. Article 9 of the constitution, the one that requires every task and every test to cite a requirement, gives this reason: “the project is implemented in large part with agents; without traceability there is no way to answer why a line of code exists.”

What the files show is a division of roles:

* **Decisions belong to the person.** The context file marks each one with its date: “user decision, 2026-10-10” to publish the three waves as 0.6.0, “user decision 2026-11-01” to compare versions by release line. Analyze presents findings; approving them is a human decision. Every feature gate has its approval date.
* **The agent works in batches.** `tasks.md` asks for it: the first batch is T-001 to T-004; then review, adjust, and only then scale. “Do not launch all 29 unsupervised.”
* **The context lives in the repository.** The plan says it is a one-person project with no ceremonies. `tasks.md` is marked with a date as each task closes, so that any session, human or agent, can resume with no prior context. The context file has a section titled “Settled decisions — do not rediscover them”.
* **A deviation stops the work.** If the code cannot meet the specification, the specification is updated or a delta is opened, and only then does the work go on.

The CI gates are the other half. An agent can write code that looks right; the SVG string, the pixels, the contrast and the traceability say whether it is.

## What was hard

The repository also keeps what went wrong or cost more than expected.

* **Hatching is heavy.** Hatching each shape separately came to 913 KB for a 12-card dashboard. The weight report shows it per chart: with per-shape hatching, the large heatmap takes 61,348 bytes, over the 40,000 budget. The decision was one hatch pattern per tonal level, `hatchFill: 'tile'`, which brings that heatmap down to 3,909 bytes.
* **A field that already existed.** `cyanotype` needed a line weight per tone. `Stroke.weight` existed, but it was the `BulletChart` target marker's, and reusing it changed 48 canonical renders. A separate field was created.
* **Publishing is code too.** The trusted publisher of `@silverpoint/mcp` on npm expired before 0.9.0, and npm answered `E404`. That package's 0.8.0 had been published by hand, without provenance, because it had no publisher yet.
* **React's strict mode.** `SpDeck` was inert under `<StrictMode>`: the double mount destroyed its controller. It was fixed in 0.9.1, the same day as 0.9.0.
* **What is still open.** The manual NVDA and VoiceOver pass over the components needs Windows or macOS and is pending. The nightly workflow is disabled. And writing this series turned up five issues, #12 to #16, such as `SpTable` cells aligned to the right or the exported SVG without its stylesheet.

## End of the series

This is where the series ends. It started with a Renaissance drawing technique and ended with a server that draws charts for an assistant, by way of one operations panel in four frameworks.

If you came straight here, go back to [article 0](/blog/silverpoint_serie_0). Its “Reading paths” section has a short route for each framework, one for evaluating the library and one for working with AI. If you already followed it, the [documentation](https://silverpointweb.vercel.app/) and the [gallery](https://silverpointweb.vercel.app/gallery) keep up with every release.
