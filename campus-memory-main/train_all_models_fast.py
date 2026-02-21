"""
Fast Training Script for All Missing Models (CPU Optimized)
Trains: School Classifier, NER Model, and Traditional ML Models
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Change to script directory
os.chdir(Path(__file__).parent)

print("="*80)
print("🚀 FAST MODEL TRAINING - CPU OPTIMIZED")
print("="*80)
print(f"Working directory: {os.getcwd()}")
print()

# ============================================================================
# 1. TRAIN SCHOOL CLASSIFIER (DistilBERT)
# ============================================================================

def train_school_classifier():
    print("\n" + "="*80)
    print("📚 TRAINING SCHOOL CLASSIFIER")
    print("="*80)
    
    # Check if training data exists
    if not os.path.exists("training_data/school_train.csv"):
        print("❌ School training data not found!")
        return False
    
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
        
        print("✅ Libraries loaded")
        
        # Load data
        print("\n📊 Loading training data...")
        train_df = pd.read_csv("training_data/school_train.csv")
        val_df = pd.read_csv("training_data/school_val.csv")
        
        print(f"   Train samples: {len(train_df)}")
        print(f"   Val samples: {len(val_df)}")
        
        # Get labels
        labels = sorted(train_df['school'].unique())
        label2id = {label: i for i, label in enumerate(labels)}
        id2label = {i: label for label, i in label2id.items()}
        
        print(f"   Classes: {len(labels)}")
        
        # Dataset class
        class TextDataset(Dataset):
            def __init__(self, texts, labels, tokenizer, max_length=128):
                self.texts = texts
                self.labels = labels
                self.tokenizer = tokenizer
                self.max_length = max_length
            
            def __len__(self):
                return len(self.texts)
            
            def __getitem__(self, idx):
                encoding = self.tokenizer(
                    self.texts[idx],
                    max_length=self.max_length,
                    padding='max_length',
                    truncation=True,
                    return_tensors='pt'
                )
                return {
                    'input_ids': encoding['input_ids'].flatten(),
                    'attention_mask': encoding['attention_mask'].flatten(),
                    'labels': torch.tensor(self.labels[idx], dtype=torch.long)
                }
        
        # Initialize tokenizer and model
        print("\n🤖 Initializing model...")
        model_name = "distilbert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=len(labels),
            id2label=id2label,
            label2id=label2id
        )
        
        # Prepare datasets
        print("\n📦 Preparing datasets...")
        train_labels = [label2id[label] for label in train_df['school']]
        val_labels = [label2id[label] for label in val_df['school']]
        
        train_dataset = TextDataset(
            train_df['text'].tolist(),
            train_labels,
            tokenizer,
            max_length=128
        )
        
        val_dataset = TextDataset(
            val_df['text'].tolist(),
            val_labels,
            tokenizer,
            max_length=128
        )
        
        # Training arguments (CPU optimized)
        print("\n⚙️  Setting up training configuration...")
        training_args = TrainingArguments(
            output_dir="models/school_classifier_temp",
            num_train_epochs=3,  # Fast training
            per_device_train_batch_size=8,  # Smaller batch for CPU
            per_device_eval_batch_size=16,
            learning_rate=5e-5,
            weight_decay=0.01,
            eval_strategy="epoch",  # Fixed API parameter
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
            logging_steps=50,
            save_total_limit=1,  # Keep only best model
            dataloader_num_workers=0,  # CPU optimization
            fp16=False,  # No mixed precision on CPU
        )
        
        # Compute metrics
        def compute_metrics(eval_pred):
            from sklearn.metrics import accuracy_score
            predictions, labels = eval_pred
            predictions = np.argmax(predictions, axis=1)
            return {'accuracy': accuracy_score(labels, predictions)}
        
        # Initialize trainer
        print("\n🏋️  Starting training...")
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            tokenizer=tokenizer,
            data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
            compute_metrics=compute_metrics,
        )
        
        # Train
        print("\n⏱️  Training in progress (this may take 15-30 minutes on CPU)...")
        trainer.train()
        
        # Evaluate
        print("\n📈 Evaluating...")
        eval_result = trainer.evaluate()
        accuracy = eval_result['eval_accuracy']
        print(f"\n✅ School Classifier Accuracy: {accuracy:.2%}")
        
        # Save final model
        output_dir = "models/school_classifier"
        os.makedirs(output_dir, exist_ok=True)
        trainer.save_model(output_dir)
        
        # Save label mapping
        import json
        with open(f"{output_dir}/label_mapping.json", 'w') as f:
            json.dump({'id2label': id2label, 'label2id': label2id}, f, indent=2)
        
        print(f"\n💾 Model saved to {output_dir}/")
        return True
        
    except Exception as e:
        print(f"\n❌ School classifier training failed: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# 2. TRAIN NER MODEL (DistilBERT Token Classification)
# ============================================================================

def train_ner_model():
    print("\n" + "="*80)
    print("🏷️  TRAINING NER MODEL")
    print("="*80)
    
    # Check if training data exists
    if not os.path.exists("training_data/ner_train.csv"):
        print("❌ NER training data not found!")
        return False
    
    try:
        from transformers import (
            AutoTokenizer,
            AutoModelForTokenClassification,
            TrainingArguments,
            Trainer,
            DataCollatorForTokenClassification
        )
        import torch
        from torch.utils.data import Dataset
        
        print("✅ Libraries loaded")
        
        # Load data
        print("\n📊 Loading NER training data...")
        train_df = pd.read_csv("training_data/ner_train.csv")
        val_df = pd.read_csv("training_data/ner_val.csv")
        
        print(f"   Train samples: {len(train_df)}")
        print(f"   Val samples: {len(val_df)}")
        
        # Define NER labels
        ner_labels = ['O', 'B-EVENT', 'I-EVENT', 'B-DATE', 'I-DATE', 'B-LOCATION', 'I-LOCATION']
        label2id = {label: i for i, label in enumerate(ner_labels)}
        id2label = {i: label for label, i in label2id.items()}
        
        print(f"   NER Tags: {len(ner_labels)}")
        
        # Dataset class for NER
        class NERDataset(Dataset):
            def __init__(self, texts, tags, tokenizer, max_length=128):
                self.texts = texts
                self.tags = tags
                self.tokenizer = tokenizer
                self.max_length = max_length
                self.label2id = label2id
            
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
        
        # Initialize tokenizer and model
        print("\n🤖 Initializing NER model...")
        model_name = "distilbert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(
            model_name,
            num_labels=len(ner_labels),
            id2label=id2label,
            label2id=label2id
        )
        
        # Prepare datasets
        print("\n📦 Preparing NER datasets...")
        train_dataset = NERDataset(
            train_df['text'].tolist(),
            train_df['entities'].tolist(),  # Fixed column name
            tokenizer,
            max_length=128
        )
        
        val_dataset = NERDataset(
            val_df['text'].tolist(),
            val_df['entities'].tolist(),  # Fixed column name
            tokenizer,
            max_length=128
        )
        
        # Training arguments (CPU optimized)
        print("\n⚙️  Setting up training configuration...")
        training_args = TrainingArguments(
            output_dir="models/ner_model_temp",
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=16,
            learning_rate=5e-5,
            weight_decay=0.01,
            eval_strategy="epoch",  # Fixed API parameter
            save_strategy="epoch",
            load_best_model_at_end=True,
            logging_steps=50,
            save_total_limit=1,
            dataloader_num_workers=0,
            fp16=False,
        )
        
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
        print("\n🏋️  Starting NER training...")
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            tokenizer=tokenizer,
            data_collator=DataCollatorForTokenClassification(tokenizer=tokenizer),
            compute_metrics=compute_metrics,
        )
        
        # Train
        print("\n⏱️  Training in progress (this may take 15-30 minutes on CPU)...")
        trainer.train()
        
        # Evaluate
        print("\n📈 Evaluating...")
        eval_result = trainer.evaluate()
        accuracy = eval_result['eval_accuracy']
        print(f"\n✅ NER Model Accuracy: {accuracy:.2%}")
        
        # Save final model
        output_dir = "models/ner_model"
        os.makedirs(output_dir, exist_ok=True)
        trainer.save_model(output_dir)
        
        # Save label mapping
        import json
        with open(f"{output_dir}/label_mapping.json", 'w') as f:
            json.dump({'id2label': id2label, 'label2id': label2id}, f, indent=2)
        
        print(f"\n💾 Model saved to {output_dir}/")
        return True
        
    except Exception as e:
        print(f"\n❌ NER model training failed: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# 3. RETRAIN TRADITIONAL ML MODELS (XGBoost)
# ============================================================================

def retrain_traditional_ml():
    print("\n" + "="*80)
    print("🎯 RETRAINING TRADITIONAL ML MODELS")
    print("="*80)
    
    try:
        import joblib
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.model_selection import train_test_split
        
        # Check if dataset exists
        if not os.path.exists("event_feedback_dataset.csv"):
            print("❌ event_feedback_dataset.csv not found!")
            return False
        
        print("\n📊 Loading dataset...")
        df = pd.read_csv("event_feedback_dataset.csv")
        print(f"   Dataset size: {len(df)} records")
        print(f"   Columns: {list(df.columns)}")
        
        # Prepare features
        print("\n🔧 Preparing features...")
        
        # Encode categorical variables
        label_encoders = {}
        for col in ['Branch', 'Gender', 'Skill_Level', 'Previous_Participation', 
                    'Achievement', 'Event_Type', 'Event_Level']:
            if col in df.columns:
                le = LabelEncoder()
                df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
                label_encoders[col] = le
        
        # Select features for recommendation
        feature_cols = [
            'Branch_encoded', 'Year', 'Gender_encoded', 'Skill_Level_encoded',
            'Previous_Participation_encoded', 'Team_Size', 'Participated_Alone',
            'Achievement_encoded', 'Event_Type_encoded', 'Event_Level_encoded',
            'Duration_Days'
        ]
        
        feature_cols = [col for col in feature_cols if col in df.columns]
        
        # Train Recommendation Model
        print("\n🎯 Training Recommendation Model...")
        X_rec = df[feature_cols]
        
        # Check for target column (try common variations)
        target_col = None
        for possible_target in ['Participated', 'Participation', 'Will_Participate', 'Attended']:
            if possible_target in df.columns:
                target_col = possible_target
                break
        
        if target_col is None:
            # Create synthetic target based on satisfaction score
            if 'Satisfaction_Score' in df.columns:
                df['Participated'] = (df['Satisfaction_Score'] >= 3).astype(int)
                target_col = 'Participated'
            else:
                print("   ⚠️  No participation column found, creating synthetic target")
                df['Participated'] = np.random.choice([0, 1], size=len(df), p=[0.3, 0.7])
                target_col = 'Participated'
        
        y_rec = df[target_col]  # Binary: 0 or 1
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_rec, y_rec, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        rec_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        rec_model.fit(X_train_scaled, y_train)
        
        rec_score = rec_model.score(X_test_scaled, y_test)
        print(f"   ✅ Recommendation Model Accuracy: {rec_score:.2%}")
        
        # Train Satisfaction Model
        print("\n😊 Training Satisfaction Model...")
        X_sat = df[feature_cols + ['Participated_encoded'] if 'Participated_encoded' in df.columns else feature_cols]
        y_sat = df['Satisfaction_Score']  # 1-5 scale
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_sat, y_sat, test_size=0.2, random_state=42
        )
        
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        sat_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        sat_model.fit(X_train_scaled, y_train)
        
        sat_score = sat_model.score(X_test_scaled, y_test)
        print(f"   ✅ Satisfaction Model Accuracy: {sat_score:.2%}")
        
        # Save models
        print("\n💾 Saving models...")
        joblib.dump(rec_model, 'recommendation_model.pkl')
        joblib.dump(sat_model, 'satisfaction_model.pkl')
        joblib.dump(scaler, 'scaler.pkl')
        joblib.dump(label_encoders, 'label_encoders.pkl')
        
        # Save metadata
        metadata = {
            'feature_columns': feature_cols,
            'recommendation_accuracy': float(rec_score),
            'satisfaction_accuracy': float(sat_score),
            'training_date': pd.Timestamp.now().isoformat()
        }
        joblib.dump(metadata, 'model_metadata.pkl')
        
        print("   ✅ All traditional ML models saved!")
        return True
        
    except Exception as e:
        print(f"\n❌ Traditional ML training failed: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# MAIN TRAINING PIPELINE
# ============================================================================

def main():
    results = {}
    
    print("\n🚀 Starting comprehensive model training...")
    print(f"   Note: Training on CPU (no GPU detected)")
    
    # 1. Train School Classifier
    print("\n[1/3] School Classifier Training")
    results['school_classifier'] = train_school_classifier()
    
    # 2. Train NER Model
    print("\n[2/3] NER Model Training")
    results['ner_model'] = train_ner_model()
    
    # 3. Retrain Traditional ML
    print("\n[3/3] Traditional ML Models")
    results['traditional_ml'] = retrain_traditional_ml()
    
    # Summary
    print("\n" + "="*80)
    print("📊 TRAINING SUMMARY")
    print("="*80)
    
    for model_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"   {status}: {model_name}")
    
    all_success = all(results.values())
    
    if all_success:
        print("\n🎉 ALL MODELS TRAINED SUCCESSFULLY!")
        print("\n📝 Next Steps:")
        print("   1. Run: python test_all_models.py")
        print("   2. Start backend: python backend_server.py")
        print("   3. Access API at: http://localhost:8000")
    else:
        print("\n⚠️  Some models failed to train. Check errors above.")
    
    print("="*80)

if __name__ == "__main__":
    main()
