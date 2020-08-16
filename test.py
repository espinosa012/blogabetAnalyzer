import 	numpy 				as 		np
import 	matplotlib.image 	as 		mpimg
import 	matplotlib.pylab 	as 		plt

from 	PIL 				import 	Image

from 	skimage.io 			import	imread 	
from 	skimage.color 		import 	rgb2lab, lab2rgb, rgb2gray

from 	copy 				import 	deepcopy
from 	pytesseract 		import 	image_to_string

from 	bba_image			import *


chart_path 	=	'./profit_charts/soccermister.png'


def last_year_balance(img_path):
	negative_area_color 	=	[242, 190, 199]
	positive_area_color 	=	[183, 229, 218]
	test_color 				=	[255,255,204]
	
	im 				=	np.array(imread(img_path))
		
	positive_area 	=	len(np.argwhere(im==positive_area_color))
	negative_area 	=	len(np.argwhere(im==negative_area_color))
	test_area 		=	len(np.argwhere(im==test_color))

	print({	
			'positive_area':positive_area, 
			'negative_area':negative_area, 
			'test_area':test_area, 
			'shape':im[...,2].shape,
			'size':im.size, 
		})

'''
im 	=	imread(chart_path)

x1=30
y2=80
y1=30
x2=220


imshow(im[x1:x2,y1:y2])
print(image_to_string(im[x1:x2,y1:y2]))'''