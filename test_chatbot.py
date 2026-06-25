import json
import urllib.request
import urllib.error
import time

questions = [
    # 1. Semantic/Vague Match (Couple/Romantic)
    "I want to go somewhere with beaches and ocean views with my partner.",
    # 2. LLM Reasoning/Filtering (Budget)
    "Suggest honeymoon packages under 20000.",
    # 3. Exact Keyword Match (Adventure/Specifics)
    "Do you have any trips to Ladakh specifically for 7 days?",
    # 4. Family Packages (General/Family)
    "I'm travelling with my kids. What are your best family packages?",
    # 5. Spiritual/Pilgrimage
    "My parents want to go on a spiritual journey in South India or Kashi. What do you recommend?",
    # 6. Wildlife/Safari
    "I love nature and want to see tigers. Are there any wildlife safari tours?",
    # 7. Luxury/Premium
    "What is your most luxurious and premium tour package in Rajasthan?",
    # 8. Weekend Getaways
    "I just need a short 2 or 3 day weekend escape near Maharashtra or Ooty.",
    # 9. Company Trust/Reviews
    "Can you share some customer reviews or testimonials about Tripigo Tales?",
    # 10. Contact Info
    "How do I book a tour and what is your contact information?",
    # 11. Group/Friends Packages
    "Me and my college friends are looking for a group trip to Goa or Kasol. Any group discounts?",
    # 12. Regional Specialties (North-East/Kerala)
    "Do you have any cultural or scenic tours in Kerala or North-East India?",
    # 13. Travel Seasons/Weather
    "What are the best destinations to visit during December and January in India?",
    # 14. Customization/Bespoke Itineraries
    "Can I customize a travel itinerary if I want to add an extra day to a standard package?",
    # 15. Policies (Cancellation/Payment)
    "What are your policies on cancellation and how do I make the payment?"
]

output_file = "test_results.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("Tripigo Chatbot Test Results\n")
    f.write("============================\n\n")

    for q in questions:
        print(f"Asking: {q}")
        data = json.dumps({"message": q}).encode("utf-8")
        req = urllib.request.Request("http://localhost:8000/chat", data=data, headers={"Content-Type": "application/json"})
        
        f.write(f"Q: {q}\n")
        try:
            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                
                answer = res_json.get("answer", "")
                sources = res_json.get("sources", [])
                
                f.write(f"A: {answer}\n\n")
                if sources:
                    f.write("Sources:\n")
                    for src in sources:
                        f.write(f" - {src}\n")
                f.write("\n--------------------------------------------------\n\n")
                print(f"Answer received.")
        except Exception as e:
            print(f"Error for question '{q}': {e}")
            f.write(f"Error: {str(e)}\n\n--------------------------------------------------\n\n")
            
        # Add a 4-second delay to avoid hitting Gemini Free Tier rate limits (15 Requests Per Minute)
        print("Waiting 4 seconds to avoid rate limit...")
        time.sleep(4)

print(f"Testing complete! Results saved to {output_file}")
