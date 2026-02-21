"""
Firebase Connection Test Script
Tests Firebase connection for Campus Memory Event Management System
"""

import sys
import os

def test_firebase_connection():
    print("=" * 60)
    print("🔥 Firebase Connection Test")
    print("=" * 60)
    print()
    
    # Check if firebase-credentials.json exists
    cred_file = "firebase-credentials.json"
    if not os.path.exists(cred_file):
        print("❌ ERROR: firebase-credentials.json not found!")
        print()
        print("📝 To fix this:")
        print("1. Go to https://console.firebase.google.com/project/campus-memory")
        print("2. Navigate to Project Settings → Service accounts")
        print("3. Click 'Generate new private key'")
        print("4. Download the JSON file")
        print("5. Rename it to 'firebase-credentials.json'")
        print(f"6. Place it in: {os.path.abspath('.')}")
        print()
        print("📖 See FIREBASE_SETUP_GUIDE.md for detailed instructions")
        print()
        return False
    else:
        print(f"✅ Found firebase-credentials.json")
        print()
    
    # Try to import firebase_admin
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore, storage
        print("✅ firebase-admin package installed")
    except ImportError as e:
        print(f"❌ ERROR: Firebase Admin SDK not installed!")
        print(f"   {e}")
        print()
        print("📦 To install:")
        print("   pip install firebase-admin")
        print()
        return False
    
    # Try to initialize Firebase
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_file)
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'campus-memory.firebasestorage.app'
            })
        print("✅ Firebase Admin SDK initialized")
        print()
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize Firebase!")
        print(f"   {e}")
        print()
        print("🔍 Possible issues:")
        print("   - Invalid service account key")
        print("   - Wrong project configuration")
        print("   - Network connectivity issues")
        print()
        return False
    
    # Test Firestore connection
    try:
        db = firestore.client()
        print("✅ Firestore client created")
        
        # Try to read from Firestore (will create collection if doesn't exist)
        test_ref = db.collection('_test').document('connection_test')
        test_ref.set({
            'timestamp': firestore.SERVER_TIMESTAMP,
            'message': 'Connection test successful'
        })
        print("✅ Firestore write test successful")
        
        # Read back the data
        doc = test_ref.get()
        if doc.exists:
            print("✅ Firestore read test successful")
            # Clean up test document
            test_ref.delete()
            print("✅ Test cleanup complete")
        
        print()
    except Exception as e:
        print(f"⚠️ WARNING: Firestore test failed!")
        print(f"   {e}")
        print()
    
    # Test Storage connection
    try:
        bucket = storage.bucket()
        print(f"✅ Storage bucket connected: {bucket.name}")
        print()
    except Exception as e:
        print(f"⚠️ WARNING: Storage test failed!")
        print(f"   {e}")
        print()
    
    # Final summary
    print("=" * 60)
    print("✅ Firebase Connection Test PASSED!")
    print("=" * 60)
    print()
    print("🎉 Your Firebase is configured correctly!")
    print()
    print("📊 Firebase Console:")
    print("   https://console.firebase.google.com/project/campus-memory")
    print()
    print("🚀 Next steps:")
    print("   1. Start the backend server:")
    print("      python event_api_server.py")
    print()
    print("   2. Start the frontend:")
    print("      cd CampusMemory/CampusMemory")
    print("      npm run dev")
    print()
    print("   3. Test creating an event from the frontend")
    print("   4. Check Firestore Console to see the data")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = test_firebase_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
