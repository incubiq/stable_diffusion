
## used as the entry point from the runlocal batch command line

import sys
sys.path.insert(0, './scripts')
from img2img import fn_run

args=sys.argv[1:]
fn_run(args)
