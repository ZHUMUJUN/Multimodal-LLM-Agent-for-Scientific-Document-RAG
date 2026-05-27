# Benchmark Report

| Mode | Cases | Avg Latency (ms) | Source Hit Rate | Avg Keyword Hit Rate | Avg Answer Length | Routing | Ragas |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| baseline_hybrid | 6 | 783.57 | 1 | 0.5 | 186 | route_hit_rate=0.6667; baseline_hybrid=6 | answer_relevancy=0.2864, faithfulness=0.3667 |
| lightrag | 6 | 3837.93 | 1 | 0.6667 | 832 | route_hit_rate=0.3333; lightrag=6 | answer_relevancy=0.2823, faithfulness=1.0000 |
| router | 6 | 575.36 | 1 | 0.6111 | 753.83 | route_hit_rate=1.0000; baseline_hybrid=4, lightrag=2 | answer_relevancy=0.1390, faithfulness=0.7500 |

## Question-Type Summary

| Mode | Question Type | Cases | Avg Latency (ms) | Source Hit Rate | Avg Keyword Hit Rate |
| --- | --- | ---: | ---: | ---: | ---: |
| baseline_hybrid | single_hop | 4 | 774.21 | 1 | 0.6667 |
| baseline_hybrid | multi_hop_relation | 2 | 802.28 | 1 | 0.1666 |
| lightrag | single_hop | 4 | 3268.32 | 1 | 0.6667 |
| lightrag | multi_hop_relation | 2 | 4977.14 | 1 | 0.6666 |
| router | single_hop | 4 | 660.28 | 1 | 0.5834 |
| router | multi_hop_relation | 2 | 405.5 | 1 | 0.6666 |

## Per-case Details

### baseline_hybrid

| Case ID | Type | Question | Resolved Mode | Route Hit | Source Hit | Latency (ms) | Sources |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| router-001 | single_hop | 哪篇文档把 artificial light at night 描述为 global disruptor，并强调 nighttime environment？ | baseline_hybrid | True | True | 628.23 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
| router-003 | single_hop | 自然夜空亮度地图那篇文档依赖哪些核心星表数据？ | baseline_hybrid | True | True | 1280.63 | 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf |
| router-004 | single_hop | 哪篇文档把光污染严格表述为 terrestrial atmosphere 中 anthropogenic photons 的浓度？ | baseline_hybrid | True | True | 588.82 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
| router-008 | single_hop | 哪篇文档强调 light pollution 是一个 environmental pollutant 和 relevant stressor？ | baseline_hybrid | True | True | 599.16 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf |
| router-018 | multi_hop_relation | 比较 review 文档和 anthropogenic photons 文档：它们分别如何把 artificial light at night 解释成污染物？ | baseline_hybrid | False | True | 818.67 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
| router-extra-001 | multi_hop_relation | 比较 natural night sky brightness 地图文档和 anthropogenic photons 文档：一个给 baseline，一个给物理量定义，它们分别回答什么问题？ | baseline_hybrid | False | True | 785.9 | 11_anthropogenic_photons_light_pollution_arxiv.pdf, 12_space_objects_artificial_night_sky_brightness_arxiv.pdf, 12_space_objects_artificial_night_sky_brightness_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf |

### lightrag

| Case ID | Type | Question | Resolved Mode | Route Hit | Source Hit | Latency (ms) | Sources |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| router-001 | single_hop | 哪篇文档把 artificial light at night 描述为 global disruptor，并强调 nighttime environment？ | lightrag | False | True | 2986.59 | 08_artificial_light_at_night_global_disruptor_arxiv.md, 11_anthropogenic_photons_light_pollution_arxiv.md |
| router-003 | single_hop | 自然夜空亮度地图那篇文档依赖哪些核心星表数据？ | lightrag | False | True | 3683.04 | 10_natural_night_sky_brightness_gaia_arxiv.md, 12_space_objects_artificial_night_sky_brightness_arxiv.md, 11_anthropogenic_photons_light_pollution_arxiv.md, 08_artificial_light_at_night_global_disruptor_arxiv.md |
| router-004 | single_hop | 哪篇文档把光污染严格表述为 terrestrial atmosphere 中 anthropogenic photons 的浓度？ | lightrag | False | True | 3457.46 | 11_anthropogenic_photons_light_pollution_arxiv.md, 08_artificial_light_at_night_global_disruptor_arxiv.md, 12_space_objects_artificial_night_sky_brightness_arxiv.md |
| router-008 | single_hop | 哪篇文档强调 light pollution 是一个 environmental pollutant 和 relevant stressor？ | lightrag | False | True | 2946.2 | 11_anthropogenic_photons_light_pollution_arxiv.md, 08_artificial_light_at_night_global_disruptor_arxiv.md |
| router-018 | multi_hop_relation | 比较 review 文档和 anthropogenic photons 文档：它们分别如何把 artificial light at night 解释成污染物？ | lightrag | True | True | 5923.7 | 08_artificial_light_at_night_global_disruptor_arxiv.md, 11_anthropogenic_photons_light_pollution_arxiv.md |
| router-extra-001 | multi_hop_relation | 比较 natural night sky brightness 地图文档和 anthropogenic photons 文档：一个给 baseline，一个给物理量定义，它们分别回答什么问题？ | lightrag | True | True | 4030.57 | 10_natural_night_sky_brightness_gaia_arxiv.md, 11_anthropogenic_photons_light_pollution_arxiv.md, 08_artificial_light_at_night_global_disruptor_arxiv.md |

### router

| Case ID | Type | Question | Resolved Mode | Route Hit | Source Hit | Latency (ms) | Sources |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| router-001 | single_hop | 哪篇文档把 artificial light at night 描述为 global disruptor，并强调 nighttime environment？ | baseline_hybrid | True | True | 544.98 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
| router-003 | single_hop | 自然夜空亮度地图那篇文档依赖哪些核心星表数据？ | baseline_hybrid | True | True | 952.03 | 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf, 10_natural_night_sky_brightness_gaia_arxiv.pdf |
| router-004 | single_hop | 哪篇文档把光污染严格表述为 terrestrial atmosphere 中 anthropogenic photons 的浓度？ | baseline_hybrid | True | True | 556.82 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf |
| router-008 | single_hop | 哪篇文档强调 light pollution 是一个 environmental pollutant 和 relevant stressor？ | baseline_hybrid | True | True | 587.31 | 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 08_artificial_light_at_night_global_disruptor_arxiv.pdf, 11_anthropogenic_photons_light_pollution_arxiv.pdf |
| router-018 | multi_hop_relation | 比较 review 文档和 anthropogenic photons 文档：它们分别如何把 artificial light at night 解释成污染物？ | lightrag | True | True | 439.35 | 08_artificial_light_at_night_global_disruptor_arxiv.md, 11_anthropogenic_photons_light_pollution_arxiv.md |
| router-extra-001 | multi_hop_relation | 比较 natural night sky brightness 地图文档和 anthropogenic photons 文档：一个给 baseline，一个给物理量定义，它们分别回答什么问题？ | lightrag | True | True | 371.64 | 10_natural_night_sky_brightness_gaia_arxiv.md, 11_anthropogenic_photons_light_pollution_arxiv.md, 08_artificial_light_at_night_global_disruptor_arxiv.md |
