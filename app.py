import gradio as gr
from PIL import Image
from PIL import ImageSequence
import numpy as np
from apng import APNG
import os
import subprocess

def main():
    # Gradio Interface
    with gr.Blocks() as app:
        gr.Markdown(
            """
            # <div align="center"> Ilaria Converter 💖 </div>
            Simple file conversion Software by Ilaria, Help me on Ko-Fi  
    
            Need help with AI? Join Join AI Hub!
            """
        )
        
        with gr.Accordion('Audio Conversion', open=True):
            with gr.Row():
                audio_input = gr.Audio(type='filepath')
                audio_output_format = gr.Dropdown(["wav", "flac", "ogg", "mp3", "aac", "alac", "m4a", "m4r"], label="Audio Output Format")
                change_bitrate = gr.Checkbox(label="Change Bitrate?")
                audio_bitrate = gr.Dropdown(["128", "256", "320"], label="Audio Bitrate")
                convert_audio_butt = gr.Button(value='Convert Audio', variant='primary')
                audio_output = gr.Audio(type='filepath', label="Converted Audio")
                    
        convert_audio_butt.click(fn=convert_audio, inputs=[audio_input, audio_output_format, change_bitrate, audio_bitrate], outputs=audio_output)
            
        with gr.Accordion('Image Conversion', open=True):
            with gr.Row():
                image_input = gr.Image(type='filepath')
                image_output_format = gr.Dropdown(["png", "jpg", "tiff", "bmp", "webp", "gif", "apng"], label="Image Output Format")
                change_resolution = gr.Checkbox(label="Change Resolution?")
                image_width = gr.Number(label="Image Width")
                image_height = gr.Number(label="Image Height")
                convert_image_butt = gr.Button(value='Convert Image', variant='primary')
                image_output = gr.Image(type='filepath', label="Converted Image")
                
        convert_image_butt.click(fn=convert_image, inputs=[image_input, image_output_format, change_resolution, image_width, image_height], outputs=image_output)
        
    app.queue(max_size=1022).launch(share=False)

def convert_audio(audio_file, output_format, change_bitrate, bitrate):
    # Get the base name of the input file
    base_name = os.path.splitext(os.path.basename(audio_file))[0]

    # Convert the audio file to the selected format
    output_audio_file = f'{base_name}.{output_format}'

    # Create the ffmpeg command
    command = ['ffmpeg', '-i', audio_file]
    if change_bitrate:
        command.extend(['-b:a', f'{bitrate}k'])
    command.append(output_audio_file)

    # Run the command
    subprocess.run(command, check=True)
    
    return output_audio_file

def convert_image(input_image, output_format, change_resolution, width, height):
    # Open the image file
    image = Image.open(input_image)

    # Resize the image if the user chose to change the resolution
    if change_resolution:
        image = image.resize((width, height))

    # Get the base name of the input file
    base_name = os.path.splitext(os.path.basename(input_image))[0]

    # Convert the image file to the selected format
    output_image_file = f'{base_name}.{output_format}'

    if output_format == 'apng':
        frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
        frame_files = []
        for i, frame in enumerate(frames):
            frame_file = f'{base_name}_{i}.png'
            frame.save(frame_file)
            frame_files.append(frame_file)
        output_image_file = f"{base_name}.png"
        APNG.from_files(frame_files, delay=100).save(output_image_file)
    else:
        image.save(output_image_file)
    
    return output_image_file

# Create the Gradio interface
main()
