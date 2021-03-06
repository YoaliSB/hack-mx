import requests

'''
Validate key generated by Azure Cognitive Services
'''
subscription_key = "f2b56f86ef2542eca80c4923a5d91b8e"
assert subscription_key

'''
Link to costum computer vision model that tags images 
according to whether they are organic or inorganic, and if 
they are recyclable, non'recyclable or special, e.g. batteries
Categories:
	Organica
	Inorganica, Especial
	Inorganica, Reciclable
	Inorganica , No reciclable
'''

#vision_base_url = "https://southcentralus.api.cognitive.microsoft.com/vision/v1.0/"
vision_base_url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v1.1/Prediction/3dce07fa-b6d0-423e-9747-0687b6d454f2/url?iterationId=2092dc38-06a8-4fde-8321-8f747f7a1d02"
vision_analyze_url = vision_base_url

'''
Provide an image url and send the request to analyze the image
Some hard-coded examples provided
'''
#Banana peel
image_url = 'https://www.theblaze.com/wp-content/uploads/2017/09/Banana-Peel-1280x720.jpg'
#Toilet paper
#image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Toilet_paper_orientation_over.jpg/1200px-Toilet_paper_orientation_over.jpg'
#Cans
#image_url = 'https://cdn.vox-cdn.com/thumbor/IGsqloX3dIiTgdBpaCm77pTVW_Y=/0x0:4184x2944/1200x800/filters:focal(1624x823:2292x1491)/cdn.vox-cdn.com/uploads/chorus_image/image/54823249/648299226.0.jpg'#'
#Batteries
image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Batteries.jpg/250px-Batteries.jpg'
headers  = {'Ocp-Apim-Subscription-Key': subscription_key, 'Prediction-Key':'71c9eaac238240d29fb3960af49d3bbc', 'Content-Type':'application/json' }
data     = {'url': image_url}
response = requests.post(vision_analyze_url, headers=headers, json=data)
response.raise_for_status()
analysis = response.json()
predictions = analysis['Predictions']
#print(predictions)

'''

'''
categories_list = ["Organica","Inorganica"]
sub_categories_list = ["Reciclable", "No reciclable", "Especial"]
tag_list = []
category = ''

for x in range(0, 3):
  '''
  The model is not yet trained enough to have high rates of confidence
  in its predictions so we're removing the condition for the demo, 
  but we should validate the probability of an accurate prediction for 
  a real project

  probability = predictions[x]['Probability']
  if probability >= 0.75:
  '''
  tag = predictions[x]['Tag']
  tag_list.append(tag)

for item in tag_list:
  if item in categories_list:
    category += item.lower() + " "
    tag_list.remove(item)
    break

for item in tag_list:
  if item in sub_categories_list:
    category += item.lower() + " "
    break

'''
Here we should be sending a command to the trash cans to open their respective doors, 
but we don't have physical smart devices for the prototype yet so we'll just print the result
'''
print 'Abrir compuerta de basura ' + category

