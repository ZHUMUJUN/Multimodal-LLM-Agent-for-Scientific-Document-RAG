# Benchmark Report

| Mode | Cases | Avg Latency (ms) | P95 Latency (ms) | Avg Answer Length | Ragas |
| --- | ---: | ---: | ---: | ---: | --- |
| baseline_hybrid | 3 | 4712.55 | 6204.3 | 221.67 | answer_relevancy=0.5402, faithfulness=0.6667 |
| lightrag | 3 | 32845.45 | 51775.44 | 340.67 | answer_relevancy=0.4641, faithfulness=0.5556 |

## Per-case Details

### baseline_hybrid

| Case ID | Collection | Question | Latency (ms) | Sources |
| --- | --- | --- | ---: | --- |
| mini-lightrag-001 | public_light_pollution_mini | 哪篇文档把 artificial light at night 描述为 global disruptor of the nighttime environment？ | 3854.23 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
| mini-lightrag-002 | public_light_pollution_mini | 哪篇文档讨论了 natural night sky brightness including Gaia and Hipparcos integrated starlight？ | 6204.3 | 10_natural_night_sky_brightness_gaia_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf |
| mini-lightrag-003 | public_light_pollution_mini | 哪篇文档把光污染表述为大气中 anthropogenic photons 的浓度？ | 4079.12 | 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |

### lightrag

| Case ID | Collection | Question | Latency (ms) | Sources |
| --- | --- | --- | ---: | --- |
| mini-lightrag-001 | public_light_pollution_mini | 哪篇文档把 artificial light at night 描述为 global disruptor of the nighttime environment？ | 51775.44 | 08_artificial_light_at_night_global_disruptor_arxiv.md, 11_anthropogenic_photons_light_pollution_arxiv.md |
| mini-lightrag-002 | public_light_pollution_mini | 哪篇文档讨论了 natural night sky brightness including Gaia and Hipparcos integrated starlight？ | 22009.73 | 10_natural_night_sky_brightness_gaia_arxiv.md, 08_artificial_light_at_night_global_disruptor_arxiv.md, 11_anthropogenic_photons_light_pollution_arxiv.md |
| mini-lightrag-003 | public_light_pollution_mini | 哪篇文档把光污染表述为大气中 anthropogenic photons 的浓度？ | 24751.19 | 11_anthropogenic_photons_light_pollution_arxiv.md, 08_artificial_light_at_night_global_disruptor_arxiv.md |
