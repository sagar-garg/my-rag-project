# Eval set expanded to 15 questions; gating metrics shift to purity and rank

## Date
2026-07-18

## Outcome

The retrieval eval set grew from 4 saturated questions to 15 (4 originals kept
verbatim, 11 new: no chapter names, paraphrased concepts, deliberate Ch5/Ch6
vocabulary traps, 2 cross-chapter targets). The re-run stayed 15/15 hit@4 — and
that exposed the real finding: chapter-level hit@4 on a 3-file corpus is
structurally unmissable, so the metrics that gate feature work from now on are
chunk purity (55/60 = 92%) and first-hit rank (worst: 2). Artifact:
`docs/showcase/eval/2026-07-18-expanded-set.md`.

## What works

- 15-question eval set in `data/eval/chapters_4_6_starter.json`, incl.
  multi-target (cross-chapter) cases — `judge_retrieval` needed no changes.
- `scripts/run_starter_eval.py` with `--out` and new `--title` flags;
  retrieval-only (15 embedding calls, no chat API).
- Three questions now show measurable weakness for dense retrieval:
  Q3 (purity 2/4), Q8 (rank 2, purity 2/4), Q13 (purity 3/4).
- `pytest tests/test_basic_eval.py` green (6 tests, count assertion updated).

## Corpus / data / inputs used

Chapters 4–6 of Chip Huyen's *AI Engineering* (PDFs), collection
`book_chapters_4_6`, chunking 512/80, dense top-4, `text-embedding-3-small-2`.
New questions were grounded by extracting section maps and key page text from
the PDFs (pypdf), so reference answers cite actual corpus content.

## Important lessons

- **A metric that can't fail measures nothing.** With 3 source files and top-4
  retrieval, a chapter-level "any chunk counts" hit needs all 4 chunks to land
  wrong to miss. When a binary metric saturates structurally, switch to the
  finer signals already collected (purity, first-hit rank) before redesigning
  the eval.
- **Paraphrase distance is not a hardness axis for modern embeddings.** The
  question with zero lexical overlap with its target passage retrieved
  perfectly; the questions reusing vocabulary that two chapters share are the
  ones that degraded. Hard retrieval questions come from cross-document
  lexical confusion, not oblique wording.
- Chapter-level gold labels are too coarse to ever produce misses here;
  section- or chunk-level labels are the escalation path if purity/rank stop
  discriminating.

## Next step

First measured feature iteration: chunking-parameter sweep (e.g. 256/40 and
1024/160 vs current 512/80, fresh collection per config), judged on purity and
first-hit rank per question — specifically whether any config cleans up
Q3/Q8/Q13.
