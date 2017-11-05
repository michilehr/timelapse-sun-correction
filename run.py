import os, sys, argparse
from PIL import Image, ImageOps
from os import path
import imghdr

# read command line arguments

parser = argparse.ArgumentParser("run.py")
parser.add_argument('-input', help="Input directory", required=True)
parser.add_argument('-output', help="Output directory", required=True)

args = parser.parse_args()

inputDir = args.input
outputDir = args.output

sunSize = 0
imgBoarder = 200

def treshold(x):
    if x < 100:
        x = 0
    return x

def suncrop(image, border):
    sunBorders = image.point(treshold).getbbox()
    global sunSize

    # get sun size from the first image where the sun is complete

    if sunSize == 0:
        sunSize = sunBorders[3] - sunBorders[1]
        print "Sunsize %d px" % sunSize

    # calculcate top point x from sun by cropping first line and divide left and right border /2

    sunFirstLinePoints = (0, sunBorders[1], im.size[0], sunBorders[1]+1)
    sunFirstLineCrop = im.crop(sunFirstLinePoints)

    sunFirstLineBoarder = sunFirstLineCrop.point(treshold).getbbox()

    topBorder = sunBorders[1] - imgBoarder
    bottomSunBorder = sunBorders[1] + imgBoarder + sunSize 
    leftSunBoarder = ((sunFirstLineBoarder[0] + sunFirstLineBoarder[2])/2) - (sunSize/2) - imgBoarder
    rightSunBoarder = ((sunFirstLineBoarder[0] + sunFirstLineBoarder[2])/2) + (sunSize/2) + imgBoarder    

    # crop whole image only by top point and sun size as reference
    
    sunBorderBorders = (leftSunBoarder, topBorder, rightSunBoarder, bottomSunBorder)
    return image.crop(sunBorderBorders)

sunSize = 0
files = [f for f in os.listdir(inputDir) if f.endswith(".jpg")]
files.sort()

for img in files:
    im = Image.open("%s/%s" % (inputDir, img))
    imtrim = suncrop(im, imgBoarder)
    outfile = "%s/%s" % (outputDir, img)
    print "Saving to %s" % outfile
    imtrim.save(outfile)