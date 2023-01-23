

set /A resX = 512
set /A resY = 512
set model="models/ldm/stable-diffusion-v1/sd-v1-4.ckpt"
set /A seed = 50

rem change this...
rem set prompt= "dali painting of van gogh flowers with a touch of gustav klimt"
set prompt= "realistic photo of a fragile woman with deep fascinating look, blue eyes, and long hair"

python runlocal_txt2img.py -orig "http://localhost:3456/" -t 123456789 -u "testlocal" -uid 987654321 --W %resX% --H %resY% --plms  --ckpt %model% --prompt %prompt% --outdir _output --seed %seed%
:End
