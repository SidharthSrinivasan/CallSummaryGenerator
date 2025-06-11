import json
from datetime import datetime
from word_writer import write_summary_to_word
from summarizer import load_summarizer, summarize_transcript
import torch

# Ensure CUDA GPU is available for model acceleration
if not torch.cuda.is_available():
    raise RuntimeError("CUDA GPU is not available. Please set up your GPU and CUDA before running this script.")

# Load the LLM summarizer pipeline
summarizer = load_summarizer()

# Read the transcript from a file (default: sample_transcript.txt)
transcript_file = "sample_transcript.txt"  # Change this to use a different file
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

except json.JSONDecodeError as e:
    # Handle JSON parsing errors from the model output
    raise RuntimeError(f"Could not parse model response as JSON.\nError: {e}")
