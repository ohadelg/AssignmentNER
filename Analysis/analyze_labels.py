import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch
from tqdm import tqdm

# Set device
device = 0 if torch.cuda.is_available() else -1
print(f"Using device: {device}")

def load_dnrti_file(file_path):
    data = []
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found.")
        return data
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        tokens = []
        labels = []
        for line in f:
            line = line.strip()
            if not line:
                if tokens:
                    data.append({'tokens': tokens, 'labels': labels})
                    tokens = []
                    labels = []
            else:
                parts = line.split()
                if len(parts) >= 2:
                    tokens.append(parts[0])
                    labels.append(parts[-1])
        if tokens:
             data.append({'tokens': tokens, 'labels': labels})
    return data

def align_predictions_raw(predictions, token_list):
    """
    Aligns pipeline predictions to original tokens, returning RAW labels.
    """
    aligned_labels = ['O'] * len(token_list)
    
    # Create character spans for tokens
    token_spans = []
    current_char = 0
    for token in token_list:
        start = current_char
        end = start + len(token)
        token_spans.append((start, end))
        current_char = end + 1 # +1 for space
        
    for pred in predictions:
        p_start = pred['start']
        p_end = pred['end']
        entity_group = pred['entity_group']
        
        for idx, (t_start, t_end) in enumerate(token_spans):
            if max(t_start, p_start) < min(t_end, p_end):
                aligned_labels[idx] = entity_group
                
    return aligned_labels

def run_analysis(model_path, model_name, train_data, sample_size=2000):
    print(f"\n--- Analyzing {model_name} ---")
    print(f"Loading {model_name} from {model_path}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)

    correlations = []
    print(f"Processing {sample_size} sentences...")

    for i in tqdm(range(sample_size)):
        tokens = train_data[i]['tokens']
        true_labels = train_data[i]['labels']
        
        # Strip B-/I- prefixes from true labels
        true_labels_raw = [l[2:] if l != 'O' else 'O' for l in true_labels]
        
        # Run prediction
        sentence = " ".join(tokens)
        try:
            preds = nlp(sentence)
        except Exception as e:
            print(f"Error processing sentence {i}: {e}")
            continue
        
        # Align
        pred_labels_raw = align_predictions_raw(preds, tokens)
        
        # Record pairs
        for p, t in zip(pred_labels_raw, true_labels_raw):
            correlations.append({'Predicted': p, 'True': t})

    df_corr = pd.DataFrame(correlations)
    
    # Save results
    output_file = f"label_correlation_{model_name.lower()}.csv"
    df_corr.to_csv(output_file, index=False)
    print(f"Saved correlations to {output_file}")
    
    return df_corr

if __name__ == "__main__":
    train_data = load_dnrti_file("../DNRTI/train.txt")
    print(f"Loaded {len(train_data)} sentences from ../DNRTI/train.txt")
    
    sample_size = min(2000, len(train_data))
    
    # Define models to test
    models = [
        {"path": "../NER/CyNER", "name": "CyNER"},
        {"path": "../NER/SecureBert-NER", "name": "SecureBERT"}
    ]
    
    for m in models:
        run_analysis(m["path"], m["name"], train_data, sample_size)
    
    print("\nAll analyses complete.")
