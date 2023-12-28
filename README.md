# Record default audio input into mp3 chunks 🐍 😄

<hr>

Record default audio input into mp3 chunks files. If you would like to make any comments then please feel free to email me: sam.y.tang@gmail.com.
You can use Virtual Audio Cable from https://vb-audio.com/Cable/ to route audio output into audio input. Therefore you can record PC audio output directly into mp3 files.

<hr>
How to use?
<hr>
python -m venv venv <br>
venv\Scripts\activate  <br>
pip install -r requirements.txt  <br>
python record2mp3.py filename_prefix total_length_in_seconds  <br>

You can change the default file chunk size by modifying CHUNK_SIZE. Default 300 seconds
