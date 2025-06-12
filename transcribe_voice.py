import whisper
import sys
import os

def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """
    Transcribe an audio file to text using OpenAI Whisper.
    Args:
        audio_path: Path to the audio file (wav, mp3, m4a, etc.).
        model_size: Whisper model size (tiny, base, small, medium, large).
    Returns:
        The transcribed text.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe_voice.py <audio_file> [model_size]")
        sys.exit(1)
    audio_file = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    print(f"Transcribing {audio_file} using Whisper model '{model_size}'...")
    transcript = transcribe_audio(audio_file, model_size)
    print("\nTranscription:\n")
    print(transcript)
    # Optionally, save to a file
    with open("sample_transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)
    print("\nTranscript saved to sample_transcript.txt")
