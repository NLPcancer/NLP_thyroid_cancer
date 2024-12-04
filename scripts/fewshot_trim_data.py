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
    text = fd.readlines()
    fd.close
    
    template = """
              Read the clinical note or operation record.
              Return one string for each item listed below in JSON format.
              If the information is not mentioned, return "".
              
              "Date of clinical note or operation";
              "Age of patient" - Return the result without unit;
              "Primary tumor staging (pT)" - Return "TX", "T1", "T1a", "T1b", "T2", "T3", "T4", "T4a" or "T4b" if the pT was mentioned in the clinical note, otherwise do not return;
              "Regional lymph node staging (pN)" - Return "NX", "N0", "N1", "N1a" or "N1b" if the pN was mentioned in the clinical note, otherwise do not return;
              "Distant metastasis staging (pM)"- Return "MX", "M0" or "M1" if the pM was mentioned in the clinical note, otherwise do not return;
              "Site of involved lymph nodes" - Examples include location ("Left", "right", "central", "lateral", "unilateral", "bilateral", "contralateral", "superior" and "deep"), site ("pretracheal", "paratracheal, and prelaryngeal/delphian", "thyroid lobe", "thyroid gland", "compartment", "neck", "peri-thyroid", "mediastinal tissue", "cervical", "cricothyroid", "retropharyngeal" and "traceheoesophageal groove") and level ("1", "1-B" , "I", "one", "2", "2-A", "II", "two", "3", "III", "three", "4", "four", "IV", "5", "V", "five", "6", "six", "VI", "7", "seven" and "VII");
              "Site of distant metastasis" - Examples include "Right femur" and "C6 soft tissue";
              "Number of lymph node identified" - Return the total number only;
              "Number of involved lymph node" - Return the total number only;
              "Largest dimension of involved lymph node" - Return the largest result with unit;
              "Histologic type of thyroid cancer" - Do not return subtype or variant in this field, examples include "papillary" and "follicular";
              "Histologic subtype or variant of thyroid cancer" - Do not return histologic type in this field, examples include "classic", "microcarcinoma", "follicular", "usual", "papillary", "conventional", "tall cell", "encapsulated", "encapsulated follicular", "oncocytic", "ANGIOINVASIVE", "ENCAPSULATED ONCOCYTIC FOLLICULAR", "poorly differentiated" and "diffuse sclerosing";
              "Largest dimension of tumor" - Return the largest result with unit;
              "Number of tumor";
              "Vascular invasion" - Positive examples include "Indeterminate", "Present" and "Focal Invasion", and negative examples include "Not identified", "Negative" and "Absent";
              "Extensiveness of vascular invasion" - Examples include "4 or more", "less than 4" and "<4";
              "Capsular invasion" - Positive examples include "Present", "Partially surrounded", "invade perithyroid tissue", "Focal invasion", "invades into posterior left lobe capsule", "Indeterminate", "not entirely encapsulated" and "IDENTIFIED", and negative examples include "negative", "None Identified", "within the thyroid capsule",	"Absent", "not applicable", "Not identified", "No extracapsular extension" and "Cannot be accessed";
              "Extrathyroidal extension" - Positive examples include "Present", "invading into the region of the recurrent laryngeal nerve", "Invades: perithyroid skeletal muscle", "WITH MICROSCOPIC EXTRATHYROIDAL EXTENSION", "invades subcutaneous soft tissues", "invades larynx", "invades trachea", "invades esophagus", "invades recurrent laryngeal nerve", "IS SEEN", "minimal", "EXTENDING TO PERITHYROIDAL ADIPOSE TISSUE", "extentive invasion into perithyroidal soft tissues with invasion of skeletal muscle", "identified" and "lnvades: into adjacent perithyroid fibroadipose tissue", and negative example includes "Not identified";
              "Gene mutation test performed" - Examples of mutation include "BRAF", "BRAF V600E", "NRAS61", "HRAS61", and "KRAS12/13";
              "Gene mutation type identified" - Examples of mutation include "BRAF", "BRAF V600E", "NRAS61", "HRAS61", and "KRAS12/13";
              "Margin involved" - Positive examples include "Margins involved", "Carcinoma extensively involves", "Positive", "Tumor is present", "carcinoma involves the resection margin", "Microcarcinoma (0.8 cm) is less than 0.5 mm from cauterized surgical margin", "posterior", "inferior", "superior", "anterior" and "RIGHT ANTERIOR", and negative examples include "Margins uninvolved", "Free of tumor" and "Negative".
              
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