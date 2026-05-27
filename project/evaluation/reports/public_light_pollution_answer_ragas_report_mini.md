# Benchmark Report

| Mode | Cases | Avg Latency (ms) | P95 Latency (ms) | Avg Answer Length | Ragas |
| --- | ---: | ---: | ---: | ---: | --- |
| baseline_hybrid | 3 | 4422.07 | 4902.32 | 123.33 | answer_relevancy=0.2970, faithfulness=0.8056 |

## Per-case Details

### baseline_hybrid

| Case ID | Collection | Question | Latency (ms) | Sources |
| --- | --- | --- | ---: | --- |
| answer-mini-001 | public_light_pollution_corpus | 哪篇文档把 artificial light at night 描述为 global disruptor，它强调的环境对象是什么？ | 4216.48 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 09_world_atlas_artificial_night_sky_brightness_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
| answer-mini-002 | public_light_pollution_corpus | 自然夜空亮度地图那篇文档依赖哪些核心数据来源？ | 4147.41 | 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf |
| answer-mini-003 | public_light_pollution_corpus | 关于 space objects 的文档认为什么因素正在增加人工夜空亮度？ | 4902.32 | 12_space_objects_artificial_night_sky_brightness_arxiv.pdf, 12_space_objects_artificial_night_sky_brightness_arxiv.pdf, 12_space_objects_artificial_night_sky_brightness_arxiv.pdf, 12_space_objects_artificial_night_sky_brightness_arxiv.pdf |
