# Thonburian Whisper

[🤖 Model](https://huggingface.co/biodatlab/whisper-th-medium-combined) | [📔 Jupyter Notebook](https://github.com/biodatlab/whisper-th-demo/blob/main/whisper_th_demo.ipynb) | [🤗 Hugginface Space Demo](https://huggingface.co/spaces/biodatlab/whisper-thai-demo) | 📃 Blog in Thai (TBA)

<p align="center">
  <img src="assets/Thonburian-Whisper-1.jpg" width="700"/>
</p>

Thonburian Whisper is an Automatic Speech Recognition (ASR) in Thai fine-tuned using [Whisper](https://openai.com/blog/whisper/) model
originally from OpenAI. The model is released as a part of [Whisper fine-tuning event](https://github.com/huggingface/community-events/tree/main/whisper-fine-tuning-event) from Huggingface (December 2022). We trained the model using Commonvoice 11, [Gowajee corpus](https://github.com/ekapolc/gowajee_corpus), and [Thai Elderly Speech dataset](https://github.com/VISAI-DATAWOW/Thai-Elderly-Speech-dataset/releases/tag/v1.0.0).

## Usage

Use the model with [Hugginface's transformers](https://github.com/huggingface/transformers) as follows:

```py
import torch
from transformers import pipeline

MODEL_NAME = "biodatlab/whisper-th-medium-combined"
lang = "th"

device = 0 if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

pipe.model.config.forced_decoder_ids = pipe.tokenizer.get_decoder_prompt_ids(language=lang, task="transcribe")
pipe("audio.mp3", ignore_warning = True)["text"] # perform ASR with created pipe
```

## Requirements

Use `pip` to install the requirements as follows:

``` sh
!pip install git+https://github.com/huggingface/transformers
!pip install librosa
!sudo apt install ffmpeg
```

## Model performance

We measure word error rate (WER) of the model with [deepcut tokenizer](https://github.com/rkcosmos/deepcut) after punctuation removal and replaing maiyamok (ๆ) with the prior word.

| **Model**        | **Commonvoice 7** | **Commonvoice 11** |
|------------------|-------------------|--------------------|
| Whisper (medium) | 8.49              | 9.17               |


## Developers

- [Biomedical and Data Lab, Mahidol University](https://biodatlab.github.io/)
- [Looloo technology](https://loolootech.com/)
