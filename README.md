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
The operation records and pathology reports for 35 pseudo cases could be found in the folder "Clinical note".

The TCGA pathology reports (50 for few-shot prompting and 289 for validation) could be found in the Genomic Data Commons data portal of National Cancer Institute (<a href="https://portal.gdc.cancer.gov/projects/TCGA-THCA">link</a>).

## Prompt to LLM
The Python scripts which include the prompts to LLMs could be found in the folder "Script".

## Enquiry
For any enquiry, please contact Dr. Carlos Wong (carloswong@d24h.hk) or Laboratory of Data Discovery for Health (D²4H) (info@d24h.hk).
