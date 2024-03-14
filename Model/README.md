# Quad Music Transformer Original Pre-Trained Model

***

## This is the original (non-optimized) Quad Music Transformer pre-trained model with its respective generator code/colabs
## For optimized Quad Music Transformer pre-trained model please see [Optimized](https://github.com/asigalov61/Quad-Music-Transformer/tree/main/Model/Optimized) dir above

***

## Original pre-trained model is hosted on [Hugging Face](https://huggingface.co/asigalov61/Quad-Music-Transformer)

***

### Model training corpus is [Monster MIDI Dataset Sample Search Results](https://huggingface.co/datasets/projectlosangeles/Monster-MIDI-Dataset/blob/main/Monster_MIDI_Dataset_Search_Results_Ver_1_0_CC_BY_NC_SA.zip)

### This training corpus consists of 90k select MIDIs from [Monster MIDI Dataset](https://github.com/asigalov61/Monster-MIDI-Dataset)

### Training corpus was augmented x6 times (x2 by time and x3 by pitch), which resulted in ~540k training samples of 8k length

### Model was trained on the resulting augmented training corpus for 41 hours(1 full epoch) @ 4 batches on a single H100 GPU

***

## Original Version

[![Open In Colab][colab-badge]][colab-notebook1]

[colab-notebook1]: <https://colab.research.google.com/github/asigalov61/Quad-Music-Transformer/blob/main/Model/Quad_Music_Transformer.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

### Features demonstration

***

## Composer Version

[![Open In Colab][colab-badge]][colab-notebook2]

[colab-notebook2]: <https://colab.research.google.com/github/asigalov61/Quad-Music-Transformer/blob/main/Model/Quad_Music_Transformer_Composer.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

### MuseNet-style workflow for endless supervised continuation generation

***

## Bulk Generator Version

[![Open In Colab][colab-badge]][colab-notebook3]

[colab-notebook3]: <https://colab.research.google.com/github/asigalov61/Quad-Music-Transformer/blob/main/Model/Quad_Music_Transformer_Bulk_Generator.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

### Bulk improvs and continuations generation

***

### Project Los Angeles
### Tegridy Code 2024
