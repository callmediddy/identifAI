'''
NAME: Aditya Khandelwal
Project Title: IdentifAI
Class: CS106X
Section Leader: Trey Connelly
Description: This is an API and web tool that can be used to generate image hashes,
assign these hashes to owners, and 
'''

# Importing packages needed for Flask application
from flask import Flask, jsonify, render_template, request, send_from_directory, url_for
# To set basedir where uploaded images will be stored locally
import os
# For image manipulations
from PIL import Image
# For searching for similar images
from similarity_search import find_similar_image
# To call the Sightengine API
from sightengine.client import SightengineClient

# These are my personal credentials for Sightengine. I have a limit
# of 5000 queries/month, but I don't think you will be able to
# throttle that limit while testing my submission, so should work
# just fine
client = SightengineClient('144007915', 'pAaRprRoTZV5x23hWk5Q')
app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
  hists = [f for f in os.listdir('uploads') if not f.startswith('.')]
  return render_template('index.html', hists=hists)


@app.route('/upload', methods=['GET','POST'])
def upload_image():
  if request.method == 'POST':
    # Fetch file to be uploaded
    file = request.files.get('image')
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    invalidImage = False
    username = request.form.get('username')
    hashtype = request.form.get('inlineRadioOptions')
    img = Image.open(file)
    is_similar_img = find_similar_image(username, hashtype, img)
    message = ""
    if(is_similar_img == True):
      output = client.check('nudity', 'wad', 'celebrities', 'scam', 'face-attributes').set_file(filename)
      print(output)
      if output['nudity']['safe'] <= output['nudity']['partial'] and output['nudity']['safe'] <= output['nudity']['raw']:
          message = "Contains nudity."
          invalidImage = True
      # contains weapon, alcohol or drugs
      if output['weapon'] > 0.5 or output['alcohol'] > 0.2 or output['drugs'] > 0.2:
          message = "Contains weapons, alcohol or drugs."
          invalidImage = True
      # contains scammers
      if output['scam']['prob'] > 0.85:
          message = "Uploaded by a scammer"
          invalidImage = True
      # contains celebrities
      if 'celebrity' in output:
          message = "Includes a celebrity"
          if output[0]['prob'] > 0.85:
              invalidImage = True
      # contains children
      if 'attributes' in output:
          message = "Contains children"
          if output['attributes']['minor'] > 0.85:
              invalidImage = True

    if invalidImage:
        os.remove(filename)
    else:
      if is_similar_img == True:
        message = "Your photo was uploaded to the gallery!"
      else:
        message = "Your photo was denied. You are not the owner."
        invalidImage = True
    hists = [f for f in os.listdir('uploads') if not f.startswith('.')]
    return render_template('index.html', invalidImage=invalidImage, init=True, hists=hists, message=message)

  # return render_template('upload.html')

# Created this route to display images using pathnames in index.html
@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# Required to make sure that the images displayed in gallery get updated
# as soon as 
extra_files = ['index.html']

if __name__ == '__main__':
   app.run(debug=True, extra_files=extra_files)