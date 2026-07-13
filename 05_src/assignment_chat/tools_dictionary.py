from langchain.tools import tool
import json
import requests

@tool
def get_definition(s:str=""):
   """
   Returns definition of the word s from Free Dictionary API.
   """
 
   url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + s
   response = requests.get(url)
   resp_dict = json.loads(response.text)
   definition = resp_dict[0]['meanings'][0]['definitions'][0]['definition']
   return definition