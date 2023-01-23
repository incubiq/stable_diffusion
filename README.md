
** Origin
 - https://github.com/CompVis/stable-diffusion

** TEST samples
 - python scripts/txt2img.py --prompt "dali painting of van gogh flowers with a touch of gustav klimt" --plms --ckpt models/ldm/stable-diffusion-v1/sd-v1-4.ckpt --outdir _output
 - python scripts/img2img.py  --init-img _input/zombie.jpg --strength 0.35 --ckpt models/ldm/stable-diffusion-v1/sd-v1-4.ckpt --outdir _output  --n_samples 4

** BATCH MODE RUN
// to run DIFFUSION in BATCH mode (not a server), use: 
 - runlocal_txt2img.bat  (it has its entry point with runlocal_txt2img.py, then making use of scripts/txt2img.py)

** SERVER MODE RUN
// the python servers are built with FLASK ; when debugging (not in docker), it needs a FLASK app defined to run
// in windows (when debugging) use :  $env:FLASK_APP="flask_5000"
// in linux / wsl, use :  FLASK_APP="flask_5000"
// to run DIFFUSION in local server mode (localhost:5004), open terminal
  - conda activate ldm                                    // put the machine in the right conda env
  - go to AI/DIFFUSION  dir                               // go in the correct directory
  - $env:FLASK_APP="flask_5000"                           // set the flask env var
  - python -m flask run --host=0.0.0.0 --port=5004        // run the python web server
  // remember this localhost runs on http://192.168.1.108:5004/   so this is where we can access it (nowhere else, all other pings fail)
  // http://localhost:5004/run?uid=0&token=0&username=bob&orig=http%3A%2F%2Flocalhost%3A3654%2F&odir=_output&output=result&prompts=zombie&cimg=4&strength=0.7&steps=10&seed=10&input=_input%2Fzombie.jpg
  
** DOCKER MODE (SERVER) RUN
docker build -t yeepeekoo/my_images:ai_diffusion .
docker push yeepeekoo/my_images:ai_diffusion

// on windows
docker run -it -v "$(pwd)/_input:/src/app/_input" -v "$(pwd)/_output:/src/app/_output" --name ai_diffusion --rm --gpus all --publish 5004:5000 yeepeekoo/my_images:ai_diffusion

// on WLS => same (but GPU should work!)

// to run PING in docker server mode (localhost:5001), see instructions in flask_5000.py  (we can also run it locally in flask for debug before running the flask app in docker)
// list of files in root : localhost:5004/root
// list of files in input dir : localhost:5004/input
// list of files in output dir : localhost:5004/output
// warning : since docker cannot see localhost, it requires passing as encoded param the TachikuAI origin ( ?orig=.... ) to the localhost:5004/run?... at each call

// NOTE: the notifyTachiku.py file is duplicated in all AI engines directories since docker (shit) cannot build an image with files outside its root directory... so we duplicate... make sure they are all in sync when updating
