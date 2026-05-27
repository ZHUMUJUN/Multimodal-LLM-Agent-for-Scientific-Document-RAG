# Benchmark Report

| Mode | Cases | Avg Latency (ms) | P95 Latency (ms) | Avg Answer Length | Ragas |
| --- | ---: | ---: | ---: | ---: | --- |
| baseline_hybrid | 6 | 5376.81 | 11523.73 | 113.17 | Ragas evaluation failed: All metrics must be initialised metric objects, e.g: metrics=[BleuScore(), AspectCritic()] |

## Per-case Details

### baseline_hybrid

| Case ID | Collection | Question | Latency (ms) | Sources |
| --- | --- | --- | ---: | --- |
| answer-001 | public_light_pollution_corpus | 根据语料，哪篇文档把 artificial light at night 描述为 global disruptor，并且它强调的对象是什么？ | 11523.73 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 09_world_atlas_artificial_night_sky_brightness_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
| answer-002 | public_light_pollution_corpus | 世界人工夜空亮度图谱那篇文档主要讨论什么现象？ | 4254.86 | 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 06_cambridge_turtle_conservation_light_glow.pdf, 06_cambridge_turtle_conservation_light_glow.pdf |
| answer-003 | public_light_pollution_corpus | 自然夜空亮度地图那篇文档依赖哪些核心星表或星光数据来源？ | 4144.41 | 11_anthropogenic_photons_light_pollution_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf |
| answer-004 | public_light_pollution_corpus | 关于 space objects 的文档认为哪类因素正在成为人工夜空变亮的来源？ | 3843.03 | 12_space_objects_artificial_night_sky_brightness_arxiv.pdf, 12_space_objects_artificial_night_sky_brightness_arxiv.pdf, 12_space_objects_artificial_night_sky_brightness_arxiv.pdf, 12_space_objects_artificial_night_sky_brightness_arxiv.pdf |
| answer-005 | public_light_pollution_corpus | Paranal 夜空观测那篇文档研究了多长时间、在哪个地点进行监测？ | 3891.35 | 13_dancing_sky_paranal_observations_arxiv.pdf, 13_dancing_sky_paranal_observations_arxiv.pdf, 13_dancing_sky_paranal_observations_arxiv.pdf, 13_dancing_sky_paranal_observations_arxiv.pdf |
| answer-006 | public_light_pollution_corpus | 生物多样性政策那篇文档把 artificial light at night 放在什么政策语境下讨论？ | 4603.45 | 11_anthropogenic_photons_light_pollution_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
