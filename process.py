import sys
import os

from pysiril.siril   import *

def master_bias(bias_dir, process_dir):
    app.Execute("cd " + bias_dir )
    app.Execute("convert bias -out=" + process_dir + " -fitseq" )
    app.Execute("cd " + process_dir )
    app.Execute("stack bias rej 3 3  -nonorm")
    
def master_flat(flat_dir, process_dir, hasbias=True):
    if hasbias:
        bias_switch = "-bias=bias_stacked"
    else:
        bias_switch = ""

    app.Execute("cd " + flat_dir + "\n"
                "convert flat -out=" + process_dir + " -fitseq"   + "\n"
                "cd " + process_dir  + "\n"
                "calibrate flat  " + bias_switch + "\n"
                "stack pp_flat rej  3 3 -norm=mul")
    
def master_dark(dark_dir, process_dir):
    app.Execute(""" cd %s
                    convert dark -out=%s -fitseq
                    cd %s
                    stack dark rej 3 3 -nonorm """ % (dark_dir,process_dir,process_dir) )
    
def light(light_dir, process_dir, hasflats=True, hasdarks=True):
    if hasflats:
        flat_switch = " -flat=pp_flat_stacked "
    else:
        flat_switch = ""

    if hasdarks:
        dark_switch = " -dark=dark_stacked "
    else:
        dark_switch = ""

    app.Execute("cd " + light_dir)
    app.Execute("convert light -out=" + process_dir + " -fitseq"  )
    app.Execute("cd " + process_dir )
    app.Execute("calibrate light -bias=bias_stacked " + dark_switch + flat_switch + " -cfa -equalize_cfa -debayer" )
    app.Execute("seqsubsky pp_light 1")
    app.Execute("register bkg_pp_light")
    app.Execute("stack r_bkg_pp_light rej 3 3 -norm=addscale -output_norm -out=../result")
    app.Execute("close")
    
# ==============================================================================

work_dir     = "C:/Users/dave/Desktop/thor"

app=Siril()

try:
    app.Open(  )
    
    app.Execute("set32bits")
    app.Execute("setext fit")
    
    process_dir = work_dir+ '/process'
    flats_dir   = work_dir+ '/flats'
    darks_dir   = work_dir+ '/darks'
    biases_dir  = work_dir+ '/biases'
    lights_dir  = work_dir+ '/lights'
    
    if (os.path.isdir(flats_dir)) and (len(os.listdir(flats_dir)) > 0): 
        hasflats=True
    else:
        hasflats=False
        raise Exception("hasflats is false")

    if (os.path.isdir(darks_dir)) and (len(os.listdir(darks_dir)) > 0): 
        hasdarks=True
    else:
        hasdarks=False

    if (os.path.isdir(biases_dir)) and (len(os.listdir(biases_dir)) > 0): 
        hasbiases=True
    else:
        hasbiases=False

    if hasflats:
        master_bias(biases_dir, process_dir)
        master_flat(flats_dir,  process_dir, hasbiases)
    
    if hasdarks:
        master_dark(darks_dir, process_dir)  

    light(lights_dir, process_dir, hasflats, hasdarks)
except Exception as e :
    print("\n**** ERROR *** " + str(e) + "\n" )    
    
app.Close( )
del app