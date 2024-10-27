import google.generativeai as genai
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


key = 'AIzaSyACzwr8pJFMl57dydB_1ENd_2pJowO1w4o'	#DO NOT EXPORT
userTopic = "To be mentioned by the user"

def main():
    idealSummary = ""
    if len(sys.argv) < 2:  # Check if the URL argument is provided
        print("Usage: python script_name.py <YouTube URL>")
        return

    rex = re.compile("(?<=v=).+?((?=&)|$)")  # Basic regex ID finder; needs support for youtu.be links
    match = rex.search(sys.argv[1])

    if match:
        vID = match.group(0)
        print(f"Video ID: {vID}")
        
        baseTranscript = YouTubeTranscriptApi.get_transcript(vID)
        txtFormatter = TextFormatter()
        textTranscript = txtFormatter.format_transcript(baseTranscript)

        promptTail = '''
---
Please summarize the video transcript provided above.
Identify the topics introduced in the video. Also, identify the essence of the key concepts, details, the significance, and the role in nature/world of the topics being discussed.
---
'''
        payload = textTranscript + promptTail

        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        # The summary we use to compare with user's summary 
        response = model.generate_content(payload)
        idealSummary = response.text
    else:
        print("Invalid YouTube URL format! Please check the link and try again :/")
        
    """User is now questioned thrice where they need to talk the answer out each time. User's answers are transcribed accordingly and then fed into an answer pool,
    thus identifying the core points and loopholes in their understanding. We also calculate scores accordingly and announce an ultimate understanding score and a brief
    feedback as to what they need to revisit/ work on."""

    userResponse1 = "User's response for question 1"
    userResponse2 = "User's response for question 2"
    userResponse3 = "User's response for question 3"

    userUnderstanding = userResponse1 + userResponse2 + userResponse3

    promptBasedOnUserUnderstanding = f"""
The user's understanding of the topic can be understood by the following exact explanation given by them: {userUnderstanding}. 
Now compare this response to the ideal summary: {idealSummary}.
If the user's transcription is missing out any core essence of the key concepts, details, the significance, and the role in nature/world of the topics being discussed with respect to the other, briefly mention that in the form of a feedback.
While providing the feedback, start off with 'Feedback:'
"""
    # Generating response based on user understanding
    response = model.generate_content(promptBasedOnUserUnderstanding)
    
    # Extract everything from "Feedback:" onward
    feedback_word = "Feedback:"
    start_index = response.text.find(feedback_word)
    
    if start_index != -1:
        # Extract from "Feedback:" to the end
        feedback = response.text[start_index:]
        print("Feedback extracted:", feedback.strip())  # Clean up whitespace/newlines
    else:
        print("No feedback found in the response.")

if __name__ == '__main__':
    main()
