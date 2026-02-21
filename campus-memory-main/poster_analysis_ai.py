"""
AI Poster Analysis Module
Phase 2: OCR + Classification + NER Pipeline
"""

import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import numpy as np

# Check if dateutil is available for better date parsing
try:
    from dateutil import parser as date_parser
    DATEUTIL_AVAILABLE = True
except ImportError:
    DATEUTIL_AVAILABLE = False
    print("⚠️ python-dateutil not installed. Date parsing will be basic.")

# Check OCR libraries availability
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("⚠️ EasyOCR not installed. Install with: pip install easyocr")

try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False
    print("⚠️ PaddleOCR not installed. Install with: pip install paddleocr")

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# Check if transformers (for DistilBERT) is available
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers not installed. Install with: pip install transformers torch")

# Check if spaCy is available
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("⚠️ spaCy not installed. Install with: pip install spacy")

class PosterAnalysisPipeline:
    """
    AI Pipeline for analyzing event posters:
    1. OCR (PaddleOCR) - Extract text from image
    2. Text Cleaning
    3. Category Classification (DistilBERT)
    4. School Classification (DistilBERT)
    5. Named Entity Recognition (spaCy)
    """
    
    # Event categories
    CATEGORIES = [
        "Technical",
        "Workshop",
        "Cultural",
        "Sports",
        "Career",
        "Awareness",
        "Webinar"
    ]
    
    # Amity Schools
    SCHOOLS = [
        "Amity School of Engineering & Technology",
        "Amity School of Business",
        "Amity School of Communication",
        "Amity School of Computer Science",
        "Amity School of Architecture & Planning",
        "Amity School of Fine Arts",
        "Amity School of Law",
        "Amity School of Applied Sciences",
        "Amity School of Biotechnology",
        "Amity School of Hospitality",
        "Amity School of Liberal Arts",
        "Amity School of Design"
    ]
    
    def __init__(self, models_path: str = "./models"):
        """Initialize the AI pipeline"""
        self.models_path = models_path
        self.easyocr_reader = None
        self.paddle_ocr = None
        self.category_classifier = None
        self.school_classifier = None
        self.ner_model = None
        
        # Initialize components
        self._init_ocr()
        self._init_classifiers()
        self._init_ner()
    
    def _init_ocr(self):
        """Initialize OCR engines - EasyOCR (primary) and PaddleOCR (fallback)"""
        # Try EasyOCR first (more reliable and accurate)
        if EASYOCR_AVAILABLE:
            try:
                print("🔄 Initializing EasyOCR (downloading models on first run)...")
                self.easyocr_reader = easyocr.Reader(['en'], gpu=True)
                print("✅ EasyOCR initialized successfully!")
            except Exception as e:
                print(f"⚠️ EasyOCR GPU init failed, trying CPU: {e}")
                try:
                    self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
                    print("✅ EasyOCR initialized (CPU mode)")
                except Exception as e2:
                    print(f"❌ EasyOCR initialization failed: {e2}")
                    self.easyocr_reader = None
        
        # Initialize PaddleOCR as fallback
        if PADDLE_AVAILABLE:
            try:
                print("🔄 Initializing PaddleOCR as backup...")
                self.paddle_ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang='en',
                    show_log=False
                )
                print("✅ PaddleOCR initialized as backup")
            except Exception as e:
                print(f"⚠️ PaddleOCR initialization failed: {e}")
                self.paddle_ocr = None
        
        if not self.easyocr_reader and not self.paddle_ocr:
            print("❌ No OCR engines available!")
            print("   Install with: pip install easyocr")
    
    def _init_classifiers(self):
        """Initialize DistilBERT classifiers"""
        if TRANSFORMERS_AVAILABLE:
            try:
                # Try to load trained models or use zero-shot classification
                self.category_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
                self.school_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
                print("✅ Classifiers initialized (zero-shot)")
            except Exception as e:
                print(f"⚠️ Classifier initialization failed: {e}")
        else:
            print("⚠️ Classifiers not available - using rule-based")
    
    def _init_ner(self):
        """Initialize spaCy NER"""
        if SPACY_AVAILABLE:
            try:
                # Try to load trained model or use base model
                try:
                    self.ner_model = spacy.load("en_core_web_sm")
                except:
                    print("⚠️ spaCy model not found. Run: python -m spacy download en_core_web_sm")
                    self.ner_model = None
                
                if self.ner_model:
                    print("✅ NER model initialized")
            except Exception as e:
                print(f"⚠️ NER initialization failed: {e}")
        else:
            print("⚠️ NER not available - using rule-based")
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from poster image using OCR (tries EasyOCR first, then PaddleOCR)"""
        
        # Try EasyOCR first (more accurate)
        if self.easyocr_reader:
            try:
                print(f"🔍 Running EasyOCR on image: {image_path}")
                result = self.easyocr_reader.readtext(image_path)
                
                if not result:
                    print("⚠️ EasyOCR: No text detected")
                else:
                    # EasyOCR returns: [(bbox, text, confidence), ...]
                    text_lines = []
                    for detection in result:
                        text = detection[1]
                        confidence = detection[2]
                        if confidence > 0.3:  # Filter low confidence
                            text_lines.append(text)
                    
                    if text_lines:
                        raw_text = "\n".join(text_lines)
                        print(f"✅ EasyOCR extracted {len(text_lines)} lines")
                        print(f"📄 First 200 chars: {raw_text[:200]}...")
                        return raw_text
            except Exception as e:
                print(f"⚠️ EasyOCR failed: {e}")
                print("   Trying PaddleOCR...")
        
        # Try PaddleOCR as fallback
        if self.paddle_ocr:
            try:
                print(f"🔍 Running PaddleOCR on image: {image_path}")
                result = self.paddle_ocr.ocr(image_path, cls=True)
                
                if not result or not result[0]:
                    print("⚠️ PaddleOCR: No text detected")
                    return ""
                
                # Concatenate all text
                text_lines = []
                for line in result[0]:
                    if line and len(line) >= 2:
                        text_lines.append(line[1][0])
                
                if text_lines:
                    raw_text = "\n".join(text_lines)
                    print(f"✅ PaddleOCR extracted {len(text_lines)} lines")
                    print(f"📄 First 200 chars: {raw_text[:200]}...")
                    return raw_text
            except Exception as e:
                print(f"❌ PaddleOCR Error: {e}")
                import traceback
                traceback.print_exc()
        
        # If both failed
        print("❌ All OCR engines failed to extract text")
        print("   Possible issues:")
        print("   1. Image file is corrupted or invalid format")
        print("   2. Image has no readable text")
        print("   3. Text is too small or blurry")
        print("   4. OCR models not properly installed")
        return ""
    
    def _mock_ocr(self, image_path: str) -> str:
        """Mock OCR for testing without PaddleOCR"""
        return """
        TECH FEST 2026
        Amity School of Computer Science
        Innovation and Technology
        Date: March 15-16, 2026
        Time: 9:00 AM - 6:00 PM
        Venue: Main Auditorium Block-A
        Register by: March 10, 2026
        Contact: techfest@amity.edu
        Organized by: Student Council
        """
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\-:,.\/@]', '', text)
        return text.strip()
    
    def classify_category(self, text: str) -> Tuple[str, float]:
        """Classify event category"""
        if self.category_classifier:
            try:
                result = self.category_classifier(
                    text,
                    candidate_labels=self.CATEGORIES
                )
                return result['labels'][0], result['scores'][0]
            except Exception as e:
                print(f"Category classification error: {e}")
                return self._rule_based_category(text)
        else:
            return self._rule_based_category(text)
    
    def _rule_based_category(self, text: str) -> Tuple[str, float]:
        """Rule-based category classification"""
        text_lower = text.lower()
        
        # Keywords for each category
        keywords = {
            "Technical": ["hackathon", "coding", "tech", "programming", "ai", "ml", "software", "hardware"],
            "Workshop": ["workshop", "training", "seminar", "tutorial", "hands-on", "session"],
            "Cultural": ["cultural", "music", "dance", "drama", "fest", "performance", "art"],
            "Sports": ["sports", "tournament", "match", "athletic", "game", "competition"],
            "Career": ["career", "placement", "job", "internship", "recruitment", "interview"],
            "Awareness": ["awareness", "campaign", "social", "environment", "health", "safety"],
            "Webinar": ["webinar", "online", "virtual", "zoom", "meet", "session"]
        }
        
        scores = {}
        for category, words in keywords.items():
            score = sum(1 for word in words if word in text_lower)
            scores[category] = score
        
        if max(scores.values()) == 0:
            return "Technical", 0.5  # Default
        
        best_category = max(scores, key=scores.get)
        confidence = min(scores[best_category] / 10.0, 0.95)
        
        return best_category, confidence
    
    def classify_school(self, text: str) -> Tuple[str, float]:
        """Classify organizing school"""
        if self.school_classifier:
            try:
                result = self.school_classifier(
                    text,
                    candidate_labels=self.SCHOOLS
                )
                return result['labels'][0], result['scores'][0]
            except Exception as e:
                print(f"School classification error: {e}")
                return self._rule_based_school(text)
        else:
            return self._rule_based_school(text)
    
    def _rule_based_school(self, text: str) -> Tuple[str, float]:
        """Rule-based school classification"""
        text_lower = text.lower()
        
        # Check for school keywords
        school_keywords = {
            "Amity School of Engineering & Technology": ["engineering", "technology", "aset"],
            "Amity School of Business": ["business", "mba", "management", "asb"],
            "Amity School of Communication": ["communication", "media", "journalism", "asc"],
            "Amity School of Computer Science": ["computer science", "cs", "it", "ascs"],
            "Amity School of Architecture & Planning": ["architecture", "planning", "design"],
            "Amity School of Fine Arts": ["fine arts", "art", "painting"],
            "Amity School of Law": ["law", "legal", "judiciary"],
            "Amity School of Applied Sciences": ["applied sciences", "science", "physics", "chemistry"],
            "Amity School of Biotechnology": ["biotechnology", "bio", "genetics"],
            "Amity School of Hospitality": ["hospitality", "hotel", "tourism"],
            "Amity School of Liberal Arts": ["liberal arts", "humanities"],
            "Amity School of Design": ["design", "graphic", "ux", "ui"]
        }
        
        scores = {}
        for school, keywords in school_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[school] = score
        
        if max(scores.values()) == 0:
            return "Amity School of Engineering & Technology", 0.5  # Default
        
        best_school = max(scores, key=scores.get)
        confidence = min(scores[best_school] / 5.0, 0.95)
        
        return best_school, confidence
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities: DATE, TIME, LOCATION, ORG, DEADLINE"""
        entities = {
            "date": None,
            "time": None,
            "location": None,
            "organizer": None,
            "deadline": None
        }
        
        # Use spaCy NER if available
        if self.ner_model:
            doc = self.ner_model(text)
            
            for ent in doc.ents:
                if ent.label_ == "DATE" and not entities["date"]:
                    entities["date"] = ent.text
                elif ent.label_ == "TIME" and not entities["time"]:
                    entities["time"] = ent.text
                elif ent.label_ in ["GPE", "LOC", "FAC"] and not entities["location"]:
                    entities["location"] = ent.text
                elif ent.label_ == "ORG" and not entities["organizer"]:
                    entities["organizer"] = ent.text
        
        # Enhanced rule-based extraction
        entities.update(self._rule_based_entities(text))
        
        return entities
    
    def _rule_based_entities(self, text: str) -> Dict[str, Any]:
        """Enhanced rule-based entity extraction with better patterns"""
        entities = {}
        
        # Enhanced Date extraction patterns - more comprehensive
        date_patterns = [
            # "Date: March 15, 2026" or "On: March 15, 2026"
            r'(?:Date|On|Event Date):\s*([A-Za-z]+\s+\d{1,2}(?:-\d{1,2})?,?\s+\d{4})',
            # "15 March 2026" or "15-16 March 2026"
            r'(\d{1,2}(?:-\d{1,2})?\s+[A-Za-z]+\s+\d{4})',
            # "March 15-16, 2026"
            r'([A-Za-z]+\s+\d{1,2}(?:-\d{1,2})?,?\s+\d{4})',
            # "15/03/2026" or "15-03-2026"
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})',
            # "2026-03-15" ISO format
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities["date"] = self._normalize_date(match.group(1))
                break
        
        # Enhanced Time extraction - multiple formats
        time_patterns = [
            # "Time: 9:00 AM - 6:00 PM" or "At: 9:00 AM"
            r'(?:Time|At|Timing):\s*(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?(?:\s*-\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)?)',
            # "9:00 AM - 6:00 PM" standalone
            r'(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\s*-\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm))',
            # "09:00 - 18:00" 24-hour format
            r'(\d{2}:\d{2}\s*-\s*\d{2}:\d{2})',
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities["time"] = match.group(1).strip()
                break
        
        # Enhanced Location extraction
        location_patterns = [
            # "Venue: Main Auditorium Block-A"
            r'(?:Venue|Location|Place|Venue:):\s*([A-Za-z0-9\s,\-&()]+?)(?:\n|Date|Time|Register|Contact|Organized|$)',
            # "@ Main Auditorium" or "@ Block A"
            r'@\s*([A-Za-z0-9\s,\-&()]+?)(?:\n|Date|Time|$)',
            # "Hall 1, Block A" or similar patterns
            r'(?:Hall|Room|Auditorium|Block|Building)\s+[A-Za-z0-9\-]+[^.!?\n]*',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1) if match.lastindex else match.group(0)
                entities["location"] = location.strip()
                break
        
        # Enhanced Organizer extraction
        org_patterns = [
            r'(?:Organized|Organised|Organized by|Organised by):\s*([A-Za-z0-9\s,&\-()]+?)(?:\n|Contact|Date|$)',
            r'(?:By|Presented by):\s*([A-Za-z0-9\s,&\-()]+?)(?:\n|Contact|Date|$)',
        ]
        
        for pattern in org_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities["organizer"] = match.group(1).strip()
                break
        
        # Enhanced Deadline/Registration extraction
        deadline_patterns = [
            r'(?:Register|Registration|Registration by|Register by|Deadline):\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4})',
            r'(?:Register|Registration|Registration by|Register by|Deadline):\s*(\d{1,2}[-/]\d{1,2}[-/]\d{4})',
            r'(?:Last date|Last Date):\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4}|\d{1,2}[-/]\d{1,2}[-/]\d{4})',
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                entities["deadline"] = self._normalize_date(match.group(1))
                break
        
        # Extract contact email
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        match = re.search(email_pattern, text)
        if match:
            entities["email"] = match.group(1)
        
        # Extract phone number
        phone_pattern = r'(?:Contact|Ph|Phone|Call):\s*([\d\s\-+()]{10,})'
        match = re.search(phone_pattern, text, re.IGNORECASE)
        if match:
            entities["phone"] = match.group(1).strip()
        
        return entities
    
    def _normalize_date(self, date_str: str) -> str:
        """Normalize date to ISO format (YYYY-MM-DD) for frontend compatibility"""
        if DATEUTIL_AVAILABLE:
            try:
                parsed_date = date_parser.parse(date_str, fuzzy=True)
                return parsed_date.strftime('%Y-%m-%d')
            except:
                pass
        
        # Basic normalization without dateutil
        try:
            # Try to handle common formats manually
            # Format: "15 March 2026" or "March 15, 2026"
            months = {
                'january': '01', 'february': '02', 'march': '03', 'april': '04',
                'may': '05', 'june': '06', 'july': '07', 'august': '08',
                'september': '09', 'october': '10', 'november': '11', 'december': '12',
                'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
            }
            
            date_lower = date_str.lower().strip()
            
            # Try DD/MM/YYYY or MM/DD/YYYY
            if '/' in date_str or '-' in date_str:
                parts = re.split(r'[-/]', date_str)
                if len(parts) == 3:
                    day, month, year = parts
                    if len(year) == 4:
                        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            
            # Try month name format
            for month_name, month_num in months.items():
                if month_name in date_lower:
                    # Extract day and year
                    numbers = re.findall(r'\d+', date_str)
                    if len(numbers) >= 2:
                        day = numbers[0]
                        year = numbers[-1]
                        if len(year) == 4:
                            return f"{year}-{month_num}-{day.zfill(2)}"
        except:
            pass
        
        # If all parsing fails, return original
        return date_str
    
    def analyze_poster(self, image_path: str) -> Dict[str, Any]:
        """
        Complete poster analysis pipeline
        Returns structured JSON with extracted event data
        """
        print("="*80)
        print("🔍 Starting poster analysis for:", image_path)
        print("="*80)
        
        # Step 1: OCR
        print("📝 Step 1: Extracting text from image...")
        raw_text = self.extract_text_from_image(image_path)
        
        if not raw_text or len(raw_text.strip()) < 10:
            error_msg = "Could not extract sufficient text from image. Please ensure:"
            error_msg += "\n  1. Image is clear and readable"
            error_msg += "\n  2. Text is in English"
            error_msg += "\n  3. Image format is supported (JPG, PNG)"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "rawText": raw_text,
                "extractedData": {}
            }
        
        # Step 2: Clean text
        cleaned_text = self.clean_text(raw_text)
        
        # Step 3: Classify category
        print("🏷️ Classifying category...")
        category, category_confidence = self.classify_category(cleaned_text)
        
        # Step 4: Classify school
        print("🏫 Identifying school...")
        school, school_confidence = self.classify_school(cleaned_text)
        
        # Step 5: Extract entities
        print("🎯 Extracting entities...")
        entities = self.extract_entities(cleaned_text)
        
        # Step 6: Extract title
        title = self._extract_title(cleaned_text)
        
        # Step 7: Generate description
        description = self._generate_description(cleaned_text, entities)
        
        # Calculate field confidence scores
        field_confidence = {
            "title": 0.9 if len(title) > 5 else 0.5,
            "date": 0.9 if entities.get("date") else 0.0,
            "time": 0.9 if entities.get("time") else 0.0,
            "location": 0.85 if entities.get("location") else 0.0,
            "organizer": 0.8 if entities.get("organizer") else 0.0,
            "deadline": 0.85 if entities.get("deadline") else 0.0,
        }
        
        # Calculate overall confidence
        all_scores = [
            category_confidence,
            school_confidence,
            field_confidence["title"],
            field_confidence["date"],
            field_confidence["time"],
            field_confidence["location"]
        ]
        overall_confidence = sum(all_scores) / len(all_scores)
        
        # Compile results
        result = {
            "success": True,
            "extractedData": {
                "title": title,
                "category": category,
                "school": school,
                "date": entities.get("date", ""),
                "time": entities.get("time", ""),
                "location": entities.get("location", ""),
                "organizer": entities.get("organizer", ""),
                "registrationDeadline": entities.get("deadline", ""),
                "description": description,
                "email": entities.get("email", ""),
                "phone": entities.get("phone", "")
            },
            "confidence": {
                "category": round(category_confidence, 2),
                "school": round(school_confidence, 2),
                "fields": field_confidence,
                "overall": round(overall_confidence, 2)
            },
            "rawText": raw_text,
            "needsReview": overall_confidence < 0.7,
            "suggestions": self._generate_suggestions(field_confidence)
        }
        
        print("✅ Analysis complete!")
        return result
    
    def _generate_suggestions(self, field_confidence: Dict[str, float]) -> List[str]:
        """Generate suggestions for fields that need review"""
        suggestions = []
        low_confidence_fields = [
            field for field, conf in field_confidence.items() if conf < 0.7
        ]
        
        if low_confidence_fields:
            suggestions.append(f"Please review: {', '.join(low_confidence_fields)}")
        
        return suggestions
    
    def _extract_title(self, text: str) -> str:
        """Extract event title with enhanced detection"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return "Untitled Event"
        
        # Title is usually:
        # 1. First prominent line (not a label)
        # 2. Longest line in first few lines
        # 3. Contains event-related keywords
        
        # Skip common label words
        skip_words = ['date', 'time', 'venue', 'location', 'organized', 'contact', 'register']
        
        potential_titles = []
        for i, line in enumerate(lines[:5]):  # Check first 5 lines
            # Skip lines that are just labels
            if any(word in line.lower() for word in skip_words):
                continue
            # Title should be 5-100 chars
            if 5 <= len(line) <= 100:
                # Prefer lines with capital letters or multiple words
                score = len(line)
                if line.isupper() or line.istitle():
                    score += 50
                potential_titles.append((score, line))
        
        if potential_titles:
            # Return highest scored title
            potential_titles.sort(reverse=True)
            return potential_titles[0][1]
        
        # Fallback to first line
        return lines[0] if lines[0] and len(lines[0]) < 100 else "Untitled Event"
    
    def _generate_description(self, text: str, entities: Dict[str, Any]) -> str:
        """Generate a better description from extracted text"""
        # Remove redundant information that's already captured
        cleaned = text
        
        # Remove date, time, venue patterns as they're in separate fields
        patterns_to_remove = [
            r'(?:Date|On):\s*[^\n]+',
            r'(?:Time|At|Timing):\s*[^\n]+',
            r'(?:Venue|Location|Place):\s*[^\n]+',
            r'(?:Register|Registration):\s*[^\n]+',
            r'(?:Contact):\s*[^\n]+',
        ]
        
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Take first 300 chars as description
        if len(cleaned) > 300:
            cleaned = cleaned[:297] + "..."
        
        return cleaned if cleaned else "No description available"


# Singleton instance
_pipeline_instance = None

def get_analysis_pipeline() -> PosterAnalysisPipeline:
    """Get or create singleton pipeline instance"""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = PosterAnalysisPipeline()
    return _pipeline_instance


if __name__ == "__main__":
    # Test the pipeline
    pipeline = get_analysis_pipeline()
    
    # Mock test
    result = pipeline.analyze_poster("mock_poster.jpg")
    print(json.dumps(result, indent=2))
