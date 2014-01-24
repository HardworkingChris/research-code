from __future__ import print_function
import os
import sys
import subprocess as subp
import numpy as np
import scipy.io as scio
import spike_distance as sd
import spike_distance_mp as sdm



def octave_spkd(st_one, st_two, cost):
    """
    Creates an octave `m` file to run the spike train distance script, then
    saves the two spike trains to disk in order to be loaded into the octave
    function script and run the comparison. The result is again saved, loaded
    and returned by this function.
    """
    octave_filename = "run_spkd.m"
    octave_code = (
        "% Automatically generated script. Code exists in st_distance.py.\n"
        "% There is absolutely no reason this code could not just exist here\n"
        "% to begin with."
        "\n"
        "output_precision(10)\n"
        "load(\"tmp_spiketrains.mat\")\n"
        "printf(\"OCTAVE: Loaded tmp_spiketrains.mat\\n\");"
        "d=spkd(one, two, cost);\n"
        "save(\"-mat\", \"tmp_distfile.mat\", \"d\")\n "
        "printf(\"OCTAVE: Saved tmp_distfile.mat\\n\");"
        "\n"
    )
    octave_script = open(octave_filename, "w")
    octave_script.write(octave_code)
    octave_script.close()
    print("Octave function created (%s) ..." % (octave_filename))
    data = {"one": st_one, "two": st_two, "cost": cost}
    scio.savemat("tmp_spiketrains.mat", data)
    print("Data saved to tmp_spiketrains.mat ...")
    _null = open(os.devnull, "w")
    subp.call(["octave", "run_spkd.m"]) #, stdout=_null)#, stderr=_null)
    print("Octave subprocess finished!")
    oct_dist = scio.loadmat("tmp_distfile.mat")["d"]
    try:
        oct_dist = float(oct_dist)
    except ValueError:
        print("Something went wrong with the output of the process.\n"
              "The result was: %s" % (oct_dist), file=sys.stderr)
    return oct_dist


if __name__=="__main__":
    # generate two spike trains
    print("Generating random spike trains ...")
    st_one = np.cumsum(np.random.random(100))
    st_two = np.cumsum(np.random.random(90))
    cost = np.random.randint(100)

    print("Running python script(s) ...")
    dist_sd = sd.stdistance(st_one, st_two, cost)
    dist_sdm = sdm.stdistance(st_one, st_two, cost)

    print("Doing the octave ...")
    dist_oct = octave_spkd(st_one, st_two, cost)

    print("The results were as follows:")
    print("sd\t\tsdm\t\toctave")
    print("%0.5f\t%0.5f\t%0.5f" % (dist_sd, dist_sdm, dist_oct))
    print("-"*10)
    print("|sd - sdm|  = %f" % (np.abs(dist_sd-dist_sdm)))
    print("|sd - oct|  = %f" % (np.abs(dist_sd-dist_oct)))
    print("|sdm - oct| = %f" % (np.abs(dist_sdm-dist_oct)))


