# -*- coding: utf-8 -*-
"""Quad_Music_Transformer_Composer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/asigalov61/Quad-Music-Transformer/blob/main/Quad_Music_Transformer_Composer.ipynb

# Quad Music Transformer Composer (ver. 1.0)

***

Powered by tegridy-tools: https://github.com/asigalov61/tegridy-tools

***

WARNING: This complete implementation is a functioning model of the Artificial Intelligence. Please excercise great humility, care, and respect. https://www.nscai.gov/

***

#### Project Los Angeles

#### Tegridy Code 2024

***

# (GPU CHECK)
"""

#@title NVIDIA GPU check
!nvidia-smi

"""# (SETUP ENVIRONMENT)"""

#@title Install dependencies
!git clone --depth 1 https://github.com/asigalov61/Quad-Music-Transformer
!pip install huggingface_hub
!pip install torch
!pip install einops
!pip install torch-summary
!apt install fluidsynth #Pip does not work for some reason. Only apt works

# Commented out IPython magic to ensure Python compatibility.
#@title Import modules

print('=' * 70)
print('Loading core Quad Music Transformer modules...')

import os
import pickle
import secrets
import statistics
from time import time
import tqdm

print('=' * 70)
print('Loading main Quad Music Transformer modules...')
import torch

# %cd /content/Quad-Music-Transformer

import TMIDIX

from midi_to_colab_audio import midi_to_colab_audio

from x_transformer_1_23_2 import *

import random

# %cd /content/
print('=' * 70)
print('Loading aux Quad Music Transformer modules...')

import matplotlib.pyplot as plt

from torchsummary import summary
from sklearn import metrics

from IPython.display import Audio, display

from huggingface_hub import hf_hub_download

from google.colab import files

print('=' * 70)
print('Done!')
print('Enjoy! :)')
print('=' * 70)

"""# (LOAD MODEL)"""

#@title Load Quad Music Transformer Pre-Trained Model

#@markdown Model precision option

model_precision = "bfloat16" # @param ["bfloat16", "float16"]

#@markdown bfloat16 == Half precision/faster speed (if supported, otherwise the model will default to float16)

#@markdown float16 == Full precision/fast speed

plot_tokens_embeddings = False # @param {type:"boolean"}

print('=' * 70)
print('Loading Quad Music Transformer Pre-Trained Model...')
print('Please wait...')
print('=' * 70)

full_path_to_models_dir = "/content/Quad-Music-Transformer/Model"

model_checkpoint_file_name = 'Quad_Music_Transformer_Large_Trained_Model_16964_steps_0.9194_loss_0.7386_acc.pth'
model_path = full_path_to_models_dir+'/'+model_checkpoint_file_name
num_layers = 32

if os.path.isfile(model_path):
  print('Model already exists...')

else:
  hf_hub_download(repo_id='asigalov61/Quad-Music-Transformer',
                  filename=model_checkpoint_file_name,
                  local_dir='/content/Quad-Music-Transformer/Model',
                  local_dir_use_symlinks=False)

print('=' * 70)
print('Instantiating model...')

device_type = 'cuda'

if model_precision == 'bfloat16' and torch.cuda.is_bf16_supported():
  dtype = 'bfloat16'
else:
  dtype = 'float16'

if model_precision == 'float16':
  dtype = 'float16'

ptdtype = {'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
ctx = torch.amp.autocast(device_type=device_type, dtype=ptdtype)

SEQ_LEN = 8192

# instantiate the model

model = TransformerWrapper(
    num_tokens = 2855,
    max_seq_len = SEQ_LEN,
    attn_layers = Decoder(dim = 1024, depth = num_layers, heads = 32, attn_flash = True)
)

model = AutoregressiveWrapper(model, ignore_index=2854)

model.cuda()
print('=' * 70)

print('Loading model checkpoint...')

model.load_state_dict(torch.load(model_path))
print('=' * 70)

model.eval()

print('Done!')
print('=' * 70)

print('Model will use', dtype, 'precision...')
print('=' * 70)

# Model stats
print('Model summary...')
summary(model)

# Plot Token Embeddings
if plot_tokens_embeddings:
  tok_emb = model.net.token_emb.emb.weight.detach().cpu().tolist()

  cos_sim = metrics.pairwise_distances(
    tok_emb, metric='cosine'
  )
  plt.figure(figsize=(7, 7))
  plt.imshow(cos_sim, cmap="inferno", interpolation="nearest")
  im_ratio = cos_sim.shape[0] / cos_sim.shape[1]
  plt.colorbar(fraction=0.046 * im_ratio, pad=0.04)
  plt.xlabel("Position")
  plt.ylabel("Position")
  plt.tight_layout()
  plt.plot()
  plt.savefig("/content/Quad-Music-Transformer-Tokens-Embeddings-Plot.png", bbox_inches="tight")

"""# (SETUP OUTPUT MIDI PACHES)"""

# @title Setup and load output MIDI patches
output_MIDI_patches = "0, 10, 19, 24, 35, 40, 52, 56, 65, 73, 87, 89, 98, 105, 117, 123" # @param {type:"string"}

patches = [int(p) if 0 <= int(p) < 128 else 0 for p in output_MIDI_patches.split(',')]

for chan, pat in enumerate(patches):

  if chan == 9:
      channel = 16
      patch = 0
  else:
    channel = chan
    patch = pat

  print('=' * 70)
  print('MIDI Channel:', chan)
  print('Model Channel:', channel)

  print('MIDI Patch:', patch, '===', TMIDIX.MIDI_Instruments_Families[channel], '===', TMIDIX.Number2patch[patch])

print('=' * 70)

"""# (LOAD SEED MIDI)"""

#@title Load Seed MIDI

#@markdown Press play button to to upload your own seed MIDI or to load one of the provided sample seed MIDIs from the dropdown list below

select_seed_MIDI = "Upload your own custom MIDI" # @param ["Upload your own custom MIDI", "Quad-Music-Transformer-Piano-Seed-1", "Quad-Music-Transformer-Piano-Seed-2", "Quad-Music-Transformer-Piano-Seed-3", "Quad-Music-Transformer-Piano-Seed-4", "Quad-Music-Transformer-Piano-Seed-5", "Quad-Music-Transformer-Piano-Seed-6", "Quad-Music-Transformer-MI-Seed-1", "Quad-Music-Transformer-MI-Seed-2", "Quad-Music-Transformer-MI-Seed-3", "Quad-Music-Transformer-MI-Seed-4", "Quad-Music-Transformer-MI-Seed-5", "Quad-Music-Transformer-MI-Seed-6"]
number_of_prime_tokens = 8190 # @param {type:"slider", min:80, max:8192, step:4}
render_MIDI_to_audio = False # @param {type:"boolean"}

print('=' * 70)
print('Quad Music Transformer Seed MIDI Loader')
print('=' * 70)

#=====================================================
# Helper function
#=====================================================

f = ''

if select_seed_MIDI != "Upload your own custom MIDI":
  print('Loading seed MIDI...')
  f = '/content/Quad-Music-Transformer/Seeds/'+select_seed_MIDI+'.mid'

else:
  print('Upload your own custom MIDI...')
  print('=' * 70)
  uploaded_MIDI = files.upload()
  if list(uploaded_MIDI.keys()):
    f = list(uploaded_MIDI.keys())[0]

if f != '':

  print('=' * 70)
  print('File:', f)
  print('=' * 70)

  #===============================================================================
  # Raw single-track ms score

  raw_score = TMIDIX.midi2single_track_ms_score(f)

  #===============================================================================
  # Enhanced score notes

  escore_notes = TMIDIX.advanced_score_processor(raw_score, return_enhanced_score_notes=True)[0]

  if len(escore_notes) > 0:

      #=======================================================
      # PRE-PROCESSING

      # checking number of instruments in a composition
      instruments_list = list(set([y[3] for y in escore_notes]))

      #===============================================================================
      # Augmented enhanced score notes

      escore_notes = TMIDIX.augment_enhanced_score_notes(escore_notes)

      #=======================================================
      # FINAL PROCESSING

      melody_chords = []
      melody_chords2 = []

      # Break between compositions / Intro seq

      if 9 in instruments_list:
          drums_present = 2706 # Yes
      else:
          drums_present = 2705 # No

      if escore_notes[0][3] != 9:
          fpat = escore_notes[0][6]
          fptc = escore_notes[0][4]
      else:
          fpat = 128
          fptc = escore_notes[0][4]

      fchan = fpat // 8

      melody_chords.extend([2852, drums_present, 2707+fchan, 2724+fptc]) # Intro seq + zero time

      #=======================================================
      # MAIN PROCESSING CYCLE
      #=======================================================

      pe = escore_notes[0]

      chords_counter = 1

      comp_chords_len = len(list(set([y[1] for y in escore_notes])))

      for e in escore_notes:

          #=======================================================
          # Timings...

          # Cliping all values...

          delta_time = max(0, min(255, (e[1]-pe[1])))

          # Durations and channels

          dur = max(0, min(255, e[2]))
          cha = max(0, min(15, e[3]))

          # Patches
          if cha == 9: # Drums patch will be == 128
              pat = 128

          else:
              pat = e[6]

          # Channels

          chan = pat // 8

          # Pitches

          ptc = max(1, min(127, e[4]))

          # Velocities

          # Calculating octo-velocity
          velocity = max(8, min(127, e[5]))
          vel = round(velocity / 8)-1

          #=======================================================
          # Outro seq

          # if comp_chords_len >= 250:
          #    if ((comp_chords_len - chords_counter) == 50) and (delta_time != 0):
          #        melody_chords.extend([2704, 2704, 2704, 2704]) # outro seq

          # if delta_time != 0:
          #    chords_counter += 1

          #=======================================================
          # FINAL NOTE SEQ

          # Writing final note asynchronously

          cha_ptc = (128 * chan) + ptc

          melody_chords.extend([delta_time, dur+256, cha_ptc+512, vel+2688])
          melody_chords2.append([delta_time, dur+256, cha_ptc+512, vel+2688])

          pe = e

          #=======================================================

      # melody_chords.extend([2853, 2853, 2853, 2853]) # EOS

      #=======================================================

      # TOTAL DICTIONARY SIZE 2853+1=2854
      #=======================================================


  melody_chords_f = melody_chords[:number_of_prime_tokens]

  #=======================================================

  song = melody_chords_f

  song_f = []

  time = 0
  dur = 0
  vel = 90
  pitch = 0
  channel = 0

  for ss in song:

      if 0 <= ss < 256:

          time += ss * 16

      if 256 <= ss < 512:

          dur = (ss-256) * 16

      if 512 <= ss < 2688:

          chan = (ss-512) // 128

          if chan < 9:
              channel = chan
          elif 9 < chan < 15:
              channel = chan+1
          elif chan == 15:
              channel = 15
          elif chan == 16:
              channel = 9

          pitch = (ss-512) % 128

      if 2688 <= ss < 2704:

          vel = (((ss-2688)+1) * 8)-1

          song_f.append(['note', time, dur, channel, pitch, vel, chan*8])

  detailed_stats = TMIDIX.Tegridy_ms_SONG_to_MIDI_Converter(song_f,
                                                            output_signature = 'Quad Music Transformer',
                                                            output_file_name = '/content/Quad-Music-Transformer-Seed-Composition',
                                                            track_name='Project Los Angeles',
                                                            list_of_MIDI_patches=patches
                                                            )

  #=======================================================

  print('=' * 70)
  print('Composition stats:')
  print('Composition has', int(len(melody_chords_f) / 3), 'notes')
  print('Composition has', len(melody_chords_f), 'tokens')
  print('Composition MIDI channels:', sorted(list(set([((y-512) // 128) for y in melody_chords if 512 <= y < 2688]))))
  print('=' * 70)

  print('Displaying resulting composition...')
  print('=' * 70)

  fname = '/content/Quad-Music-Transformer-Seed-Composition'

  block_lines = [(song_f[-1][1] / 1000)]
  block_tokens = [min(len(melody_chords_f), number_of_prime_tokens)]
  pblock = []

  if render_MIDI_to_audio:
    midi_audio = midi_to_colab_audio(fname + '.mid')
    display(Audio(midi_audio, rate=16000, normalize=False))

  TMIDIX.plot_ms_SONG(song_f, plot_title=fname)

else:
  print('=' * 70)

"""# (COMPOSITION LOOP)

## Run the cells below in a loop to generate endless continuation
"""

#@title Standard Continuation Generator

#@markdown Generation settings

try_to_generate_outro = False #@param {type:"boolean"}
try_to_introduce_drums = False # @param {type:"boolean"}
number_of_tokens_to_generate = 404 # @param {type:"slider", min:32, max:1024, step:4}
number_of_batches_to_generate = 4 #@param {type:"slider", min:1, max:16, step:1}
preview_length_in_tokens = 120 # @param {type:"slider", min:32, max:240, step:4}
number_of_memory_tokens = 7160 # @param {type:"slider", min:300, max:8192, step:4}
temperature = 0.9 # @param {type:"slider", min:0.1, max:1, step:0.05}

#@markdown Other settings

allow_model_to_stop_generation_if_needed = False #@param {type:"boolean"}
render_MIDI_to_audio = True # @param {type:"boolean"}

print('=' * 70)
print('Quad Music Transformer Standard Continuation Model Generator')
print('=' * 70)

if allow_model_to_stop_generation_if_needed:
  min_stop_token = 2853
else:
  min_stop_token = None

preview = melody_chords_f[-preview_length_in_tokens:]

mel_cho = melody_chords_f[-number_of_memory_tokens:]

if try_to_introduce_drums:
  last_note = mel_cho[-4:]
  drums = [36, 38, 47, 54]
  if 0 <= last_note[0] < 256:
    for d in random.choices(drums, k = random.randint(1, len(drums))):
      mel_cho.extend([0, min(4+256, last_note[1]), ((128*16)+d)+512, 100+2688])

if try_to_generate_outro:
  mel_cho.extend([2704, 2704, 2704, 2704])

torch.cuda.empty_cache()

inp = [mel_cho] * number_of_batches_to_generate

inp = torch.LongTensor(inp).cuda()

with ctx:
  out = model.generate(inp,
                        number_of_tokens_to_generate,
                        temperature=temperature,
                        return_prime=False,
                        eos_token=min_stop_token,
                        verbose=True)

out0 = out.tolist()

torch.cuda.empty_cache()

print('=' * 70)
print('Done!')
print('=' * 70)

#======================================================================
print('Rendering results...')

for i in range(number_of_batches_to_generate):

  print('=' * 70)
  print('Batch #', i)
  print('=' * 70)

  out1 = out0[i]

  print('Sample INTs', out1[:12])
  print('=' * 70)

  if len(out) != 0:

      song = preview + out1
      song_f = []

      time = 0
      dur = 0
      vel = 90
      pitch = 0
      channel = 0

      for ss in song:

          if 0 <= ss < 256:

              time += ss * 16

          if 256 <= ss < 512:

              dur = (ss-256) * 16

          if 512 <= ss < 2688:

              chan = (ss-512) // 128

              if chan < 9:
                  channel = chan
              elif 9 < chan < 15:
                  channel = chan+1
              elif chan == 15:
                  channel = 15
              elif chan == 16:
                  channel = 9

              pitch = (ss-512) % 128

          if 2688 <= ss < 2704:

              vel = (((ss-2688)+1) * 8)-1

              song_f.append(['note', time, dur, channel, pitch, vel, chan*8])

      detailed_stats = TMIDIX.Tegridy_ms_SONG_to_MIDI_Converter(song_f,
                                                          output_signature = 'Quad Music Transformer',
                                                          output_file_name = '/content/Quad-Music-Transformer-Composition_'+str(i),
                                                          track_name='Project Los Angeles',
                                                          list_of_MIDI_patches=patches
                                                          )
      print('=' * 70)
      print('Displaying resulting composition...')
      print('=' * 70)

      fname = '/content/Quad-Music-Transformer-Composition_'+str(i)

      if render_MIDI_to_audio:
        midi_audio = midi_to_colab_audio(fname + '.mid')
        display(Audio(midi_audio, rate=16000, normalize=False))

      TMIDIX.plot_ms_SONG(song_f,
                          plot_title=fname,
                          preview_length_in_notes=int(preview_length_in_tokens / 4)
                          )

#@title Choose one generated block to add to the composition
block_action = "add_last_generated_block" #@param ["add_last_generated_block", "remove_last_added_block"]
add_block_with_batch_number = 0 #@param {type:"slider", min:0, max:15, step:1}
render_MIDI_to_audio = False # @param {type:"boolean"}

print('=' * 70)

if block_action == 'add_last_generated_block':

  new_block = out0[min(len(out0)-1, add_block_with_batch_number)]

  if new_block != pblock:
    melody_chords_f.extend(new_block)
    print('Block added!')

  else:
    print('Nothing to add!!!')

else:
  if len(block_tokens) > 1:
    melody_chords_f = melody_chords_f[:(len(melody_chords_f)-block_tokens[-1])]

    block_lines.pop()
    block_tokens.pop()
    print('Block removed!')

    pblock = []

  else:
    print('Nothing to remove!!!')

print('=' * 70)
print('Composition now has', (len(melody_chords_f) // 4), 'notes')
print('Composition now has', len(melody_chords_f), 'tokens')
print('Composition now has MIDI channels:', sorted(list(set([((y-512) // 128) for y in melody_chords if 512 <= y < 2688]))))

print('=' * 70)
print('Sample INTs', out1[:12])
print('=' * 70)

if len(melody_chords_f) != 0:

    song = melody_chords_f
    song_f = []

    time = 0
    dur = 0
    vel = 90
    pitch = 0
    channel = 0

    for ss in song:

        if 0 <= ss < 256:

            time += ss * 16

        if 256 <= ss < 512:

            dur = (ss-256) * 16

        if 512 <= ss < 2688:

            chan = (ss-512) // 128

            if chan < 9:
                channel = chan
            elif 9 < chan < 15:
                channel = chan+1
            elif chan == 15:
                channel = 15
            elif chan == 16:
                channel = 9

            pitch = (ss-512) % 128

        if 2688 <= ss < 2704:

            vel = (((ss-2688)+1) * 8)-1

            song_f.append(['note', time, dur, channel, pitch, vel, chan*8])

    detailed_stats = TMIDIX.Tegridy_ms_SONG_to_MIDI_Converter(song_f,
                                                              output_signature = 'Quad Music Transformer',
                                                              output_file_name = '/content/Quad-Music-Transformer-Composition',
                                                              track_name='Project Los Angeles',
                                                              list_of_MIDI_patches=patches
                                                              )

    if block_action == 'add_last_generated_block' and new_block != pblock:
      block_tokens.append(len(new_block))
      block_lines.append((song_f[-1][1] / 1000))
      pblock = new_block

    print('=' * 70)
    print('Displaying resulting composition...')
    print('=' * 70)

    fname = '/content/Quad-Music-Transformer-Composition'

    if render_MIDI_to_audio:
      midi_audio = midi_to_colab_audio(fname + '.mid')
      display(Audio(midi_audio, rate=16000, normalize=False))

    TMIDIX.plot_ms_SONG(song_f,
                        plot_title=fname,
                        block_lines_times_list=block_lines[:-1]
                        )

"""# Congrats! You did it! :)"""
