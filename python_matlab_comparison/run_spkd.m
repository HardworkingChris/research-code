% Automatically generated script. Code exists in st_distance.py.
% There is absolutely no reason this code could not just exist here
% to begin with.
output_precision(10)
load("tmp_spiketrains.mat")
printf("OCTAVE: Loaded tmp_spiketrains.mat\n");d=spkd(one, two, cost);
save("-mat", "tmp_distfile.mat", "d")
 printf("OCTAVE: Saved tmp_distfile.mat\n");
