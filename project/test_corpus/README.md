# Public PDF Test Corpus

This folder stores public PDF documents used for retrieval and RAG evaluation.

## Verified Ingestable Documents

The following files were re-checked with PyMuPDF and confirmed to have readable pages.

1. `05_cbd_artificial_light_at_night_biodiversity.pdf`
   Source: https://www.cbd.int/doc/c/5735/c241/efeeac8d7685af2f38d75e4e/sbstta-24-inf-31-en.pdf

2. `06_cambridge_turtle_conservation_light_glow.pdf`
   Source: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/E87C8921E34AD76B787E8A2FE691D48D/S0376892914000216a.pdf/div-class-title-balancing-artificial-light-at-night-with-turtle-conservation-coastal-community-engagement-with-light-glow-reduction-div.pdf

3. `08_artificial_light_at_night_global_disruptor_arxiv.pdf`
   Source: https://arxiv.org/pdf/2311.02098.pdf

4. `09_world_atlas_artificial_night_sky_brightness_arxiv.pdf`
   Source: https://arxiv.org/pdf/1609.01041.pdf

5. `10_natural_night_sky_brightness_gaia_arxiv.pdf`
   Source: https://arxiv.org/pdf/2101.01500.pdf

6. `11_anthropogenic_photons_light_pollution_arxiv.pdf`
   Source: https://arxiv.org/pdf/2210.14131.pdf

7. `12_space_objects_artificial_night_sky_brightness_arxiv.pdf`
   Source: https://arxiv.org/pdf/2103.17125.pdf

8. `13_dancing_sky_paranal_observations_arxiv.pdf`
   Source: https://arxiv.org/pdf/0801.2270.pdf

## Notes

- `01`, `04`, and `07` are kept in the folder for reference but currently open as zero-page PDFs in PyMuPDF, so they should not be used for ingestion.
- The corpus now has enough document diversity to test retrieval ordering, source selection, and reranker behavior better than a single-PDF setup.

## Suggested Usage

- Use `05` and `06` as ecology and biodiversity documents.
- Use `08`, `09`, `10`, `11`, `12`, and `13` as astronomy, sky brightness, and artificial light references.
- Mix these with your own domain PDFs to create harder multi-document benchmark queries.

## Ingest Command

Run this from the repository root:

```bash
source .venv/bin/activate
python project/test_corpus/ingest_public_corpus.py --collection public_light_pollution_corpus --clear
```

The ingestion script first builds a `markdown_cache/` snapshot from the PDFs and then ingests those markdown files. This avoids the unstable direct PDF-to-Markdown path for several public documents.

## Retrieval Benchmark Dataset

The corresponding retrieval benchmark dataset is stored at:

`project/evaluation/datasets/public_light_pollution_retrieval_eval.jsonl`
