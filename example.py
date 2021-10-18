import requests

dummy_example = [
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


pos_request = requests.post('http://localhost:5000/pos/', json={'list': dummy_example})
ner_request = requests.post('http://localhost:5000/ner/', json={'list': dummy_example})
relex_request = requests.post('http://localhost:5000/relex/', json={'list': dummy_example})


pos_response = pos_request.json()
ner_response = ner_request.json()
relex_response = relex_request.json()

print()