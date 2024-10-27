import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def primary (URL, apiKeyGlobal, userTopic):  #This is the first function for working with the AI. It takes in a youtube video's URL and provides a summary for use later.
    #Example usage: primary("https://www.youtube.com/watch?v=BY5qBsmWEa8", "aeiou", "Cryptographic Hashing")
    #1. Extract the video ID from the provided URL
    rex = re.compile("((?<=v=)|(?<=be/)).+?((?=[&?]|$))")   #regex string for youtube.com and youtu.be links
    match = rex.search(URL)
    if(match):
        vID = match.group(0)
        #print("Video ID: " + vID)
    else:
        print("Could not find a valid Video ID...")
        return(-1)    
    
    #2. Get the transcript from the video using YouTubeTranscriptApi
    baseTranscript = YouTubeTranscriptApi.get_transcript(vID)   #Gets the basic dictionary form of the transcript. Contains timestamps and other unnecessary formatting
    txtFormatter = TextFormatter()  #Reformats the transcript object into plaintext.
    textTranscript = txtFormatter.format_transcript(baseTranscript)
    
    #3. Sending the prompt to gemini API
    promptTail = f"""
---
Please summarize the video transcript on {userTopic} provided above.
Identify the topics introduced in the video. Also, identify the essence of the key concepts the lecturer talks about, how it works, the significance, and the role in nature/world of the topics being discussed.
---
"""

    payload = textTranscript + promptTail
    genai.configure(api_key = apiKeyGlobal)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(payload)
    return(response.text)
    
def checkAnswers(apiKeyGlobal, summary, useranswer1, useranswer2, useranswer3): #This is the second function used once the user has recorded their responses to the three questions
    #Example uage: checkAnswers("aeiou", "The video can be summarized as follows...", "My answer to the first question", "My answer to the second question", "My answer to the third question")
    userUnderstanding = f"""**1. Please talk about what today's topic was all about in brief**
    {useranswer1}
**2. How does it work? Please include technicalities!**
    {useranswer2}
**3. How is it significant?**
    {useranswer3}
"""

    #Puts together the previously generated summary and 
    payload = f"""
The user's understanding of the topic can be understood by the following explanation given by them in three parts:
{userUnderstanding}
Now compare this response to the ideal summary:
{summary}
If the user's transcription is missing out any core essence of the lecturer's talk, significance, and technicalities when comparing it with the ideal summary, please mention it in the feedback as to what they missed out.
While providing the feedback... keep it under 4 sentences, ratw their each sub-answer of the three questions on a scale of 1 to 5, start off with 'Feedback:'
"""

    genai.configure(api_key = apiKeyGlobal)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(payload)

    feedback_word = "Feedback:" #Is this necessary, or can we just pipe the entire response back in? Also, how to do scoring?
    start_index = response.text.find(feedback_word)
    
    if start_index != -1:
        # Extract from "Feedback:" to the end
        feedback = response.text[start_index:]
    else:
        feedback = ''
    
    return(feedback.strip())

#Test Framework
#def main():
#    video_summary = primary("https://www.youtube.com/watch?v=BY5qBsmWEa8", "APIKEY", "Cryptographic Hashing")
    #print(video_summary)
#    urs1 = "Cryptographic hashing is a technique used to turn a given input into a fixed length value. The message can be either shorter or longer than the hash, but all inputs will produce the same length hash value. This makes it possible to demonstrate knowledge of the input without disclosing its true value."
#    urs2 = "In order to produce a hash from an input, an algorith like SHA-256 is used to perform a series of mathematical operations on it. Important properties for these hashing are that it should be extremely difficult to trace a hash back to its input, and that small changes in the content should still cause significant changes in the hash value."
#    urs3 = "Like I described before, hashing is useful for different things in cybersecurity. For passwords, due to the asymmetric relationship between the password and its hash, the hash can be saved or leaked without revealing the original password used."
#    evaluation = checkAnswers("APIKEY", video_summary, urs1, urs2, urs3)
#    print(evaluation)
    
#if __name__ == '__main__':
#	main()
