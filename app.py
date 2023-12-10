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
            File conversion Software by Ilaria, support me on [Ko-Fi!](https://ko-fi.com/ilariaowo)  
    
            Need help with AI? [Join AI Hub!](https://discord.gg/aihub)
            """
        )
        
        with gr.Tab('Audio Conversion'):
            with gr.Row():
                audio_input = gr.Audio(type='filepath')
                with gr.Column():
                    audio_output_format = gr.Dropdown(["wav", "flac", "ogg", "mp3", "aac", "m4a"], label="Audio Output Format")
                    change_bitrate = gr.Checkbox(label="Change Bitrate?")
                    audio_bitrate = gr.Dropdown(["128", "256", "320"], label="Audio Bitrate")
                convert_audio_butt = gr.Button(value='Convert Audio', variant='primary')
                audio_output = gr.Audio(type='filepath', label="Converted Audio")
                    
        convert_audio_butt.click(fn=convert_audio, inputs=[audio_input, audio_output_format, change_bitrate, audio_bitrate], outputs=audio_output)
            
        with gr.Tab('Image Conversion'):
            with gr.Row():
                image_input = gr.Image(type='filepath', image_mode='RGBA')
                with gr.Column():
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
    command = ['ffmpeg', '-y', '-i', audio_file]
    if change_bitrate:
        command.extend(['-b:a', f'{bitrate}k'])
    command.append(output_audio_file)

    # Run the command
    subprocess.run(command, check=True)
    
    return output_audio_file

def convert_image(input_image, output_format, change_resolution, width, height):
    base_name = os.path.splitext(os.path.basename(input_image))[0]
    
    out_file = f'{base_name}.{output_format}'
    
    command = ['ffmpeg', '-y', '-i', input_image, '-vframes', '1']

    if change_resolution:
        command.extend(['-vf', f'scale={width}:{height}'])

    command.append(out_file)

    subprocess.run(command, check=True)

    print(f'Converted {input_image} to {out_file}')

    return out_file

# Create the Gradio interface
main()