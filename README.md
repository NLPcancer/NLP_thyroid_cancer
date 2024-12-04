# Annotation-guided NLP models for thyroid cancer staging and risk level classification using large language models
This page is to provide the technical information for the article "Annotation-guided NLP models for thyroid cancer staging and risk level classification using large language models", which aims to extract disease information using open source LLMs via Ollama by using different types of prompt, and classify ATA risk and AJCC 8th edition cancer staging using pre-written classification rules.

## Requirement
### Installation of Ollama
Download and install Ollama according to your operation system.

#### MacOS
<a href="https://ollama.com/download/Ollama-darwin.zip">Download</a>

#### Windows
<a href="https://ollama.com/download/OllamaSetup.exe">Download</a>

#### Linux
```sh
curl -fsSL https://ollama.com/install.sh | sh
```

Check out more at the Ollama offical website (<a href="https://ollama.com/">link</a>).

### Large Language Models via Ollama
The list of Ollama LLM models used in the study is listed in 'model_list.txt'.

Pull (download) the models you wish to use by running 'ollama pull' commands.

e.g.
```sh
ollama pull gemma2:9b-instruct-fp16
```


### Python libraries
Install the required python libraries through 'requirement.txt'.
```sh
pip install -r requirements.txt
```

## Clinical notes
The operation records and pathology reports for 35 pseudo cases could be found in the folder "sample".

The TCGA pathology reports (50 for few-shot prompting and 289 for validation) could be found in the Genomic Data Commons data portal of National Cancer Institute (<a href="https://portal.gdc.cancer.gov/projects/TCGA-THCA">link</a>).

## Extraction of data from clinical notes using LLMs
The Python scripts for extraction of disease information from clinical notes could be found in the folder "scripts".
Eight prompting strategies have been proposed, and their corresponding file names of the script are as follow:
| Prompting strategies  | File name |
| ------------- | ------------- |
| Zero-shot prompting  | zeroshot.py  |
| COT  | cot.py |
| Few-shot prompting with all annotated data  | fewshot_all_data.py  |
| Few-shot prompting with non-repeated annotated data  | fewshot_trim_data.py  |
| Few-shot prompting with part of annotated data  | fewshot_part_data.py  |
| COT and few-shot prompting with all annotated data  | cot_fewshot_all_data.py  |
| COT and few-shot prompting with non-repeated annotated data  | cot_fewshot_trim_data.py  |
| COT and few-shot prompting with part of annotated data  | cot_fewshot_part_data.py  |

By default, Gemma 2 9B Instruct model is demonstrated in the scripts.
Any model could be chosen in the script file.

To run the script (e.g. zero-shot prompting), simply run:
```sh
python zeroshot.py
```

After extraction, a CSV file named 'output.csv' will be created in the resposity.

## Classification of risk and cancer staging
The templates of the pre-written classification rules could be found in the folder "classification".
After extraction of data, paste the data from the 'output.csv' to the sheet "Model output" to obtain the classification results in the sheet "Classification result".

## Enquiry
For any enquiry, please contact Dr. Carlos Wong (carloswong@d24h.hk) or Laboratory of Data Discovery for Health (D²4H) (info@d24h.hk).
