"""
Direct OCR Test Script
Tests PaddleOCR directly on your poster image
"""
import sys
import os

# Test PaddleOCR
print("="*80)
print("Testing PaddleOCR Installation")
print("="*80)

try:
    from paddleocr import PaddleOCR
    print("✅ PaddleOCR imported successfully")
except ImportError as e:
    print(f"❌ PaddleOCR import failed: {e}")
    sys.exit(1)

# Initialize OCR
print("\n🔄 Initializing PaddleOCR...")
try:
    ocr = PaddleOCR(
        use_angle_cls=True,
        lang='en',
        show_log=False,
        det_db_thresh=0.3,  # Lower detection threshold
        det_db_box_thresh=0.5,  # Lower box threshold  
        use_gpu=True,  # Try GPU first
        rec_batch_num=6
    )
    print("✅ PaddleOCR initialized")
except Exception as e:
    print(f"⚠️ GPU init failed, trying CPU: {e}")
    ocr = PaddleOCR(
        use_angle_cls=True,
        lang='en',
        show_log=False,
        det_db_thresh=0.3,
        det_db_box_thresh=0.5,
        use_gpu=False
    )
    print("✅ PaddleOCR initialized (CPU mode)")

# Test with sample text
print("\n" + "="*80)
print("READY TO TEST IMAGE")
print("="*80)
print("\nUsage:")
print("  python test_ocr_direct.py <image_path>")
print("\nExample:")
print("  python test_ocr_direct.py poster.jpg")

if len(sys.argv) > 1:
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"\n❌ Image not found: {image_path}")
        sys.exit(1)
    
    print(f"\n🔍 Running OCR on: {image_path}")
    print("-"*80)
    
    try:
        result = ocr.ocr(image_path, cls=True)
        
        if not result or not result[0]:
            print("⚠️ No text detected in image!")
            print("\nPossible issues:")
            print("  1. Image is too low resolution")
            print("  2. Text is too small or blurry")
            print("  3. Unusual fonts or colors")
            print("  4. Image format issue")
        else:
            print(f"✅ Detected {len(result[0])} text regions\n")
            print("="*80)
            print("EXTRACTED TEXT:")
            print("="*80)
            
            full_text = []
            for idx, line in enumerate(result[0], 1):
                bbox = line[0]
                text = line[1][0]
                confidence = line[1][1]
                
                full_text.append(text)
                print(f"{idx}. [{confidence:.2f}] {text}")
            
            print("\n" + "="*80)
            print("FULL TEXT (combined):")
            print("="*80)
            print("\n".join(full_text))
            
            print("\n" + "="*80)
            print(f"Total lines: {len(full_text)}")
            print(f"Total characters: {len(''.join(full_text))}")
            print("="*80)
            
    except Exception as e:
        print(f"❌ OCR Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n💡 Provide an image path to test OCR extraction")
    print(f"\nExample: python {sys.argv[0]} path/to/poster.jpg")
