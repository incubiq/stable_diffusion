##
## when in docker:
##
##   Put yourself in the JUST-PING directory
##   Go in Linux : wsl
##   Build the docker image: docker build -t yeepeekoo/my_images:ai_ping .
##   Run doker instance: docker run -it -v "$(pwd)/_input:/src/app/_input" -v "$(pwd)/_output:/src/app/_output" --name ai_ping --rm --gpus all --publish 5001:5000 yeepeekoo/my_images:ai_ping
##   Test it: http://localhost:5001/run?orig=TODO&username=123&uid=4343&token=123098&size=800&output=test.jpg&input=622969762353.jpg
##
##
## when debug locally:
##
##   Put yourself in the JUST-PING directory
##   Set env var once:  $env:FLASK_APP="flask_5000"
##   Run with: python -m flask run --host=0.0.0.0 --port=5000
##   Test it : http://localhost:5000/run?username=123&uid=4343&token=123098&size=800&output=test.jpg&input=..%2F_uploads%2F551918561430.jpg&odir=.%2F_output%2F
##

APP_ENGINE="AI-DIFFUSION"
from flask import Flask, request, jsonify, render_template
app = Flask(
    APP_ENGINE,  
    template_folder='_template',
    static_folder='_output')

from libTachikuTools import getHostInfo, listDirContent
import json

import sys
sys.path.insert(0, './scripts')

# globals (to avoid cost of re-init each time)
gModel=0
gDevice=0


@app.route('/')
def home():
    obj=getHostInfo(APP_ENGINE)  
    ret=json.dumps(obj, indent=4)
    print(ret)
    return ret
#    return dt_string+"<br>"+'TaChiKu AI<br>Engine: VQGAN<br><br>Go to /run to make use of it'

@app.route('/root')
def root():
    return listDirContent("./")

@app.route('/input')
def input():
    return listDirContent("./_input")

@app.route('/output')
def output():
    return listDirContent("./_output")

@app.route('/test')
def test():
    return render_template('./image_result.html', 
        prompt="zombie", 
        seed=100, 
        strength=0.5,
        steps=20,
        cimg=2,
        files=[],
        W=512,
        H=512,

        username="",
        token="0",
        uid="0",
        
        orig="http://localhost:3654/",
        odir="_output",
        output="result",
        input="_input/zombie.jpg")

@app.route('/run')
def run():
    from img2img import fn_runImg
    from txt2img import fn_runTxt

    aFinalArg=[]
    
    ## tachiku args
    if request.args.get('uid'):
        aFinalArg.append("-uid")
        aFinalArg.append(request.args.get('uid'))
    if request.args.get('token'):
        aFinalArg.append("-t")
        aFinalArg.append(request.args.get('token'))
    if request.args.get('username'):
        aFinalArg.append("-u")
        aFinalArg.append(request.args.get('username'))

    # output dir (with trailing slash)
    if request.args.get('odir'):
        aFinalArg.append("--outdir")
        aFinalArg.append(request.args.get('odir'))

    # output filename
    if request.args.get('output'):
        aFinalArg.append("--output")
        aFinalArg.append(request.args.get('output'))
    
    # input image
    if request.args.get('input'):
        aFinalArg.append("--init-img")
        aFinalArg.append(request.args.get('input'))
    
    # size W
    if request.args.get('W'):
        aFinalArg.append("--W")
        aFinalArg.append(request.args.get('W'))
    
    # size H
    if request.args.get('H'):
        aFinalArg.append("--H")
        aFinalArg.append(request.args.get('W'))
    
    # iterations
    if request.args.get('iterations'):
        aFinalArg.append("-i")
        aFinalArg.append(request.args.get('iterations'))

    # strength
    if request.args.get('strength'):
        aFinalArg.append("--strength")
        aFinalArg.append(request.args.get('strength'))

    # seed
    if request.args.get('seed'):
        aFinalArg.append("--seed")
        aFinalArg.append(request.args.get('seed'))

    # samples (how many per call)
    if request.args.get('cimg'):
        aFinalArg.append("--n_samples")
        aFinalArg.append(request.args.get('cimg'))

    # steps
    if request.args.get('steps'):
        aFinalArg.append("--ddim_steps")
        aFinalArg.append(request.args.get('steps'))

    # word(s) for morphing
    if request.args.get('prompts'):
        aFinalArg.append("--prompt")
        aFinalArg.append(request.args.get('prompts'))
        
    # model used for morphing
    if request.args.get('ckpt'):
        aFinalArg.append("--ckpt")
        aFinalArg.append(request.args.get('ckpt'))
                
    if request.args.get('orig'):
        aFinalArg.append("-orig")
        aFinalArg.append(request.args.get('orig'))

    print("processed args from url: "+str(aFinalArg))
    
    global gModel
    global gDevice

    if request.args.get('input')=="":
        aOutput, model, device=fn_runTxt(aFinalArg, gModel, gDevice)
        gModel=model
        gDevice=device
    else:
        aOutput, model, device=fn_runImg(aFinalArg, gModel, gDevice)
        gModel=model
        gDevice=device

    return render_template('./image_result.html', 
        files=aOutput, 
        prompt=request.args.get('prompts'), 
        seed=request.args.get('seed'), 
        strength=request.args.get('strength'),
        steps=request.args.get('steps'),
        W=request.args.get('W'),
        H=request.args.get('H'),
        cimg=request.args.get('cimg'),

        username=request.args.get('username'),
        token=request.args.get('token'),
        uid=request.args.get('uid'),

        orig=request.args.get('orig'),
        odir=request.args.get('odir'),
        output=request.args.get('output'),
        input=request.args.get('input'))

