# 2) IO-Format / Example:

Under the following address:

```shell
http://localhost:5000/
```

Following endpoints are available:
* SequenceTaggers
  - http://localhost:5000/pos/
  - http://localhost:5000/ner/
* RelationExtraction
  - http://localhost:5000/relex/

---

## Input / Output Format:

---

### Input:
JSON is used as input format and uses a unified input-model for all API-Endpoints (POS, NER, RelEx).

The Input is a nested list of lists: A list of tokenized sentences represented as a list of tokens.


```python
model = app.model('Taggers Input', {'list': fields.List(fields.List(fields.String()))})
```

#### Input-Model:
```js
{
  "list": [ # List of tokenized sentences
    # 1.Sentence
    [  
      "Token 1",
      "Token 2",
      "Token 3"
    ],
    # 2.Sentence
    [
      "Token 1",
      "Token 2",
      "Token 3",
      "Token 4"            
    ],
    .
    .
    .
    .
    .
    # nth.sentence
    [
      "Token 1",
      "Token 2",
      "Token 3",
          .
          .
          .
          .
          .
      "Token n"
    ]
  ]
}
```

---

### Try-out Example: on (localhost:5000)

This example works for all API endpoints on http://localhost:5000/


```json
{
    "list":[
        [
            "Seit",
            "2",
            "Wochen",
            "depressive",
            "Symptomatik",
            "."
        ],
        [
            "Hat",
            "Schmerzen",
            "und",
            "Engegefühl",
            "im",
            "Brust",
            "ohne",
            "Dyspnoe",
            "bei",
            "unauffälligem",
            "EKG-Befund",
            "und",
            "normaler",
            "Labor",
            "."
        ],
        [
            "Vorstellung",
            "bei",
            "Psychosomatik",
            "nächste",
            "Woche",
            "am",
            "12.12.2012",
            "."
        ],
        [
            "Kreatinin",
            "auf",
            "1,0",
            "abgefallen",
            "."
        ],
        [
            "Prograf",
            "planmäßig",
            "reduziert",
            ",",
            "Urbason",
            "reduziert",
            "."
        ],
        [
            "Sono-Tx",
            ":"
        ],
        [
            "iO",
            "."
        ]
    ]
}
```

## Output: 


### SequenceTaggers:

#### **/pos/**  & **/ner** endpoints:

The output of the part-of-speech tagger model is a list of tags, each element includes:

- Tag-ID
- Sentence index
- Start Token index
- End Token index
- Tag


```json
{
  "tags": [
    [
      "T1",
      "Sent-0",
      "Tok-0",
      "Tok-0",
      "Tag-x"
    ],
    [
      "T2",
      "Sent-0",
      "Tok-1",
      "Tok-1",
      "Tag-x"
    ],
    [
      "T3",
      "Sent-0",
      "Tok-2",
      "Tok-2",
      "Tag-x"
    ],
    [
      "T7",
      "Sent-1",
      "Tok-0",
      "Tok-0",
      "Tag-x"
    ],
    [
      "T22",
      "Sent-2",
      "Tok-0",
      "Tok-0",
      "Tag-x"
    ],
    [
      "T23",
      "Sent-2",
      "Tok-1",
      "Tok-3",
      "Tag-x"
    ]
  ]
}
```

### RelationExtraction:

#### /relex/ endpoint:

This endpoint is for the Relation Extraction Model, in the backend the NER will be used to generate the 
ner-tags which are then used to run the relation extraction on the given input.

The output will be a dictionary including 2 entries:

* ner_tags: The content on ner_tags is explained [as above]()
* relations: a list of relations each element includes:
    - Relation-ID
    - Relation-From (Token-ID)
    - Relation-To (Token-ID)
    - Relation Name

The direction of the relations always goes from the first token to the second one.


The token ids could be mapped back to Named-Entities in the ner_tags list.


```json
{
  "ner_tags": [
    [
      "T1",
      "Sent-0",
      "Tok-0",
      "Tok-2",
      "Time_information"
    ],
    [
      "T2",
      "Sent-0",
      "Tok-3",
      "Tok-4",
      "Medical_condition"
    ],
    [
      "T3",
      "Sent-1",
      "Tok-1",
      "Tok-1",
      "Medical_condition"
    ],
    [
      "T4",
      "Sent-1",
      "Tok-3",
      "Tok-3",
      "Medical_condition"
    ],
    [
      "T5",
      "Sent-1",
      "Tok-5",
      "Tok-5",
      "Body_part"
    ],
    [
      "T6",
      "Sent-1",
      "Tok-7",
      "Tok-7",
      "Medical_condition"
    ],
    [
      "T7",
      "Sent-1",
      "Tok-9",
      "Tok-9",
      "State_of_health"
    ],
    [
      "T8",
      "Sent-1",
      "Tok-10",
      "Tok-10",
      "DiagLab_Procedure"
    ],
    [
      "T9",
      "Sent-1",
      "Tok-12",
      "Tok-12",
      "State_of_health"
    ],
    [
      "T10",
      "Sent-1",
      "Tok-13",
      "Tok-13",
      "DiagLab_Procedure"
    ],
    [
      "T11",
      "Sent-2",
      "Tok-0",
      "Tok-2",
      "Treatment"
    ],
    [
      "T12",
      "Sent-2",
      "Tok-3",
      "Tok-4",
      "Time_information"
    ],
    [
      "T13",
      "Sent-2",
      "Tok-6",
      "Tok-6",
      "Time_information"
    ],
    [
      "T14",
      "Sent-3",
      "Tok-0",
      "Tok-0",
      "Biological_chemistry"
    ],
    [
      "T15",
      "Sent-3",
      "Tok-2",
      "Tok-3",
      "Measurement"
    ],
    [
      "T16",
      "Sent-4",
      "Tok-0",
      "Tok-0",
      "Medication"
    ],
    [
      "T17",
      "Sent-4",
      "Tok-2",
      "Tok-2",
      "Treatment"
    ],
    [
      "T18",
      "Sent-4",
      "Tok-4",
      "Tok-4",
      "Medication"
    ],
    [
      "T19",
      "Sent-4",
      "Tok-5",
      "Tok-5",
      "Treatment"
    ],
    [
      "T20",
      "Sent-5",
      "Tok-0",
      "Tok-0",
      "DiagLab_Procedure"
    ],
    [
      "T21",
      "Sent-6",
      "Tok-0",
      "Tok-0",
      "State_of_health"
    ]
  ],
  "relations": [
    [
      "Rel-1",
      "T2",
      "T1",
      "rel-has_time_info(e2,e1)"
    ],
    [
      "Rel-2",
      "T3",
      "T5",
      "rel-is_located(e1,e2)"
    ],
    [
      "Rel-3",
      "T4",
      "T5",
      "rel-is_located(e1,e2)"
    ],
    [
      "Rel-4",
      "T11",
      "T12",
      "rel-has_time_info(e1,e2)"
    ],
    [
      "Rel-5",
      "T14",
      "T15",
      "rel-has_measure(e1,e2)"
    ],
    [
      "Rel-6",
      "T17",
      "T16",
      "rel-involves(e2,e1)"
    ],
    [
      "Rel-7",
      "T19",
      "T18",
      "rel-involves(e2,e1)"
    ]
  ]
}
```

---