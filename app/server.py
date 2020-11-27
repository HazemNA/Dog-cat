import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

#export_file_url = 'https://www.dropbox.com/s/z33humicksg6iu2/Dogcat.pkl?dl=1'
#export_file_name = 'Dogcat.pkl'
export_file_url = 'https://www.dropbox.com/s/u8ah1h7h7n5khub/Dog-Cat-2.pkl?dl=1'
export_file_name = 'Dog-Cat-2.pkl'

#classes = ['Abyssinian', 'Bengal', 'Birman', 'Bombay', 'British_Shorthair', 'Egyptian_Mau', 'Maine_Coon', 'Persian', 'Ragdoll', 'Russian_Blue', 'Siamese', 'Sphynx', 'aegean', 'american_bulldog', 'american_pit_bull_terrier', 'anatolian_shepherd', 'arabian_mau', 'australian_shepherd', 'basset_hound', 'beagle', 'bernese_mountain', 'boston_terrier', 'boxer', 'bull_terrier', 'bulldog', 'canaan', 'cavalier_spaniel', 'chihuahua', 'dachshund', 'dalmation', 'devon_rex', 'doberman', 'english_cocker_spaniel', 'english_setter', 'english_springer_spaniel', 'french_bulldog', 'german_shepherd', 'german_shorthaired', 'german_shorthaired_pointer', 'golden_retriever', 'great_dane', 'great_pyrenees', 'havanese', 'huskey', 'japanese_chin', 'keeshond', 'labrador_retriever', 'leonberger', 'miniature_pinscher', 'miniature_schnauzer', 'newfoundland', 'pembroke_welsh_corgi', 'pharaoh_hound', 'pharaoh_statue', 'pomeranian', 'poodle', 'pug', 'rottweiler', 'saint_bernard', 'saluki', 'samoyed', 'scottish_terrier', 'shetland_sheepdog', 'shiba_inu', 'shih_tzu', 'sloughi', 'staffordshire_bull_terrier', 'turkish_van', 'wheaten_terrier', 'yorkshire_terrier']
classes = ['Abyssinian Cat',
 'Aegean Cat',
 'American Bulldog',
 'American Pitbull Terrier',
 'Anatolian Shepherd Dog',
 'Anubis and-or Hieroglyphs',
 'Arabian Mau Cat',
 'Australian Shepherd',
 'Basset Hound',
 'Beagle',
 'Bengal Cat',
 'Bernese Mountain Dog',
 'Birman Cat',
 'Bombay Cat',
 'Boston Terrier',
 'Boxer',
 'British Shorthair',
 'Bull Terrier',
 'Bulldog',
 'Canaan Dog',
 'Cavalier King Charles Spaniel',
 'Chihuahua',
 'Dachshund',
 'Dalmation',
 'Devon Rex Cat',
 'Doberman',
 'Egyptian Mau Cat',
 'English Cocker Spaniel',
 'English Setter',
 'English Springer Spaniel',
 'French Bulldog',
 'German Shepherd',
 'German Shorthair',
 'German Shorthaired Pointer',
 'Golden Retriever',
 'Great Dane',
 'Great Pyrenees',
 'Havanese Dog',
 'Huskey',
 'Japanese Chin',
 'Keeshond',
 'Labrador Retriever',
 'Leonberger',
 'Maine Coon Cat',
 'Miniature Pinscher',
 'Miniature Schnauzer',
 'New Found Land',
 'Pembroke Welsh Corgi',
 'Persian Cat',
 'Pharaoh Hound',
 'Pomeranian',
 'Poodle',
 'Portugesse Water Dog',
 'Pug',
 'Ragdoll Cat',
 'Rottweiler',
 'Russian Blue Cat',
 'Saint Bernard',
 'Saluki',
 'Samoyed',
 'Scottish Terrier',
 'Shetland Sheepdog',
 'Shiba Inu',
 'Shih Tzu Dog',
 'Siamese Cat',
 'Sloughi',
 'Sphynx Cat',
 'Staffordshire Bull Terrier',
 'Turkish Van Cat',
 'Wheaten Terrier',
 'Yorkshire Terrier']

path = Path(__file__).parent
app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    size = 256, 256
    im.thumbnail(size, img.ANTIALIAS)
    
    prediction = learn.predict(im)[0]
    return JSONResponse({'result': str(prediction)})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
