from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/webhook")
def webhook_get():
    """GET endpoint for OMI setup completion check"""
    return {"is_setup_completed": True}

@app.post("/webhook")
async def webhook(request: Request, session_id: str = None, uid: str = None):
    # Get the request body (transcript segments array)
    transcript_segments = await request.json()
    print(f"Session ID: {session_id}, UID: {uid}")
    print(f"Transcript segments: {transcript_segments}")

    # Hint: The transcript contains segments with text data
    # Hint: Access the latest segment with transcript_segments[-1]["text"]
    # Hint: Return a dictionary with a "message" key and the value being the notification message

    # Task: Implement keyword detection and response logic of your choice
    # example: if the word "tired" is mentioned, return a message notifying the user to take a break

    try:
        print(f"Raw transcript_segments type: {type(transcript_segments)}")
        print(f"Raw transcript_segments content: {transcript_segments}")
        
        if transcript_segments and "segments" in transcript_segments and len(transcript_segments["segments"]) > 0:
            latest_segment = transcript_segments["segments"][-1]
            print(f"Latest segment: {latest_segment}")
            latest_text = latest_segment.get("text", "").lower()
            print(f"Processing text: '{latest_text}'")
            
            keywords_responses = {
                "tired": "You mentioned feeling tired. Consider taking a break to recharge!",
                "stressed": "I heard you mention stress. Try some deep breathing or a short walk.",
                "hungry": "Sounds like you're hungry! Don't forget to fuel your body with a healthy meal.",
                "sick": "I hope you feel better soon! Make sure to rest and stay hydrated.",
                "help": "I'm here to help! What do you need assistance with?",
                "meeting": "Meeting coming up? Make sure you're prepared and have your notes ready.",
                "deadline": "Deadline approaching? Break it down into smaller tasks to stay on track.",
                "exercise": "Great that you're thinking about exercise! Even a short walk can boost your energy.",
                "sleep": "Sleep is important for your health. Try to maintain a consistent sleep schedule.",
                "work": "Work can be demanding. Remember to take breaks and maintain work-life balance."
            }

            detected_keywords = []
            for keyword, response in keywords_responses.items():
                if keyword in latest_text:
                    detected_keywords.append(response)
                    print(f"Keyword '{keyword}' detected in: '{latest_text}'")
            
            # Return appropriate response
            if detected_keywords:
                return {"message": detected_keywords[0]}
            else:
                return {"message": "I'm listening and ready to help with anything you need!"}
        else:
            print("ERROR: No segments found")
            return {"message": "No transcript data received."}
            
    except Exception as e:
        print(f"Error processing transcript: {e}")
        import traceback
        traceback.print_exc()
        return {"message": "Error processing your message. Please try again."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
