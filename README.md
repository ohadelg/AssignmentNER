# Assignment NER Comparison

This project aims to compare two Named Entity Recognition (NER) models on the DNRTI dataset.

## Project Structure

```
AssignmentNER/
├── DNRTI/                  # Dataset folder
│   └── DNRTI.rar           # Dataset archive (needs extraction)
├── NER/
│   ├── CyNER/              # CyNER model folder
│   └── SecureBert-NER/     # SecureBERT model folder
├── comparison.ipynb        # Comparison notebook
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

## Setup Instructions

1.  **Extract Data**:
    The dataset is located in `DNRTI/DNRTI.rar`. You must extract it manually if `unrar` is not installed on your system.
    ```bash
    cd DNRTI
    unrar x DNRTI.rar
    ```
    Ensure the extracted JSON/TXT files are directly accessible or update the loading logic in the notebook.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Comparison**:
    Open `comparison.ipynb` in Jupyter Notebook and run the cells.
    The notebook will:
    - Load the dataset (if extracted).
    - Download `CyNER` and `SecureBERT` models to the `NER` folder.
    - Split the data into test (90%) and validation (10%).
    - Evaluate both models.

## Models Compared
-   **CyNER**: [AI4Sec/cyner-xlm-roberta-base](https://huggingface.co/AI4Sec/cyner-xlm-roberta-base)
-   **SecureBERT**: [CyberPeace-Institute/SecureBERT-NER](https://huggingface.co/CyberPeace-Institute/SecureBERT-NER)
