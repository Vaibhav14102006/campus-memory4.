"""
GPU-Optimized NER Model Training Script
Trains Named Entity Recognition model using NVIDIA GPU (CUDA)
Uses NVIDIA GeForce RTX 3050 6GB with CUDA 12.6
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("🚀 GPU-ACCELERATED NER MODEL TRAINING")
print("="*80)

# Check if PyTorch is installed
try:
    import torch
    TORCH_INSTALLED = True
    print(f"✅ PyTorch version: {torch.__version__}")
except ImportError:
    TORCH_INSTALLED = False
    print("❌ PyTorch not installed!")
    sys.exit(1)

# Check GPU availability
if torch.cuda.is_available():
    print(f"✅ CUDA available: {torch.version.cuda}")
    print(f"✅ GPU count: {torch.cuda.device_count()}")
    print(f"✅ GPU name: {torch.cuda.get_device_name(0)}")
    print(f"✅ GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    device = torch.device("cuda")
    
    # 🔥 ENABLE ALL GPU OPTIMIZATIONS FOR MAXIMUM SPEED!
    torch.backends.cudnn.benchmark = True  # Auto-tune best algorithms
    torch.backends.cuda.matmul.allow_tf32 = True  # TensorFloat-32 for matmul
    torch.backends.cudnn.allow_tf32 = True  # TensorFloat-32 for cuDNN
    print("🔥 GPU optimizations enabled: cuDNN benchmark, TF32")
else:
    print("⚠️  CUDA not available! Training will use CPU (slower)")
    device = torch.device("cpu")

# Check transformers
try:
    from transformers import (
        AutoTokenizer,
        AutoModelForTokenClassification,
        TrainingArguments,
        Trainer,
        DataCollatorForTokenClassification
    )
    from torch.utils.data import Dataset
    print("✅ Transformers library loaded")
except ImportError:
    print("❌ Transformers not installed!")
    print("   pip install transformers")
    sys.exit(1)

print()

# ============================================================================
# NER DATASET CLASS
# ============================================================================

class NERDataset(Dataset):
    """Custom dataset for Named Entity Recognition"""
    
    def __init__(self, texts, tags, label2id, tokenizer, max_length=128):
        self.texts = texts
        self.tags = tags
        self.label2id = label2id
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        tags = eval(self.tags[idx]) if isinstance(self.tags[idx], str) else self.tags[idx]
        
        # Tokenize
        encoding = self.tokenizer(
            text.split(),
            is_split_into_words=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # Align labels
        labels = []
        word_ids = encoding.word_ids(batch_index=0)
        previous_word_idx = None
        
        for word_idx in word_ids:
            if word_idx is None:
                labels.append(-100)
            elif word_idx != previous_word_idx:
                try:
                    labels.append(self.label2id[tags[word_idx]])
                except:
                    labels.append(self.label2id['O'])
            else:
                labels.append(-100)
            previous_word_idx = word_idx
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(labels, dtype=torch.long)
        }

# ============================================================================
# TRAINING FUNCTION
# ============================================================================

def train_ner_model(train_file, val_file, output_dir, model_name="distilbert-base-uncased"):
    """
    Train NER model optimized for GPU
    
    Args:
        train_file: Path to training CSV
        val_file: Path to validation CSV
        output_dir: Directory to save model
        model_name: HuggingFace model name
    """
    
    print("\n" + "="*80)
    print(f"🔧 TRAINING NER MODEL")
    print("="*80)
    
    # Check files
    if not os.path.exists(train_file):
        print(f"❌ Training file not found: {train_file}")
        return False
    if not os.path.exists(val_file):
        print(f"❌ Validation file not found: {val_file}")
        return False
    
    # Load data
    print("\n📊 Loading data...")
    train_df = pd.read_csv(train_file)
    val_df = pd.read_csv(val_file)
    
    print(f"   Train samples: {len(train_df):,}")
    print(f"   Val samples: {len(val_df):,}")
    
    # Define NER labels
    ner_labels = ['O', 'B-EVENT', 'I-EVENT', 'B-DATE', 'I-DATE', 'B-LOCATION', 'I-LOCATION']
    label2id = {label: i for i, label in enumerate(ner_labels)}
    id2label = {i: label for label, i in label2id.items()}
    
    print(f"   NER Tags: {len(ner_labels)}")
    for idx, label in id2label.items():
        print(f"      {idx}: {label}")
    
    # Initialize tokenizer and model
    print(f"\n🤖 Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        num_labels=len(ner_labels),
        id2label=id2label,
        label2id=label2id
    )
    
    # Move model to GPU
    model = model.to(device)
    print(f"   Model moved to: {device}")
    
    if torch.cuda.is_available():
        print(f"   GPU memory allocated: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
    
    # Create datasets
    print("\n📦 Preparing datasets...")
    train_dataset = NERDataset(
        train_df['text'].tolist(),
        train_df['entities'].tolist(),
        label2id,
        tokenizer,
        max_length=128
    )
    
    val_dataset = NERDataset(
        val_df['text'].tolist(),
        val_df['entities'].tolist(),
        label2id,
        tokenizer,
        max_length=128
    )
    
    # GPU-Optimized training arguments - MAXIMIZED FOR 6GB GPU!
    print("\n⚙️  Configuring MAXIMUM GPU-optimized training...")
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=128,  # 🔥 4X LARGER! Using full 6GB GPU
        per_device_eval_batch_size=256,   # 🔥 4X LARGER! Max speed eval
        learning_rate=5e-5,
        weight_decay=0.01,
        warmup_steps=500,
        logging_dir=f'{output_dir}/logs',
        logging_steps=25,  # More frequent updates
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        save_total_limit=2,
        fp16=True,  # Mixed precision training for faster GPU training
        tf32=True,  # TensorFloat-32 for even faster training on RTX 3050
        dataloader_num_workers=8,  # 🔥 2X more parallel data loading
        dataloader_pin_memory=True,  # Faster GPU transfer
        gradient_accumulation_steps=1,
        gradient_checkpointing=False,  # We have enough memory, skip checkpointing for speed
        remove_unused_columns=False,
        optim="adamw_torch_fused",  # 🔥 Fused optimizer for 20% speedup
        torch_compile=False,  # Disabled for compatibility
    )
    
    print(f"   Batch size (train): {training_args.per_device_train_batch_size}")
    print(f"   Batch size (eval): {training_args.per_device_eval_batch_size}")
    print(f"   Epochs: {training_args.num_train_epochs}")
    print(f"   Mixed precision (FP16): {training_args.fp16}")
    print(f"   Device: {training_args.device}")
    
    # Compute metrics
    def compute_metrics(eval_pred):
        from sklearn.metrics import accuracy_score
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=-1)
        
        # Remove ignored labels (-100)
        true_labels = [[id2label[l] for l in label if l != -100] for label in labels]
        pred_labels = [[id2label[p] for (p, l) in zip(prediction, label) if l != -100] 
                      for prediction, label in zip(predictions, labels)]
        
        # Calculate accuracy
        correct = sum([1 for true, pred in zip(true_labels, pred_labels) 
                      for t, p in zip(true, pred) if t == p])
        total = sum([len(true) for true in true_labels])
        
        return {'accuracy': correct / total if total > 0 else 0}
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=DataCollatorForTokenClassification(tokenizer=tokenizer),
        compute_metrics=compute_metrics
    )
    
    # Train
    print("\n🏋️  Training started...")
    print("-"*80)
    
    trainer.train()
    
    print("\n✅ Training completed!")
    
    if torch.cuda.is_available():
        print(f"   Max GPU memory used: {torch.cuda.max_memory_allocated(0) / 1024**3:.2f} GB")
    
    # Evaluate
    print("\n📊 Evaluating on validation set...")
    eval_results = trainer.evaluate()
    
    print("\n📈 Results:")
    for key, value in eval_results.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.4f}")
    
    # Save model
    print(f"\n💾 Saving model to: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save label mappings
    with open(f"{output_dir}/label_mapping.json", "w") as f:
        json.dump({
            "label2id": label2id,
            "id2label": id2label
        }, f, indent=2)
    
    print("✅ Model saved successfully!")
    
    return True

# ============================================================================
# MAIN TRAINING PIPELINE
# ============================================================================

def main():
    """Main training pipeline"""
    
    os.chdir(Path(__file__).parent)
    print(f"\n📁 Working directory: {os.getcwd()}\n")
    
    # Train NER Model
    if os.path.exists("training_data/ner_train.csv"):
        print("\n" + "🎯 TRAINING NER MODEL")
        success = train_ner_model(
            train_file="training_data/ner_train.csv",
            val_file="training_data/ner_val.csv",
            output_dir="./models/ner_model"
        )
        
        # Clear GPU cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("\n🧹 GPU cache cleared")
    else:
        print("⚠️  NER training data not found!")
        success = False
    
    # Summary
    print("\n" + "="*80)
    print("📊 TRAINING SUMMARY")
    print("="*80)
    
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"   NER Model: {status}")
    
    if torch.cuda.is_available():
        print(f"\n💻 GPU Stats:")
        print(f"   Total GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
        print(f"   Peak GPU memory used: {torch.cuda.max_memory_allocated(0) / 1024**3:.2f} GB")
    
    print("\n" + "="*80)
    print("🎉 TRAINING PIPELINE COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()
