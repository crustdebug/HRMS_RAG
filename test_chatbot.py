"""
Test script for the HR Chatbot
Run this after starting the server to verify it's working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_chat(query, user_id="test_user_123"):
    """Send a test query to the chatbot"""
    url = f"{BASE_URL}/chat"
    payload = {
        "query": query,
        "user_id": user_id
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response")
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect to server. Make sure the server is running on port 8000"
    except Exception as e:
        return f"ERROR: {str(e)}"

def run_tests():
    """Run a series of test queries"""
    print("=" * 60)
    print("HR CHATBOT TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Hello", "Test 1: Greeting"),
        ("What is the leave policy?", "Test 2: HR Question"),
        ("How many sick leaves can I take?", "Test 3: Specific Policy Question"),
        ("asdfghjkl", "Test 4: Gibberish Detection"),
        ("Thank you", "Test 5: Acknowledgment"),
    ]
    
    for query, description in tests:
        print(f"\n{description}")
        print(f"Query: {query}")
        print("-" * 60)
        response = test_chat(query)
        print(f"Response: {response}")
        print("=" * 60)

if __name__ == "__main__":
    print("\nMake sure the server is running first:")
    print("  uvicorn app.main:app --reload --port 8000\n")
    
    input("Press Enter to start tests...")
    run_tests()
