from email import message
from googleapiclient import discovery
from dotenv import load_dotenv
import os
from googleapiclient.errors import HttpError
load_dotenv()

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=os.getenv('API_KEY'),
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)
attributes = {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}, 'PROFANITY': {}, 'THREAT':{}}

def api_response(text):
  analyze_request = {
  'comment': { 'text': text },
  'requestedAttributes': attributes
  }
  try:
    response = client.comments().analyze(body=analyze_request).execute()
  except HttpError as err:
    print(err)
    return None
  max_score = 0.0
  atype = None
  for attribute in attributes.keys():
      attributes[attribute]['score'] = response['attributeScores'][attribute]['summaryScore']['value']
      if attributes[attribute]['score'] >= max_score:
          max_score = attributes[attribute]['score']
          atype = attribute
  print(str(attributes) + "\n" + text)
  if max_score >= 0.65:
    return atype
  elif max_score >= 0.50:
    return "SLIGHT " + atype
