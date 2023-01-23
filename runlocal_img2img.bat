
set model="models/ldm/stable-diffusion-v1/sd-v1-4.ckpt"
set /A seed = 1

rem change this...
set input=_input/4343_2.jpg
set prompt= "a young athlete in mountain surroundings"
set strength=0.15

python runlocal_img2img.py -orig "http://localhost:3456/" -t 123456789 -u "testlocal" -uid 987654321 --strength %strength% --prompt %prompt% --init-img  %input% --ckpt %model% --outdir _output --seed %seed%
:End
