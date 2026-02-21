"""
GPU-Optimized Model Training Script
Trains Category and School Classifiers using NVIDIA GPU (CUDA)
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
print("🚀 GPU-ACCELERATED MODEL TRAINING")
print("="*80)

# Check if PyTorch is installed
try:
    import torch
    TORCH_INSTALLED = True
    print(f"✅ PyTorch version: {torch.__version__}")
except ImportError:
    TORCH_INSTALLED = False
    print("❌ PyTorch not installed!")
    print("\n📥 To install PyTorch with GPU support (CUDA 12.1):")
    print("   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    print("\n   Note: This will download ~2.4GB")
    sys.exit(1)

# Check GPU availability
if torch.cuda.is_available():
    print(f"✅ CUDA available: {torch.version.cuda}")
    print(f"✅ GPU count: {torch.cuda.device_count()}")
    print(f"✅ GPU name: {torch.cuda.get_device_name(0)}")
    print(f"✅ GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    device = torch.device("cuda")
    
    # 🔥🔥🔥 INSANE GPU OPTIMIZATIONS FOR LUDICROUS SPEED! 🔥🔥🔥
    torch.backends.cudnn.benchmark = True  # Auto-tune best algorithms
    torch.backends.cudnn.deterministic = False  # Disable for maximum speed
    torch.backends.cuda.matmul.allow_tf32 = True  # TensorFloat-32 for matmul
    torch.backends.cudnn.allow_tf32 = True  # TensorFloat-32 for cuDNN
    torch.set_float32_matmul_precision('medium')  # Use TF32 for all float32 ops
    
    # Pre-allocate maximum GPU memory for faster allocation
    torch.cuda.empty_cache()
    # Aggressive memory allocator settings for maximum speed
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512,expandable_segments:True'
    os.environ['CUDA_LAUNCH_BLOCKING'] = '0'  # Async CUDA operations
    
    # Set high priority for this process
    try:
        import psutil
        p = psutil.Process(os.getpid())
        if hasattr(p, 'nice'):
            p.nice(-10)  # High priority
    except:
        pass
    
    print("🔥 EXTREME GPU optimizations enabled:")
    print("   ✓ cuDNN benchmark (auto-tuned)")
    print("   ✓ TF32 precision (faster computation)")
    print("   ✓ Non-deterministic mode (maximum speed)")
    print("   ✓ Optimized memory allocation")
else:
    print("⚠️  CUDA not available! Training will use CPU (slower)")
    device = torch.device("cpu")

# Check transformers
try:
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        TrainingArguments,
        Trainer
    )
    from torch.utils.data import Dataset
    print("✅ Transformers library loaded")
except ImportError:
    print("❌ Transformers not installed!")
    print("   pip install transformers")
    sys.exit(1)

print()

# ============================================================================
# DATASET CLASS
# ============================================================================

class PosterDataset(Dataset):
    """Custom dataset for poster text classification"""
    
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# ============================================================================
# TRAINING FUNCTION
# ============================================================================

def train_classifier(train_file, val_file, label_column, output_dir, model_name="distilbert-base-uncased"):
    """
    Train a classifier optimized for GPU
    
    Args:
        train_file: Path to training CSV
        val_file: Path to validation CSV
        label_column: Column name for labels ('category' or 'school')
        output_dir: Directory to save model
        model_name: HuggingFace model name
    """
    
    print("\n" + "="*80)
    print(f"🔧 TRAINING {label_column.upper()} CLASSIFIER")
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
    
    # Create label mapping
    unique_labels = sorted(train_df[label_column].unique())
    label2id = {label: idx for idx, label in enumerate(unique_labels)}
    id2label = {idx: label for label, idx in label2id.items()}
    
    print(f"   Classes: {len(unique_labels)}")
    for idx, label in id2label.items():
        print(f"      {idx}: {label}")
    
    # Map labels to IDs
    train_labels = train_df[label_column].map(label2id).values
    val_labels = val_df[label_column].map(label2id).values
    
    # Initialize tokenizer and model
    print(f"\n🤖 Loading {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(unique_labels),
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
    train_dataset = PosterDataset(train_df['text'].values, train_labels, tokenizer, max_length=128)
    val_dataset = PosterDataset(val_df['text'].values, val_labels, tokenizer, max_length=128)
    
    # 🚀🚀🚀 FAST TRAINING - SMALL BATCHES FOR COMPLETION! 🚀🚀🚀
    print("\n⚡ Configuring FAST GPU training (quick completion)...")
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=1,  # 🔥 Just 1 epoch for fast completion!
        per_device_train_batch_size=32,  # 🔥 Smaller batches = stable & fast
        per_device_eval_batch_size=64,   # 🔥 Moderate eval batch
        learning_rate=5e-5,
        weight_decay=0.01,
        warmup_steps=20,  # Very minimal warmup
        logging_dir=f'{output_dir}/logs',
        logging_steps=50,  # Less frequent logging = faster
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        save_total_limit=1,  # Keep only 1 checkpoint = faster
        fp16=True,  # Mixed precision training (2X faster, 50% memory)
        tf32=True,  # TensorFloat-32 for RTX 3050 (extra 20% speed)
        dataloader_num_workers=0,  # 🔥 CRITICAL: 0 workers on Windows = 5X FASTER!
        dataloader_pin_memory=True,  # Faster CPU->GPU transfer
        gradient_accumulation_steps=1,
        gradient_checkpointing=False,  # Maximum speed, no memory saving
        remove_unused_columns=False,
        optim="adamw_torch_fused",  # 🔥 Fused optimizer (20% faster)
        torch_compile=False,  # Disabled for stability
        max_grad_norm=1.0,  # Gradient clipping for stability
    )
    
    print(f"   Batch size (train): {training_args.per_device_train_batch_size}")
    print(f"   Batch size (eval): {training_args.per_device_eval_batch_size}")
    print(f"   Epochs: {training_args.num_train_epochs}")
    print(f"   Mixed precision (FP16): {training_args.fp16}")
    print(f"   Device: {training_args.device}")
    
    # Compute metrics (optional - works without sklearn)
    def compute_metrics(eval_pred):
        try:
            from sklearn.metrics import accuracy_score, f1_score
            predictions, labels = eval_pred
            predictions = np.argmax(predictions, axis=1)
            
            return {
                'accuracy': accuracy_score(labels, predictions),
                'f1': f1_score(labels, predictions, average='weighted')
            }
        except ImportError:
            # sklearn not available - compute basic accuracy manually
            predictions, labels = eval_pred
            predictions = np.argmax(predictions, axis=1)
            accuracy = (predictions == labels).mean()
            return {'accuracy': float(accuracy)}
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
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
    
    results = {}
    
    # 1. Train Category Classifier
    if os.path.exists("training_data/category_train.csv"):
        print("\n" + "🎯 TASK 1/2: Category Classifier")
        success = train_classifier(
            train_file="training_data/category_train.csv",
            val_file="training_data/category_val.csv",
            label_column="category",
            output_dir="./models/category_classifier"
        )
        results['category'] = success
        
        # Clear GPU cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("\n🧹 GPU cache cleared")
    else:
        print("⚠️  Category training data not found!")
        results['category'] = False
    
    # 2. Train School Classifier
    if os.path.exists("training_data/school_train.csv"):
        print("\n" + "🎯 TASK 2/2: School Classifier")
        success = train_classifier(
            train_file="training_data/school_train.csv",
            val_file="training_data/school_val.csv",
            label_column="school",
            output_dir="./models/school_classifier"
        )
        results['school'] = success
        
        # Clear GPU cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("\n🧹 GPU cache cleared")
    else:
        print("⚠️  School training data not found!")
        results['school'] = False
    
    # Summary
    print("\n" + "="*80)
    print("📊 TRAINING SUMMARY")
    print("="*80)
    
    for model_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"   {model_name.capitalize()}: {status}")
    
    if torch.cuda.is_available():
        print(f"\n💻 GPU Stats:")
        print(f"   Total GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
        print(f"   Peak GPU memory used: {torch.cuda.max_memory_allocated(0) / 1024**3:.2f} GB")
    
    print("\n" + "="*80)
    print("🎉 TRAINING PIPELINE COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()
