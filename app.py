import gradio as gr
import soundfile as sf
from PIL import Image

def main():
    # Gradio Interface
    with gr.Blocks() as app:
        with gr.Row():
            with gr.Column():
                audio_input = gr.Audio(type='filepath')
                audio_output_format = gr.Dropdown(["wav", "flac", "ogg", "mp3"], label="Audio Output Format")
                convert_audio_butt = gr.Button(value='Convert Audio', variant='primary')
                audio_output = gr.Markdown(value="", visible=True)
            with gr.Column():
                image_input = gr.Image(type='filepath')
                image_output_format = gr.Dropdown(["png", "jpg", "tiff", "bmp"], label="Image Output Format")
                convert_image_butt = gr.Button(value='Convert Image', variant='primary')
                image_output = gr.Markdown(value="", visible=True)
        
        convert_audio_butt.click(fn=convert_audio, inputs=[audio_input, audio_output_format], outputs=audio_output)
        convert_image_butt.click(fn=convert_image, inputs=[image_input, image_output_format], outputs=image_output)
        
        app.queue(max_size=1022).launch(share=True)

def convert_audio(audio_file, output_format):
    # Read the audio data from the file
    audio_data, sample_rate = sf.read(audio_file)

    # Convert to mono if it's not mono
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)

    # Convert the audio file to the selected format
    sf.write(f'output_audio.{output_format}', audio_data, sample_rate)
    
    return f"Audio converted to {output_format} format."

def convert_image(input_image, output_format):
    # Open the image file
    image = Image.open(input_image)

    # Convert the image file to the selected format
    image.save(f'output_image.{output_format}')
    
    return f"Image converted to {output_format} format."

# Create the Gradio interface
main()
