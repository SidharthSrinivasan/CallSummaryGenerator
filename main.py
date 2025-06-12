import json
from datetime import datetime
from word_writer import write_summary_to_word
from summarizer import load_summarizer, summarize_transcript
import torch
import argparse
#from transcribe_voice import transcribe_audio
from db_utils import save_summary_to_db

# Ensure CUDA GPU is available for model acceleration
if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is not available. Please set up your GPU and CUDA before running this script.")

# Load the LLM summarizer pipeline
summarizer = load_summarizer()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Call Summary Generator")
group = parser.add_mutually_exclusive_group()
group.add_argument('--audio', type=str, help='Path to audio file to transcribe and summarize')
group.add_argument('--transcript', type=str, help='Path to transcript text file to summarize')
parser.add_argument('--whisper_model', type=str, default='base', help='Whisper model size (tiny, base, small, medium, large)')
args = parser.parse_args()

# Determine transcript source
# if args.audio:
#     print(f"Transcribing audio file: {args.audio} using Whisper model '{args.whisper_model}'...")
#     sample_transcript = transcribe_audio(args.audio, args.whisper_model)
#     print("Audio transcription complete.")
if args.transcript:
    transcript_file = args.transcript
    with open(transcript_file, "r", encoding="utf-8") as tf:
        sample_transcript = tf.read()
else:
    transcript_file = "sample_transcript.txt"
    with open(transcript_file, "r", encoding="utf-8") as tf:
        sample_transcript = tf.read()

try:
    # Generate summary data from the transcript using the LLM
    summary_data = summarize_transcript(summarizer, sample_transcript)

    # Write the summary data to a JSON text file
    with open("summary_output.txt", "w", encoding="utf-8") as out_f:
        json.dump(summary_data, out_f, indent=2)
    print("Summary data written to summary_output.txt")

    # Write the summary data to a Word document in full sentences
    write_summary_to_word(summary_data)
    print("Summary data written to summary_output.docx (Word document)")

    # Save the summary data to the database
    save_summary_to_db(summary_data)
    print("Summary data saved to the database.")

except json.JSONDecodeError as e:
    # Handle JSON parsing errors from the model output
    raise RuntimeError(f"Could not parse model response as JSON.\nError: {e}")
