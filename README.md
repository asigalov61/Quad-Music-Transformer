# Quad Music Transformer
## SOTA quality fast music transformer with symmetrical quad MIDI notes encoding

![Quad-Music-Transformer-Artwork (7)](https://github.com/asigalov61/Quad-Music-Transformer/assets/56325539/9d69c44f-1b35-44b0-b78d-84e53ec30e16)

***

## Original Version

[![Open In Colab][colab-badge]][colab-notebook1]

[colab-notebook1]: <https://colab.research.google.com/github/asigalov61/Quad-Music-Transformer/blob/main/Quad_Music_Transformer.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

### Features demonstration

***

## Composer Version

[![Open In Colab][colab-badge]][colab-notebook2]

[colab-notebook2]: <https://colab.research.google.com/github/asigalov61/Quad-Music-Transformer/blob/main/Quad_Music_Transformer_Composer.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

### MuseNet-style workflow for endless supervised continuation generation

***

## Bulk Generator Version

[![Open In Colab][colab-badge]][colab-notebook3]

[colab-notebook3]: <https://colab.research.google.com/github/asigalov61/Quad-Music-Transformer/blob/main/Quad_Music_Transformer_Bulk_Generator.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

### Bulk improvs and continuations generation

***

## Technical notes

### SOTA quality was achieved by using the following specific techniques:

### 1) Quality source MIDI dataset (quality over quantity)
### 2) MIDI dataset augmentation by time (x2) and pitches (x3)
### 3) Timings normalization, quantization and compression (128)
### 4) Larger model embed size (2048) with less layers (16) and heads (16)
### 5) Training longer since the MIDI dataset is small (2 full epochs)
### 6) Using MIDI instruments families (16) instead of full MIDI instruments range (128)
### 7) Using symmetrical quad MIDI notes encoding
### 8) 8k sequence length so that the model can learn long-term music scructure
### 9) Using fp16 precision so that the model is sufficiently fast with low memory footprint
### 10) Hex (16) MIDI velocity range to avoid velocity overfitting while preserving velocity details

***

### Project Los Angeles
### Tegridy Code 2024
