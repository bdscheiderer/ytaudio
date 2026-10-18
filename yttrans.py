from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    ''' Extract YouTube video ID from URL '''

    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_transcript(video_id):
    ''' Get transcript using Youtube API '''
    try:

        # Initialize api object and fetch transcript
        # English version is default
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)

        # strip out new lines unless after end of sentence
        cleanedup_transcript = cleanup_transcript(transcript)
        return cleanedup_transcript

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def cleanup_transcript(transcript):
    ''' Make transcript more readable by stripping out most
        newlines except after end of sentence (. ? !)
        Grok (Xai) helped with this function!
    '''

    try:

        # Combine transcript entries into sentences
        sentence_ends = {'.', '?', '!'}  # Sentence-ending punctuation
        current_sentence = []
        transcript_text = []

        for snippet in transcript:
            # .text is string "like" method in yt api object
            # Grok did not get this right, wanted to use snippet['text']
            line = snippet.text  
            if line:  # Skip empty entries
                current_sentence.append(line)
                # Check if the text ends with sentence-ending punctuation
                if line and line[-1] in sentence_ends:
                    # Join the current sentence and add to transcript
                    transcript_text.append(' '.join(current_sentence))
                    current_sentence = []  # Reset for next sentence
        
        # Append any remaining text as the last sentence
        if current_sentence:
            transcript_text.append(' '.join(current_sentence))

        return transcript_text

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def save_transcript(transcript, video_id):
    ''' Save transcript to text file using video_id as filename '''

    # Define output file name
    output_file = video_id + "_transcript.txt"  # default

    try:
        # Write transcript to file
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(f"{entry}\n") # entry, not entry.text here
        
        print(f"Transcript successfully saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Get YouTube URL from user
    video_url = input("Enter YouTube video URL: ")

    # Extract video id
    video_id = get_video_id(video_url)
    
    # Get and save transcript
    transcript = get_transcript(video_id)

    # Save transcript to text file
    save_transcript(transcript, video_id)

if __name__ == "__main__":
    main()