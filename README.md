# State of the Art: Comparative Analysis of TTS & STT Technologies

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Unity-lightgrey.svg)
![Languages](https://img.shields.io/badge/languages-C%23%20%7C%20Python-yellow.svg)

## 📝 Overview

This repository presents a comprehensive analysis of current Text-to-Speech (TTS) and Speech-to-Text (STT) technologies in 2023-2024. The research compares cloud-based API solutions and local open-source models, with detailed metrics on:

- 💰 **Pricing structures & cost efficiency**
- 💻 **Computational requirements**
- ⏱️ **Latency performance**  
- 🔊 **Audio quality & accuracy**
- 🇪🇸 **Spanish language support**
- 🎮 **Unity integration compatibility**

## 📊 Technology Comparisons

### Text-to-Speech (TTS) Solutions

| **Service** | **Cost per 1M chars** | **Computational Requirements** | **Latency** | **Spanish Quality (1-10)** | **Implementation Complexity** |
|-------------|-------------------|---------------------------|------------|---------------------|--------------------------|
| **Google Cloud TTS** | $4 (std) / $16 (WaveNet) | Cloud-based | <100ms | 9 | Medium |
| **Amazon Polly** | $4 (std) / $16 (neural) | Cloud-based | <150ms | 8 | Low |
| **Azure Speech** | $16 (neural) | Cloud-based | <80ms | 9 | Low |
| **IBM Watson** | $20 | Cloud-based | <200ms | 7 | Medium |
| **ElevenLabs** | $180 | Cloud-based | 1-2s | 9.5 | Low |
| **Cartesiana** | Free: 20K Credits<br>Pro: $5/mo (100K Credits) | Cloud-based | - | - | Low |
| **Piper (offline)** | Free | CPU + 4GB VRAM | <50ms | 8 | High |
| **Coqui TTS (offline)** | Free | GPU recommended | 200-500ms | 7 | High |

## 💰 Free Tier Pricing Information

### Google Cloud TTS
- **Free tier:** 0 to 4 million characters
- **After free tier:** $0.000004 per character ($4 per 1 million characters) for Standard voices
- **SKU:** 9D01-5995-B545

### Cartesiana
- **Free Plan ($0/month):** 
  - 20K Credits
  - 2 Parallel Requests
  - Discord Support
  - 15 Languages
  - Infilling
  - No Commercial Use
  
- **Pro Plan ($5/month):**
  - 100K Credits
  - 3 Parallel Requests
  - Commercial Use
  - Instant Cloning
  - Voice Changer
  - Localization

### Speech-to-Text (STT) Solutions

| **Service** | **Cost per minute** | **Computational Requirements** | **Latency** | **Spanish Accuracy** | **Implementation Complexity** |
|-------------|-------------------|---------------------------|------------|---------------------|--------------------------|
| **Google Cloud STT** | $0.024 | Cloud-based | Real-time | 92-95% | Medium |
| **Amazon Transcribe** | $0.024 | Cloud-based | Near real-time | 90-92% | Low |
| **Azure Speech** | $0.016-0.02 | Cloud-based | Real-time | ~90% | Low |
| **IBM Watson** | $0.02 | Cloud-based | Near real-time | ~88% | Medium |
| **Whisper (local)** | Free | GPU 5-10GB VRAM | Batch processing | ~95% | High |
| **Vosk (offline)** | Free | CPU / 300MB RAM | Real-time | ~90% | Medium |

## 🚀 Getting Started

### Prerequisites

- Unity 2021.3 LTS or newer
- Python 3.8+
- For local models: GPU with appropriate VRAM (see requirements above)

### Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/state-of-art-tts-stt.git

# Set up Python environment
cd state-of-art-tts-stt

# On Windows:
python -m venv .venv
.venv\Scripts\activate

# On Unix/MacOS:
# python -m venv .venv
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📁 Project Structure

```
/
├── tts/                      # TTS implementation tests
│   ├── cloud/                # Cloud-based TTS services
│   │   ├── google_tts.py     # Google Cloud TTS implementation
│   │   ├── amazon_polly.py   # Amazon Polly implementation
│   │   └── ...
│   └── local/                # Self-hosted TTS models
│       ├── piper/            # Piper TTS implementation
│       └── coqui/            # Coqui TTS implementation
├── stt/                      # STT implementation tests
│   ├── cloud/                # Cloud-based STT services
│   └── local/                # Self-hosted STT models
├── unity/                    # Unity integration examples
├── evaluation/               # Test scripts and results
├── docs/                     # Documentation
└── README.md                 # This file
```

## 📊 Performance Testing

### Testing Methodology

All technologies were tested using:
1. **Standardized dataset** of Spanish text/audio samples
2. **Identical hardware** for local models
3. **Consistent metrics** for:
   - Processing time (ms)
   - Accuracy (WER for STT)
   - Voice quality ratings (for TTS)
   - Resource utilization

### Running Tests

```bash
# Run TTS benchmark tests
python evaluation/benchmark_tts.py

# Run STT benchmark tests
python evaluation/benchmark_stt.py

# Generate comparison report
python evaluation/generate_report.py
```

## 🔍 Key Findings

### TTS Insights
- **Cloud services:** ElevenLabs provides the highest quality but at premium pricing
- **Local models:** Piper offers excellent performance/quality balance for offline use
- **Cost-efficiency:** Amazon Polly standard voices offer the best value for basic needs

### STT Insights
- **Accuracy leader:** Whisper (local) and Google Cloud STT provide best Spanish transcription
- **Real-time needs:** Vosk is optimal for low-latency requirements
- **Enterprise scale:** Azure Speech offers the best pricing for high-volume transcription

## 🔮 Recommendations

### For Production Applications
- **High-quality voice needs:** ElevenLabs or Google WaveNet
- **Cost-sensitive production:** Amazon Polly or Azure Speech
- **Offline capabilities:** Piper (TTS) and Whisper (STT)

### For Unity Integration
- **Cloud integration:** Azure offers the simplest Unity SDK
- **Mobile applications:** Consider latency and bandwidth constraints
- **Desktop applications:** Local models may offer cost advantages at scale

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or feedback, please open an issue or contact [your-email@example.com].