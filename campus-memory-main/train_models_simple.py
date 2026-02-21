"""
Simplified ML Model Training Script
Focus on Category and School Classifiers (DistilBERT)
"""

import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("🧠 ML MODEL TRAINING - SIMPLIFIED")
print("=" * 80)

# Check if training data exists
if not os.path.exists("training_data"):
    print("\n❌ Error: training_data directory not found!")
    print("Run: python generate_data_quick.py first")
    exit(1)

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
    
    print("✅ ML libraries loaded successfully")
except ImportError as e:
    print(f"❌ Error: {e}")
    print("Install with: pip install transformers torch")
    exit(1)

# Create models directory
os.makedirs("models", exist_ok=True)

class TextDataset(Dataset):
    """Custom dataset for text classification"""
    
    def __init__(self, texts, labels, tokenizer, max_length=256):
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

def train_classifier(train_file, val_file, label_column, model_name, output_dir):
    """Train a DistilBERT classifier"""
    
    print(f"\n{'='*80}")
    print(f"🔧 Training {label_column} Classifier")
    print(f"{'='*80}")
    
    # Load data
    print("📥 Loading training data...")
    train_df = pd.read_csv(train_file)
    val_df = pd.read_csv(val_file)
    
    # Create label mapping
    unique_labels = sorted(train_df[label_column].unique())
    label2id = {label: idx for idx, label in enumerate(unique_labels)}
    id2label = {idx: label for label, idx in label2id.items()}
    
    print(f"✅ Loaded {len(train_df):,} training samples")
    print(f"✅ Loaded {len(val_df):,} validation samples")
    print(f"✅ Number of classes: {len(unique_labels)}")
    
    # Map labels to IDs
    train_labels = train_df[label_column].map(label2id).values
    val_labels = val_df[label_column].map(label2id).values
    
    # Initialize tokenizer and model
    print("\n🤖 Initializing DistilBERT model...")
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
    model = AutoModelForSequenceClassification.from_pretrained(
        'distilbert-base-uncased',
        num_labels=len(unique_labels),
        id2label=id2label,
        label2id=label2id
    )
    
    # Create datasets
    print("📊 Preparing datasets...")
    train_dataset = TextDataset(train_df['text'].values, train_labels, tokenizer)
    val_dataset = TextDataset(val_df['text'].values, val_labels, tokenizer)
    
    # Training arguments (optimized for speed)
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,  # Reduced from 5 for faster training
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f'{output_dir}/logs',
        logging_steps=100,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        push_to_hub=False,
        report_to="none"
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer)
    )
    
    # Train
    print("\n🚀 Starting training...")
    print("⏱️  This may take 10-20 minutes per classifier...")
    trainer.train()
    
    # Evaluate
    print("\n📊 Evaluating model...")
    eval_result = trainer.evaluate()
    
    # Save model
    print(f"\n💾 Saving model to {output_dir}...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save label mappings
    import json
    with open(f"{output_dir}/label_mapping.json", "w") as f:
        json.dump({"label2id": label2id, "id2label": {str(k): v for k, v in id2label.items()}}, f, indent=2)
    
    # Calculate accuracy
    predictions = trainer.predict(val_dataset)
    pred_labels = np.argmax(predictions.predictions, axis=1)
    accuracy = accuracy_score(val_labels, pred_labels)
    
    print(f"\n✅ Training Complete!")
    print(f"   📈 Validation Accuracy: {accuracy:.2%}")
    print(f"   📁 Model saved to: {output_dir}")
    
    return accuracy

# Main training pipeline
print("\n" + "="*80)
print("TRAINING PIPELINE START")
print("="*80)

results = {}

# Train Category Classifier
if os.path.exists("training_data/category_train.csv"):
    try:
        acc = train_classifier(
            train_file="training_data/category_train.csv",
            val_file="training_data/category_val.csv",
            label_column="category",
            model_name="category_classifier",
            output_dir="models/category_classifier"
        )
        results["Category Classifier"] = acc
    except Exception as e:
        print(f"\n❌ Category classifier training failed: {e}")
        results["Category Classifier"] = None
else:
    print("\n⚠️  Category training data not found")

# Train School Classifier
if os.path.exists("training_data/school_train.csv"):
    try:
        acc = train_classifier(
            train_file="training_data/school_train.csv",
            val_file="training_data/school_val.csv",
            label_column="school",
            model_name="school_classifier",
            output_dir="models/school_classifier"
        )
        results["School Classifier"] = acc
    except Exception as e:
        print(f"\n❌ School classifier training failed: {e}")
        results["School Classifier"] = None
else:
    print("\n⚠️  School training data not found")

# Final Summary
print("\n" + "="*80)
print("🎉 TRAINING COMPLETE - SUMMARY")
print("="*80)

for model_name, accuracy in results.items():
    if accuracy:
        status = "✅" if accuracy >= 0.85 else "⚠️ "
        print(f"{status} {model_name}: {accuracy:.2%}")
    else:
        print(f"❌ {model_name}: Failed")

print("\n📁 Models saved in ./models/ directory")
print("\n✅ Models are ready to use!")
print("\n📝 Next: Update poster_analysis_ai.py to use trained models")
print("="*80)
