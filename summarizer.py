import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import google.generativeai as genai

key = 'AIzaSyAyeUgy3N73CWVXJyy0PVTb9DQJtk5lqmc'	#DO NOT EXPORT

def main():
	rex = re.compile("(?<=v=).+?((?=&)|$)")		#Basic regex ID finder; needs support for youtu.be links
	vID = rex.search(sys.argv[1]).group(0)
	#print('Video ID: ' + vID)

	baseTranscript = YouTubeTranscriptApi.get_transcript(vID)
	txtFormatter = TextFormatter()
	textTranscript = txtFormatter.format_transcript(baseTranscript)

	promptTail = '''
---
Please summarize the video transcript provided above.
Identify the topics introduced in the video. The reader should be able to describe the key concepts, details, and significance of the topics being discussed.
---
'''
	payload = textTranscript + promptTail

	genai.configure(api_key = key)
	model = genai.GenerativeModel("gemini-1.5-flash")
	response = model.generate_content(payload)
	print(response.text)

if __name__ == '__main__':
	main()
