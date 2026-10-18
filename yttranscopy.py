from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    """Extract YouTube video ID from URL."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript(video_url, output_file="transcript.txt"):

    try:
        # Extract video ID from URL
        video_id = get_video_id(video_url)



        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)

        for snippet in fetched_transcript:
            print(snippet.text)

        
        # Get transcript list and find the English transcript (or fallback to others)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])  # Prefer English, can add more languages
        
        # Fetch the transcript data
        transcript_data = transcript.fetch()
        
        # Write transcript to file
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in transcript_data:
                f.write(f"{entry['text']}\n")
        
        print(f"Transcript successfully saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Get YouTube URL from user
    video_url = input("Enter YouTube video URL: ")
    
    # Define output file name
    output_file = "transcript.txt"
    
    # Get and save transcript
    get_transcript(video_url, output_file)

if __name__ == "__main__":
    main()