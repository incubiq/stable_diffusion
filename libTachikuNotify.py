import requests

AI_PROGRESS_IDLE=0
AI_PROGRESS_PROCESSED_ARGS=1
AI_PROGRESS_START_AI=2
AI_PROGRESS_INIT_IMAGE=3
AI_PROGRESS_DONE_IMAGE=4
AI_PROGRESS_STOP_AI=5
AI_PROGRESS_WARNING=11

TACHIKU_AI_ORIGIN="http://localhost:3654/"
def setTachikuOrigin(_origin):
    global TACHIKU_AI_ORIGIN
    TACHIKU_AI_ORIGIN=_origin
    print("=> Tachiku origin reset to: "+_origin)

# Notify Tachiku server of where we are...
def notifyTachiku(CredParam, MorphingParam, StageParam):
    
    # prepare URL
    strToken=str(CredParam["tokenAI"])
    strUID=str(MorphingParam["uid"])
    param="?engine="+CredParam["engine"]+"&username="+CredParam["username"]+"&descr="+StageParam["descr"]+"&uid="+strUID+"&token="+strToken
    if StageParam["stage"]>0:
        param=param+"&stage="+str(StageParam["stage"])
    if MorphingParam["cycle"]>=0:
        param=param+"&cycle="+str(MorphingParam["cycle"])
        if MorphingParam["filename"]!="":
            param=param+"&filename="+MorphingParam["filename"]
    api_url = TACHIKU_AI_ORIGIN+"api/v1/public/ai/notify"+param
    print("\r\n"+api_url)

    # notification console log
    merged = dict()
    merged.update(CredParam)
    merged.update(MorphingParam)
    merged.update(StageParam)
    print("NotifyTaChiKu: "+str(merged))

    # lets go call TaChiKu AI
    response = requests.get(api_url)
