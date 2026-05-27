# Router Failure Analysis

- Source report: `project/evaluation/reports/light_answer_benchmark_router_20260327_100444.json`
- Failure count captured: `2`

## router-003

- Failure Type: `answer_incomplete`
- Question Type: `single_hop`
- Expected Route: `baseline_hybrid`
- Resolved Mode: `baseline_hybrid`
- Source Hit: `True`
- Keyword Hit Rate: `0.0`
- Latency ms: `952.03`
- Question: 自然夜空亮度地图那篇文档依赖哪些核心星表数据？
- Answer: 根据提供的上下文，自然夜空亮度地图那篇文档依赖的核心星表数据包括： 1. 光子浓度分布（Photon Concentration）：具体表现为公式 (12) 中的积分项。 2. 空气传播系数（Air Propagation Coefficient）：在公式 (30) 中定义，用于描述光从天空方向到地面表面的路径衰减。  这些核心数据依赖于特定的星表和模型来计算。例如，在公式 (12) 中，积分项涉及对不同波长范围内的光子浓度进行累积；而在公式 (30) 中，则涉及到空气传播系数的计算。因此，文档需要精确的数据集来支持其数学表达式中的各种计算。

## router-extra-001

- Failure Type: `answer_incomplete`
- Question Type: `multi_hop_relation`
- Expected Route: `lightrag`
- Resolved Mode: `lightrag`
- Source Hit: `True`
- Keyword Hit Rate: `0.3333`
- Latency ms: `371.64`
- Question: 比较 natural night sky brightness 地图文档和 anthropogenic photons 文档：一个给 baseline，一个给物理量定义，它们分别回答什么问题？
- Answer: 自然夜空亮度地图（GAMBONS模型）提供了一幅以地面观测者为中心的夜空亮度分布图，它综合考虑了来自多个天体系统的光亮度贡献，包括恒星辐射、散射光以及大气发光。这个文档试图描述和量化夜间天空的本底亮度。  相反， anthropogenic photons 文档提供了对自然夜空中光源浓度的物理定义，并探讨了这些光源（如人造灯光）如何影响光污染水平。它关注的是与特定天体系统相关的物理量，通过计算空气传播路径上每单位体积中的光电流密度来确定。  两个文档回答的问题如下：  1. **GAMBONS模型**：    - GAMBONS模型试图提供一个全面的夜空亮度图，包括来自各种来源的光亮，如恒星辐射、散射光和大气发光。它的目的是描述夜间天空的本底亮度，即没有光源污染情况下可能出现的亮度。     2. ** anthropogenic photons文档**：    - 这个文档试图提供一个物理定义来解释自然夜空中的光来源浓度，并探讨这些光源如何影响光污染水平。它关注的是具体的物理量（光电流密度），并讨论了特定地点和时间条件下空气传播路径上的单位体积中的光电流密度。  总结来说，GAMBONS模型关注的是通过观测者视角的总体夜间天空亮度分布，而anthropogenic photons文档关注的是光源浓度这个物理量及其对光污染水平的影响。
