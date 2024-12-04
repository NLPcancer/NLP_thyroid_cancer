import os             
import glob
import json
import json_normalize
import pandas as pd
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import JsonOutputParser

path = "./sample" # Set directory of the note
all_files = os.listdir(path) # Read all file in the directory

txt_files = filter(lambda x: x[-4:] == '.txt', all_files) # Filter only .txt file
txt_files = glob.glob("sample/*.txt") # Adding the path to the array
txt_files.sort()

df = {} # Create an empty JSON object to store LLM output
df = pd.json_normalize(df) # Convert to DataFrame format

# A loop to read the text in all .txt files, and extract information for LLM model
for x in txt_files:
  with open(x, 'rt') as fd:
    text = fd.read()
    fd.close
    
    template = """
              Let's think step by step.
              
              Read the clinical note or operation record.
              Return one string for each item listed below in JSON format.
              If the information is not mentioned, return "".
              
              "Date of clinical note or operation";
              "Age of patient" - Return the result without unit;
              "Primary tumor staging (pT)" - Return "TX", "T1", "T1a", "T1b", "T2", "T3", "T4", "T4a" or "T4b" if the pT was mentioned in the clinical note, otherwise do not return;
              "Regional lymph node staging (pN)" - Return "NX", "N0", "N1", "N1a" or "N1b" if the pN was mentioned in the clinical note, otherwise do not return;
              "Distant metastasis staging (pM)"- Return "MX", "M0" or "M1" if the pM was mentioned in the clinical note, otherwise do not return;
              "Site of involved lymph nodes";
              "Site of distant metastasis";
              "Number of lymph node identified" - Return the total number only;
              "Number of involved lymph node" - Return the total number only;
              "Largest dimension of involved lymph node" - Return the largest result with unit;
              "Histologic type of thyroid cancer" - Do not return subtype or variant in this field;
              "Histologic subtype or variant of thyroid cancer" - Do not return histologic type in this field;
              "Largest dimension of tumor" - Return the largest result with unit;
              "Number of tumor";
              "Vascular invasion";
              "Extensiveness of vascular invasion";
              "Capsular invasion";
              "Extrathyroidal extension";
              "Gene mutation test performed";
              "Gene mutation type identified";
              "Margin involved".
              
              Clinical note: {text}
           """
           
    prompt = PromptTemplate(template=template, input_variables=["text"])
    model = OllamaLLM(model="gemma2:9b-instruct-fp16",
                      temperature=0.00,
                      num_ctx=16384,
                      rope_freq_base=0.00, rope_freq_scale=0.00,
                      callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
                      
    parser = JsonOutputParser()
    chain = prompt | model | parser

    ans = chain.invoke(text)
    json_ans = json.dumps(ans, indent=4)
    json_load = json.loads(json_ans)
    
    doc_id = x
    doc_id = doc_id.replace(".txt", "")
    doc_id = doc_id.replace("sample/", "")
    doc_id_json = json.loads('{"ID": ' + json.dumps(doc_id) + '}')
    
    jsonMerged = dict(list(doc_id_json.items()) + list(json_load.items()))
    df_ans = pd.json_normalize(jsonMerged)
    sep_file = "./output/" + doc_id + ".csv"
    df_ans.to_csv(sep_file, index=False, encoding='utf-8')
    df = pd.concat([df, df_ans])
    df.to_csv('./output/inter.csv', index=False, encoding='utf-8')

df = df.iloc[1:] # Delete the first row of data (empty row)
df.to_csv('output.csv', index=False, encoding='utf-8') # Save as a CSV file