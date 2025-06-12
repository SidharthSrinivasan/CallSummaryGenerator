# Call Summary Generator

A modular Python tool to transcribe call audio or summarize call transcripts using a local LLM (Mistral-7B-Instruct), with output as both structured JSON and a polished Word document.

---

## 🚀 Features
- **Audio Transcription:** Convert audio files to text using OpenAI Whisper (GPU-accelerated)
- **LLM Summarization:** Summarize transcripts with a local LLM (Hugging Face Transformers)
- **Multiple Outputs:** Get both JSON and Word (.docx) summaries
- **Modular Design:** Easy to extend and maintain
- **Command-Line Interface:** Flexible and user-friendly

---

## 🛠️ Requirements
- Python 3.8+
- CUDA-compatible GPU and drivers (for best performance)
- Install dependencies:
  ```powershell
  pip install torch transformers python-docx openai-whisper
  ```

---

## 💡 Usage

### Summarize a Transcript File
```powershell
python main.py --transcript path/to/transcript.txt
```

### Transcribe Audio and Summarize
```powershell
python main.py --audio path/to/audio.wav
```
- Optionally specify Whisper model size (default: base):
  ```powershell
  python main.py --audio path/to/audio.wav --whisper_model medium
  ```

### Default Behavior
If no arguments are provided, the script uses `sample_transcript.txt` in the project directory.

---

## 📦 Output
- `summary_output.txt` — JSON summary of the call
- `summary_output.docx` — Word document with a readable summary

---

## 📁 Project Structure
```
main.py              # Orchestrates workflow, handles CLI
summarizer.py        # LLM prompt building and summarization logic
word_writer.py       # Word document output logic
transcribe_voice.py  # Whisper-based audio transcription
sample_transcript.txt
summary_output.txt
summary_output.docx
```

---

## 🔧 Extending
- Add new output formats (PDF, HTML, etc.)
- Integrate with other LLMs or ASR models
- Build a web or desktop UI

---

## 🐞 Troubleshooting
- Ensure your GPU and CUDA drivers are set up if you see CUDA errors
- If you get permission errors, close output files in other programs before running
- For best Whisper accuracy, use the largest model your GPU can handle

---

## 🤝 Contributing
Feel free to open issues or contribute improvements!

---

## 🗄️ Database Usage
This project uses **PostgreSQL** to store call summaries. The table schema is defined in `schema_migration.py`.

### 1. Set Up the Database
- Ensure PostgreSQL is installed and running.
- Create a database named `call_summaries` (or update the name in `schema_migration.py`).
- Set the environment variable `PGPASSWORD` to your PostgreSQL password:
  
  ```powershell
  $env:PGPASSWORD = "your_postgres_password"
  ```

### 2. Run the Schema Migration
To create the required table, run:

```powershell
python schema_migration.py
```

### 3. Check the Database Contents
You can view the saved summaries using the `psql` command-line tool:

```powershell
psql -U postgres -d call_summaries -h localhost -c "SELECT * FROM call_summaries;"
```

Or use a GUI tool like **pgAdmin**.

---

## ⚙️ Installation
Install all dependencies with:

```powershell
pip install -r requirements.txt
```