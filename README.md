[![Logo](Documentation/DFKI_Logo_smallest.jpg)](https://www.dfki.de/web/)

# mEx - Medical Information Extraction:

---
## Introduction:
**I**n the information extraction and natural language processing domain,
accessible datasets are crucial to reproduce and compare results.
Publicly available implementations and tools can serve as benchmark and
facilitate the development of more complex applications. However, in the
context of clinical text processing the number of accessible datasets is
scarce - and so is the number of existing tools. One of the main reasons
is the confidentiality of the data. This problem is even more evident
for non-English languages.

**I**n order to address this situation, we introduce a workbench: a
collection of German clinical text processing models. The models are
trained on a de-identified corpus of German nephrology reports and
provide promising results on in-domain data. Moreover, our models can be
also successfully applied to other biomedical text in German. Our
workbench is made publicly available, so it can be used out of the box,
as a benchmark or transferred to related problems.

---

## Notice:
This repository is only a docker deployment for the mEx models to facilitate the usage and testing, The [Originial-Repo](https://github.com/DFKI-NLP/mEx_medical_information_extraction)
is still under development and will be ready soon.

---

## Requirements:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

---

## Tutorials:
* [Tutorial 1: Usage](Documentation/Usage.md)
* [Tutorial 2: IO-Format/Example](Documentation/Example.md)


---

## mEx Models Overview:

| Task | Language | Dataset | Score | Download Model|
| -------------------------------  | ---  | ----------- | ---------------- | ------------- |
| Named Entity Recognition |German | German Nephrology Corpus (Charite)   |  **83.25** (F1)  | [*named_entity_recognition_mex_model(custom_flair_embeddings).pt*](https://cloud.dfki.de/owncloud/index.php/s/WWbnqJ6N8gQQWMD/download)|
| Relation Extraction |German | German Nephrology Corpus (Charite)   |  **84.0** (F1)  | [*relation_extraction_mex_model(Custom_Word_Concept_Relative_Embeddings).pt*](https://cloud.dfki.de/owncloud/index.php/s/cDHpdckyPx72gdY/download)|
| Part-of-Speech Tagging |German| German Nephrology Corpus (Charite)  | **98.57** (Acc.) | [*part_of_speech_tagger_mex_model(default_word_flair_embeddings).pt*](https://cloud.dfki.de/owncloud/index.php/s/e7G9deea7eRksCY/download)|

---

## Reference:

---
For more information we refer to our short publication (_a more detailed
version is currently under review_):

Roland Roller, Laura Seiffe, Ammer Ayach, Sebastian Möller, Oliver
Marten, Michael Mikhailov, Christoph Alt, Danilo Schmidt, Fabian
Halleck, Marcel Naik, Wiebke Duettmann and Klemens Budde.  [**Information
Extraction Models for German Clinical Text**](https://ieeexplore.ieee.org/document/9374385). In 2020 IEEE International
Conference on Healthcare Informatics (ICHI). Oldenburg, 2020.

### Citing:

```
@INPROCEEDINGS{9374385,  
    author={Roller, Roland and Seiffe, Laura and Ayach, Ammer and Möller, Sebastian and Marten, Oliver and Mikhailov, Michael and Alt, Christoph and Schmidt, Danilo and Halleck, Fabian and Naik, Marcel and Duettmann, Wiebke and Budde, Klemens},  
    booktitle={2020 IEEE International Conference on Healthcare Informatics (ICHI)},   
    title={Information Extraction Models for German Clinical Text},   
    year={2020},  
    pages={1-2},  
    doi={10.1109/ICHI48887.2020.9374385}
    }
```

---

# Acknowledgement:
The development of the workbench was partially supported 
by the [**European Union's Horizon 2020 research and innovation program**](https://ec.europa.eu/programmes/horizon2020/) 
under [grant agreement No 780495 (BigMedilytics)](https://cordis.europa.eu/project/id/780495)
and by the [German Federal Ministry of Economics 
and Energy](https://www.bmwi.de/Navigation/EN/Home/home.html) through the project [MACSS (01MD16011F)](http://macss.dfki.de/).

**License: CC BY-NC 4.0** 

[![License: CC BY-NC 4.0](https://i.creativecommons.org/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)
