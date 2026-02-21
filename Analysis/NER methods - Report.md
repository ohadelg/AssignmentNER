# NER Model Comparison Report

## Introduction
The purpose of this report is to provide a comparative analysis of the two Named Entity Recognition (NER) models evaluated: **SecureBERT-NER** and **CyNER**. 

The findings unequivocally demonstrate that the **SecureBERT-NER** model outperforms the alternative across nearly all metrics, with the exception of a negligible difference in processing speed (a margin of only a few percentage points).

## Evaluation Process

### 1. Direct Testing (Baseline)
In the initial phase, a direct baseline comparison was conducted between the two models using the DNRTI dataset. At this stage, SecureBERT-NER already showed a significant lead in performance.
- **Reference:** `Analysis/comparison_v1.ipynb`
- **Initial Metrics (F1-Score):**
    - **CyNER:** 0.0255
    - **SecureBERT-NER:** 0.3057

### 2. Label Alignment & Mapping
It was identified that the labels were not directly comparable across models as each utilizes its own specific mapping system. To ensure an "apples-to-apples" comparison, the label sets were aligned to the DNRTI schema.
- **Reference:** `Analysis/comparison_v2.ipynb`
- **Post-Alignment Metrics (F1-Score):**
    - **CyNER:** 0.1694
    - **SecureBERT-NER:** 0.6606

### 3. Data Disparity & Refinement
Following the alignment, the performance metrics shifted significantly in favor of SecureBERT-NER. To ensure a fair assessment, further investigations were conducted to see if a more refined label mapping could improve CyNER's performance.
- **Reference:** `Analysis/label_mapping_analysis.ipynb`, `Analysis/analyze_labels.py`, and `Analysis/comparison_v3.ipynb`
- **Refined Metrics (F1-Score):**
    - **CyNER:** 0.3415
    - **SecureBERT-NER:** 0.7659

![Performance Comparison](performance_comparison_v3.png)
*Figure 1: Final Performance Metrics Comparison (from comparison_v3.ipynb).*

### 4. Heatmap Analysis
A mapping analysis was performed using heatmap visualizations to correlate predicted labels with ground truth. This confirmed—with statistical clarity—that SecureBERT-NER remains the superior choice for this task.

#### CyNER Heatmap
![CyNER Heatmap](heatmap_cyner.png)
*Figure 2: Correlation Heatmap for CyNER Predicted vs DNRTI True Labels.*

#### SecureBERT Heatmap
![SecureBERT Heatmap](heatmap_securebert.png)
*Figure 3: Correlation Heatmap for SecureBERT Predicted vs DNRTI True Labels.*

## Key Findings & Terminology
*   **Unequivocally Superior:** SecureBERT-NER is the clear winner in accuracy, precision, and recall.
*   **Negligible Latency Difference:** While CyNER is slightly faster (approx. 0.0446s vs 0.0452s per doc), the difference is statistically insignificant for most production use cases.
*   **Label Mapping:** Crucial for aligning different classification categories to a standard baseline.
*   **Baseline:** The initial unoptimized test used to establish the starting performance levels.

## Conclusion
Based on the extensive evaluation process, **SecureBERT-NER** is recommended for implementation due to its significantly higher F1-score and more reliable entity recognition capabilities.
