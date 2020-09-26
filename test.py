import 	numpy 				as 		np
import 	matplotlib.image 	as 		mpimg
import 	matplotlib.pylab 	as 		plt

from 	PIL 				import 	Image

from 	skimage.io 			import	imread 	
from 	skimage.color 		import 	rgb2lab, lab2rgb, rgb2gray

from 	copy 				import 	deepcopy
from 	pytesseract 		import 	image_to_string

from 	bba_image			import *


#	Testing script
#	...