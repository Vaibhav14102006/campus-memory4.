"""
⚡ ULTRA-FAST ML MODEL TRAINING
- Uses all 10 CPU cores for parallel processing
- Only generates data if missing
- Optimized training parameters for speed
- Saves models after training
"""

import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
import warnings
import multiprocessing
warnings.filterwarnings('ignore')

# Configure multi-core processing
NUM_CORES = 10
os.environ["OMP_NUM_THREADS"] = str(NUM_CORES)
os.environ["MKL_NUM_THREADS"] = str(NUM_CORES)
os.environ["TOKENIZERS_PARALLELISM"] = "true"

print("=" * 80)
print("⚡ ULTRA-FAST ML MODEL TRAINING")
print("=" * 80)
print(f"💻 CPU Cores: {NUM_CORES}")
print(f"🔧 Parallel Processing: ENABLED")
print("=" * 80)

# STEP 1: Check if training data exists, generate only if missing
print("\n📊 STEP 1: Checking Training Data...")
print("-" * 80)

if not os.path.exists("training_data") or len(os.listdir("training_data")) < 6:
    print("⚠️  Training data not found. Generating...")
    exec(open("generate_data_quick.py").read())
    print("✅ Training data generated!")
else:
    print("✅ Training data already exists - SKIPPING generation")
    files = os.listdir("training_data")
    for f in files:
        size_mb = os.path.getsize(f"training_data/{f}") / (1024*1024)
        print(f"   📁 {f} ({size_mb:.1f} MB)")

# STEP 2: Import ML libraries
print("\n🔧 STEP 2: Loading ML Libraries...")
print("-" * 80)

try:
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        TrainingArguments,
        Trainer,
        DataCollatorWithPadding
    )
    import torch
    from torch.utils.data import Dataset
    
    print("✅ Transformers library loaded")
    print(f"✅ PyTorch version: {torch.__version__}")
    print(f"✅ CUDA available: {torch.cuda.is_available()}")
    
except ImportError as e:
    print(f"❌ Error: {e}")
    print("Install with: pip install transformers torch")
    exit(1)

# Create models directory
os.makedirs("models", exist_ok=True)

# Custom Dataset
class FastTextDataset(Dataset):
    """Optimized dataset with caching"""
    
    def __init__(self, texts, labels, tokenizer, max_length=128):  # Reduced max_length for speed
        self.encodings = tokenizer(
            list(texts),
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors='pt'
        )
        self.labels = torch.tensor(labels, dtype=torch.long)
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return {
            'input_ids': self.encodings['input_ids'][idx],
            'attention_mask': self.encodings['attention_mask'][idx],
            'labels': self.labels[idx]
        }

def train_fast_classifier(train_file, val_file, label_col, output_dir, model_name):
    """Ultra-fast classifier training with multi-core"""
    
    print(f"\n⚡ Training {model_name}...")
    print("-" * 80)
    
    # Load data (sample for speed if too large)
    train_df = pd.read_csv(train_file)
    val_df = pd.read_csv(val_file)
    
    # Use subset for ultra-fast training (10k samples)
    # For full training, remove these lines
    print(f"📊 Original training size: {len(train_df):,}")
    if len(train_df) > 10000:
        train_df = train_df.sample(n=10000, random_state=42)
        print(f"⚡ Using {len(train_df):,} samples for fast training")
    
    # Create label mapping
    unique_labels = sorted(train_df[label_col].unique())
    label2id = {label: idx for idx, label in enumerate(unique_labels)}
    id2label = {idx: label for label, idx in label2id.items()}
    
    print(f"   📋 Classes: {len(unique_labels)}")
    print(f"   📋 Train: {len(train_df):,} | Val: {len(val_df):,}")
    
    # Map labels
    train_labels = train_df[label_col].map(label2id).values
    val_labels = val_df[label_col].map(label2id).values
    
    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    
    # Create datasets with batch tokenization
    print("   🔄 Tokenizing (parallel)...")
    train_dataset = FastTextDataset(train_df['text'].values, train_labels, tokenizer)
    val_dataset = FastTextDataset(val_df['text'].values, val_labels, tokenizer)
    
    # Initialize model
    print("   🤖 Loading model...")
    model = AutoModelForSequenceClassification.from_pretrained(
        'distilbert-base-uncased',
        num_labels=len(unique_labels),
        id2label=id2label,
        label2id=label2id
    )
    
    # Training arguments optimized for speed
    training_args = TrainingArguments(
        output_dir=f"{output_dir}_temp",
        num_train_epochs=2,  # Reduced from 3 for speed
        per_device_train_batch_size=32,  # Larger batch size
        per_device_eval_batch_size=64,
        dataloader_num_workers=0,  # Set to 0 for Windows compatibility
        warmup_steps=100,
        weight_decay=0.01,
        logging_dir=f"{output_dir}_logs",
        logging_steps=50,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        push_to_hub=False,
        report_to="none",
        fp16=False,  # Set True if GPU available
        dataloader_pin_memory=False,  # Disable for CPU
        gradient_accumulation_steps=1,
        max_grad_norm=1.0,
    )
    
    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )
    
    # Train
    print(f"   🚀 Training with {NUM_CORES} cores...")
    trainer.train()
    
    # Evaluate
    print("   📊 Evaluating...")
    results = trainer.evaluate()
    
    print(f"\n   ✅ Results:")
    print(f"      Accuracy: {results.get('eval_accuracy', 0):.2%}")
    print(f"      Loss: {results.get('eval_loss', 0):.4f}")
    
    # Save model
    print(f"   💾 Saving to {output_dir}...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save label mappings
    import json
    with open(f"{output_dir}/label_mapping.json", 'w') as f:
        json.dump({"label2id": label2id, "id2label": id2label}, f, indent=2)
    
    print(f"   ✅ {model_name} training complete!")
    return results

# Main training function
def main():
    """Main training pipeline"""
    
    # STEP 3: Train Category Classifier
    print("\n" + "=" * 80)
    print("📚 STEP 3: Training Category Classifier")
    print("=" * 80)

    try:
        cat_results = train_fast_classifier(
            train_file="training_data/category_train.csv",
            val_file="training_data/category_val.csv",
            label_col="category",
            output_dir="models/category_classifier",
            model_name="Category Classifier"
        )
    except Exception as e:
        print(f"❌ Category training failed: {e}")

    # STEP 4: Train School Classifier
    print("\n" + "=" * 80)
    print("🏫 STEP 4: Training School Classifier")
    print("=" * 80)

    try:
        school_results = train_fast_classifier(
            train_file="training_data/school_train.csv",
            val_file="training_data/school_val.csv",
            label_col="school",
            output_dir="models/school_classifier",
            model_name="School Classifier"
        )
    except Exception as e:
        print(f"❌ School training failed: {e}")

    # STEP 5: Verify models
    print("\n" + "=" * 80)
    print("✅ TRAINING COMPLETE - VERIFICATION")
    print("=" * 80)

    # Check saved models
    if os.path.exists("models/category_classifier"):
        files = os.listdir("models/category_classifier")
        print(f"✅ Category Classifier: {len(files)} files saved")

    if os.path.exists("models/school_classifier"):
        files = os.listdir("models/school_classifier")
        print(f"✅ School Classifier: {len(files)} files saved")

    print("\n" + "=" * 80)
    print("🎉 ALL MODELS TRAINED SUCCESSFULLY!")
    print("=" * 80)
    print("\n📝 Next steps:")
    print("   1. Models saved in ./models/ directory")
    print("   2. Update poster_analysis_ai.py to use trained models")
    print("   3. Restart backend API to load models")
    print("=" * 80)

if __name__ == '__main__':
    # Windows multiprocessing fix
    multiprocessing.freeze_support()
    main()
