# Passport photo preparation tool

The script generates a vertical 6x4" image file with two photos in it from the provided file with tick guides to allow easier cutting of the printed photo

Requires a processed photo of size 600x600 px.

| Original image: | Resulted image:      |
|-----------------|----------------------|
| <img src="photo.jpg" style="border-style:dotted;" width="100"> | <img src="photo_6x4in.jpg" width="200"> |



## Steps to create a passport photo from scratch:
1. Take a picture of a person with a white background. Use flash and good lighting.
2. Upload the picture to the photo cropping tool (see the link below), align and resize the photo as necessary.
3. Crop and save the photo to your computer.
4. Use image editing software (XnView, GIMP, Photoshop, etc.) to tune the levels of brightness and contrast to make the background white. Save the edited file.
5. Run the script with the path of the saved image, the resulted photo for printing will be produced.
6. Print it on your color printer or use CVS/Walmart/etc. printing service. Make sure the photo is printed without borders, or make sure the printout is scaled to produce two 2x2" passport-size photos.


## Useful links:
- https://travel.state.gov/content/passports/en/passports/photos.html: photo cropping tool to create 600x600 px input image.
- https://www.xnview.com: correct levels, etc.
- https://stackoverflow.com/a/10649311/4143531: paste image into another image.
- https://stackoverflow.com/a/19303889/4143531: quality considerations.
- https://stackoverflow.com/a/9204506/4143531: possible usage of scikit-image.
