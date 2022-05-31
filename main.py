# pip install numpy
# pip install matplotlib?
import zlib
import struct
from Fourier_Wav import *
from PNGChunkAnaliser_File import *
import numpy as npf
import matplotlib.pyplot as plt

my_image = 'png_files\\type_3.png'

DFT_S(my_image)
Colors(my_image)
PNG_Analysis = PNGChunkAnaliser(my_image)
# PNG_Analysis.ReadPNG();
