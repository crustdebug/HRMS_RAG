"""
Script to verify FAISS embeddings are properly loaded
"""
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("=" * 60)
print("CHECKING EMBEDDINGS AND FAISS INDEX")
print("=" * 60)

# Check if index files exist
index_path = "data/faiss_index_gemini_CO_gtelarge"
index_file = os.path.join(index_path, "index.faiss")
pkl_file = os.path.join(index_path, "index.pkl")

print(f"\n1. Checking index files in: {index_path}")
print(f"   - index.faiss exists: {os.path.exists(index_file)}")
if os.path.exists(index_file):
    size_mb = os.path.getsize(index_file) / (1024 * 1024)
    print(f"     Size: {size_mb:.2f} MB")

print(f"   - index.pkl exists: {os.path.exists(pkl_file)}")
if os.path.exists(pkl_file):
    size_kb = os.path.getsize(pkl_file) / 1024
    print(f"     Size: {size_kb:.2f} KB")

# Check embedding model
print("\n2. Loading embedding model...")
try:
    embedding = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        encode_kwargs={"normalize_embeddings": True}
    )
    print("   ✓ Embedding model loaded successfully")
    print(f"   Model: thenlper/gte-large")
    
    # Test embedding
    test_text = "What is the leave policy?"
    test_embedding = embedding.embed_query(test_text)
    print(f"   ✓ Test embedding created")
    print(f"   Embedding dimension: {len(test_embedding)}")
    
except Exception as e:
    print(f"   ✗ Error loading embedding model: {e}")
    exit(1)

# Load FAISS index
print("\n3. Loading FAISS index...")
try:
    db = FAISS.load_local(
        index_path,
        embedding,
        allow_dangerous_deserialization=True
    )
    print("   ✓ FAISS index loaded successfully")
    
    # Get index stats
    print(f"   Number of vectors in index: {db.index.ntotal}")
    
except Exception as e:
    print(f"   ✗ Error loading FAISS index: {e}")
    exit(1)

# Test retrieval
print("\n4. Testing document retrieval...")
try:
    test_query = "What is the leave policy?"
    results = db.similarity_search(test_query, k=3)
    
    print(f"   ✓ Retrieved {len(results)} documents")
    print("\n   Sample results:")
    for i, doc in enumerate(results, 1):
        content_preview = doc.page_content[:150].replace('\n', ' ')
        print(f"\n   Document {i}:")
        print(f"   {content_preview}...")
        if doc.metadata:
            print(f"   Metadata: {doc.metadata}")
    
except Exception as e:
    print(f"   ✗ Error during retrieval: {e}")
    exit(1)

print("\n" + "=" * 60)
print("EMBEDDINGS CHECK COMPLETE!")
print("=" * 60)
print("\nSummary:")
print(f"  - Embedding model: thenlper/gte-large")
print(f"  - Embedding dimension: {len(test_embedding)}")
print(f"  - Total documents indexed: {db.index.ntotal}")
print(f"  - Index location: {index_path}")
print("\nYour embeddings are properly configured! ✓")
