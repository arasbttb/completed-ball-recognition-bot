import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)



from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
def get_class(model_path , labels_path , image_path):
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model(r"C:\Users\Aras Bartu TEBER\Desktop\Projem\keras_model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(image_path).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

    return f"Class: {class_name}\nConfidence Score: {confidence_score:.2f}"
    if not class_name:
        return "Dosya sınıflandırılamadı"




    
@bot.command()
async def check(ctx):
    try:
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                file_name = attachment.filename
                await attachment.save(f"./{file_name}")
                result = get_class("keras_model.h5", "labels.txt", f"./{file_name}")
                
                if result:
                    await ctx.send(result)
                else:
                    await ctx.send("Sonuç döndürülemedi, lütfen dosyanızı kontrol edin.")
        else:
            await ctx.send("Bir dosya yüklemeyi unuttunuz :(")
    except UnicodeDecodeError as e:
        await ctx.send(f"Dosya kodlama hatası: {e}")
    except Exception as e:
        await ctx.send(f"Beklenmedik bir hata oluştu: {e}")



    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)


bot.run("")