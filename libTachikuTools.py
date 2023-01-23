
import uuid 
import subprocess as sp
from datetime import datetime
import pkg_resources

def listDirContent(_dir):
    import os
    from os.path import isfile, join
    onlyfiles = [f for f in os.listdir(_dir)]
    ret="Found "+str (len(onlyfiles)) + " files in path "+_dir+"<br><br>";
    for x in onlyfiles:
        if isfile(join(_dir, x)):
            ret = ret+x+"<br>"
        else:
            ret = ret+"./"+x+"<br>"

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string+"<br>"+ret


def get_gpu_attr(_attr):
   output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
   COMMAND = "nvidia-smi --query-gpu="+_attr+" --format=csv"
   try:
        memory_use_info = output_to_list(sp.check_output(COMMAND.split(),stderr=sp.STDOUT))[1:]
   except sp.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
   memory_use_values = [x.replace('\r', '') for i, x in enumerate(memory_use_info)]
   return memory_use_values

def get_list_of_modules():
    installed_packages = pkg_resources.working_set
    installed_packages_list=[]
    for i in installed_packages:
        installed_packages_list.append({i.key: i.version})
    return installed_packages_list
    COMMAND = "pip list"
    output_to_list = lambda x: x.decode('ascii').split('\n')[:-1]
    try:
        list = output_to_list(sp.check_output(COMMAND.split(),stderr=sp.STDOUT))[1:]
    except sp.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    aRet = [x.replace('\r', '') for i, x in enumerate(list)]
    return aRet

def getHostInfo(_engine):
    now = datetime.now()
    objGPU={}
    objGPU["memory_free"]=get_gpu_attr("memory.free")[0]
    objGPU["memory_used"]=get_gpu_attr("memory.used")[0]
    objGPU["name"]=get_gpu_attr("gpu_name")[0]
    objGPU["driver_version"]=get_gpu_attr("driver_version")[0]
    objGPU["temperature"]=get_gpu_attr("temperature.gpu")[0]
    objGPU["utilization"]=get_gpu_attr("utilization.gpu")[0]

    objCuda=getCudaInfo()

    return {
        "datetime": now.strftime("%d/%m/%Y %H:%M:%S"), 
        "engine": _engine,
        "machine": str (hex(uuid.getnode())),
        "GPU": objGPU,
        "Cuda": objCuda,
        "modules": get_list_of_modules()
    }


import ctypes
cuda=0    #from cuda import cuda, nvrtc

# see here: https://gist.github.com/tispratik/42a71cae34389fd7c8e89496ae8813ae
def getCudaInfo():
    CUDA_SUCCESS = 0
    CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT = 16
    CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR = 39
    CU_DEVICE_ATTRIBUTE_CLOCK_RATE = 13
    CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE = 36

    nGpus = ctypes.c_int()
    name = b' ' * 100
    cc_major = ctypes.c_int()
    cc_minor = ctypes.c_int()
    cores = ctypes.c_int()
    threads_per_core = ctypes.c_int()
    clockrate = ctypes.c_int()
    freeMem = ctypes.c_size_t()
    totalMem = ctypes.c_size_t()

    result = ctypes.c_int()
    device = ctypes.c_int()
    context = ctypes.c_void_p()
    error_str = ctypes.c_char_p()


    if cuda:
        result=cuda.cuInit(0)
        if(result != CUDA_SUCCESS):
            print("error %d " % (result))
            return 0
        
        if(cuda.cuDeviceGetCount(ctypes.byref(nGpus)) != CUDA_SUCCESS):
            return 0

        for i in range(nGpus.value):

            # get device
            if(cuda.cuDeviceGet(ctypes.byref(device), i) != CUDA_SUCCESS):
                return 0
            if (cuda.cuDeviceComputeCapability(ctypes.byref(cc_major), ctypes.byref(cc_minor), device) != CUDA_SUCCESS):  
                return 0
            if (cuda.cuDeviceGetName(ctypes.c_char_p(name), len(name), device) != CUDA_SUCCESS): 
                return 0
            if(cuda.cuDeviceGetAttribute(ctypes.byref(cores), CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT, device) != CUDA_SUCCESS):
                return 0

    return {
        "name": name.split(b'\0', 1)[0].decode(),
        "compute_major": cc_major.value,
        "compute_minor": cc_minor.value,
        "cuda cores": cores.value * _ConvertSMVer2Cores(cc_major.value, cc_minor.value)
    }

def _ConvertSMVer2Cores(major, minor):
    # Returns the number of CUDA cores per multiprocessor for a given
    # Compute Capability version. There is no way to retrieve that via
    # the API, so it needs to be hard-coded.
    return {
    # Tesla
      (1, 0):   8,      # SM 1.0
      (1, 1):   8,      # SM 1.1
      (1, 2):   8,      # SM 1.2
      (1, 3):   8,      # SM 1.3
    # Fermi
      (2, 0):  32,      # SM 2.0: GF100 class
      (2, 1):  48,      # SM 2.1: GF10x class
    # Kepler
      (3, 0): 192,      # SM 3.0: GK10x class
      (3, 2): 192,      # SM 3.2: GK10x class
      (3, 5): 192,      # SM 3.5: GK11x class
      (3, 7): 192,      # SM 3.7: GK21x class
    # Maxwell
      (5, 0): 128,      # SM 5.0: GM10x class
      (5, 2): 128,      # SM 5.2: GM20x class
      (5, 3): 128,      # SM 5.3: GM20x class
    # Pascal
      (6, 0):  64,      # SM 6.0: GP100 class
      (6, 1): 128,      # SM 6.1: GP10x class
      (6, 2): 128,      # SM 6.2: GP10x class
    # Volta
      (7, 0):  64,      # SM 7.0: GV100 class
      (7, 2):  64,      # SM 7.2: GV11b class
    # Turing
      (7, 5):  64,      # SM 7.5: TU10x class
    }.get((major, minor), 64)   # unknown architecture, return a default value