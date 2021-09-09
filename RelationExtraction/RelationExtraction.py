import spacy
from spacy.tokens import Span, Doc
from flair.data import Sentence, Token
from itertools import combinations
from flair.models import TextClassifier


class RelationExtractionModel(object):
    def __init__(self):
        self.name = 'relation_extraction'
        self.clf = TextClassifier.load_from_file('relex.pt')

        self.concept_map = {'_UNK': 0, 'State_of_health': 1, 'Measurement': 2, 'Medical_condition': 3, 'Process': 4,
                            'Medication': 5, 'Dosing': 6, 'Treatment': 7, 'Person': 8, 'Time_information': 9,
                            'DiagLab_Procedure': 10, 'Local_specification': 11, 'Biological_chemistry': 12,
                            'Body_part': 13, 'Medical_device': 14, 'Biological_parameter': 15, 'Body_Fluid': 16,
                            'Medical_specification': 17}

        self.allowed_pairs = ['Biological_chemistry-Measurement', 'Body_part-Medical_condition',
                              'DiagLab_Procedure-Biological_chemistry', 'DiagLab_Procedure-Body_part',
                              'DiagLab_Procedure-Measurement', 'DiagLab_Procedure-Medical_condition',
                              'Medical_condition-Body_part', 'Medical_condition-Local_specification',
                              'Medical_condition-Measurement', 'Medical_condition-Medical_specification',
                              'Medical_condition-Time_information', 'Medication-Dosing', 'Process-Measurement',
                              'Process-State_of_health', 'Treatment-Dosing', 'Treatment-Medical_device',
                              'Treatment-Medical_specification', 'Treatment-Medication', 'Treatment-Time_information']
        self.tagger_tag_dictionary = ['<unk>', 'O', 'B-Time_information', 'I-Time_information', 'B-Treatment',
                                      'B-Body_part', 'B-State_of_health', 'B-Medical_condition', 'I-State_of_health',
                                      'B-DiagLab_Procedure', 'I-DiagLab_Procedure', 'B-Medication', 'I-Treatment',
                                      'B-Biological_chemistry', 'B-Measurement', 'I-Measurement',
                                      'B-Biological_parameter', 'B-Medical_specification', 'B-Person', 'I-Body_part',
                                      'I-Medical_condition', 'B-Process', 'B-Local_specification', 'B-Dosing',
                                      'I-Dosing', 'I-Biological_chemistry', 'I-Medication', 'I-Person',
                                      'I-Biological_parameter', 'I-Process', 'I-Local_specification', 'B-Body_Fluid',
                                      'B-Medical_device', 'I-Medical_specification', 'I-Medical_device', 'I-Body_Fluid',
                                      '<START>', '<STOP>']


        self.nlp = spacy.load('de_core_news_sm',
                              disable=['tagger', 'ner', 'textcat', 'tokenizer', 'parser', 'lemmatizer'])

        for tag in self.tagger_tag_dictionary:
            self.nlp.vocab.strings.add(tag)
            split = tag.split('-')
            # add tags without iob prefix to string store
            if len(split) == 2:
                self.nlp.vocab.strings.add(split[1])


    def create_doc(self, token_list, sent_starts_index):
        sent_starts = [False] * len(token_list)
        target = [True] * len(sent_starts_index)
        for x, y in zip(sent_starts_index, target):
            sent_starts[x] = y

        doc = Doc(self.nlp.vocab, words=token_list, spaces=[True] * (len(token_list) - 1) + [False],
                  sent_starts=sent_starts)

        return doc

    @staticmethod
    def create_tags_per_sentence(sent_starts_index, tags):
        tags_per_sent = []
        index = 0
        for i in sent_starts_index:
            tags_per_sent.append(tags[index:i])
            index = i
        tags_per_sent.append(tags[index:])

        return tags_per_sent

    def merge_iob_spans(self, doc, spans, tags):
        def create_entity_span(tokens):
            if len(tokens) > 1:
                start = tokens[0].start
                end = tokens[-1].end
                return Span(doc, start, end, label=tokens[0].label)
            elif len(tokens) == 1:
                return tokens[0]
            return None

        entity_tokens = []
        spans_for_merge = []
        for i, (span, tag) in enumerate(zip(spans, tags)):
            if tag == 'O':
                continue
            split = tag.split('-')
            if len(split) != 2 or split[0] not in ['I', 'B']:
                return False
            if split[0] == 'B':
                merge_span = create_entity_span(entity_tokens)
                if merge_span:
                    spans_for_merge.append(merge_span)
                entity_tokens = [span]
            elif tags[i - 1][1:] == tag[1:]:
                entity_tokens.append(span)
        # merge remaining entity at the end
        merge_span = create_entity_span(entity_tokens)
        if merge_span:

            spans_for_merge.append(merge_span)
        return spans_for_merge

    def add_ents_to_sents(self, doc, tags_per_sent):
        for sent, tag_list in zip(doc.sents, tags_per_sent):
            spans = []
            tags = []
            for doc_token, tag in zip(sent, tag_list):
                start = doc_token.i
                end = start + 1

                if tag != 'O':
                    _, label = tag.split('-')
                    span = Span(doc, start, end, label=self.nlp.vocab.strings[label])
                    spans.append(span)
                    tags.append(tag)

            doc.ents = list(doc.ents) + self.merge_iob_spans(doc, spans, tags)

    @staticmethod
    def _group_entities_by_sentence(doc):
        sentence_ends = [ent.end for ent in doc.sents]

        entity_groups = []
        entity_group = []
        current_sentence = 0
        for entity in doc.ents:
            if entity.end > sentence_ends[current_sentence]:
                if entity_group:
                    entity_groups.append(entity_group)
                    entity_group = []
                current_sentence += 1

            entity_group.append(entity)

        if entity_group:
            entity_groups.append(entity_group)

        return entity_groups

    @staticmethod
    def _prepare_sentence(sent, entity1, entity2, map_dict):
        def add_offset_to_sentence(sentence, span, tag):
            start, end = span
            for i, token in enumerate(sentence.tokens):
                if i >= end:
                    token.add_tag(tag, (i + 1) - end)
                elif i < start:
                    token.add_tag(tag, i - start)
                else:
                    token.add_tag(tag, 0)

        def add_concept_to_sentence(sentence, span, tag, tag_value):
            start, end = span
            for i, token in enumerate(sentence.tokens):
                if i >= end:
                    token.add_tag(tag, 0)
                elif i < start:
                    token.add_tag(tag, 0)
                else:
                    token.add_tag(tag, tag_value)

        sentence: Sentence = Sentence()
        for token in sent:
            sentence.add_token(Token(token.text))

        # print(entity1.label_, entity2.label_)
        sent_offset = sent.start
        add_offset_to_sentence(sentence, (entity1[0].start - sent_offset, entity1[0].end - sent_offset), tag='offset_e1')
        add_offset_to_sentence(sentence, (entity2[0].start - sent_offset, entity2[0].end - sent_offset), tag='offset_e2')

        add_concept_to_sentence(sentence, (entity1[0].start - sent_offset, entity1[0].end - sent_offset), tag='concept_1',
                                tag_value=map_dict[entity1[0].label_])
        add_concept_to_sentence(sentence, (entity2[0].start - sent_offset, entity2[0].end - sent_offset), tag='concept_2',
                                tag_value=map_dict[entity2[0].label_])

        return sentence

    def predict(self, token_list, sent_starts_index, tags):

        def swap_entities(relation):
            return relation[-6:-1].lower() == 'e2,e1'

        def relation_name(relation):
            return relation[:-7]

        def negative_relation(relation):
            return relation.lower().startswith('rel-not_')

        doc = self.create_doc(token_list, sent_starts_index)


        tags_per_sent = self.create_tags_per_sentence(sent_starts_index, tags)
        self.add_ents_to_sents(doc, tags_per_sent)

        entity_groups = self._group_entities_by_sentence(doc)
        sentences = []
        entity_combinations = []


        ner_res = []
        ner_res_2 = []
        i_index = 0
        t_id = 1
        for sentence, entities in zip(doc.sents, entity_groups):
            tmp_ner_res = []
            for entity in entities:
                if (entity.end - entity.start) > 1:

                    tmp_ner_res.append([entity, "T" + str(t_id), "Sent-" + str(i_index), "Tok-" + str(entity.start - sentence.start), "Tok-" + str(entity.end - sentence.start - 1), entity.label_])
                    ner_res_2.append(["T" + str(t_id), "Sent-" + str(i_index), "Tok-" + str(entity.start - sentence.start), "Tok-" + str(entity.end - sentence.start - 1), entity.label_])
                else:
                    tmp_ner_res.append([entity, "T" + str(t_id), "Sent-" + str(i_index), "Tok-" + str(entity.start - sentence.start), "Tok-" + str(entity.start - sentence.start), entity.label_])
                    ner_res_2.append(["T" + str(t_id), "Sent-" + str(i_index), "Tok-" + str(entity.start - sentence.start), "Tok-" + str(entity.start - sentence.start), entity.label_])

                t_id += 1

            ner_res.extend(tmp_ner_res)

            for entity_left, entity_right in combinations(tmp_ner_res, r=2):
                if (entity_left[0].label_ + '-' + entity_right[0].label_ in self.allowed_pairs) or (
                        entity_right[0].label_ + '-' + entity_left[0].label_ in self.allowed_pairs):
                    sentences.append(self._prepare_sentence(sentence, entity_left, entity_right, self.concept_map))
                    entity_combinations.append((entity_left, entity_right))


            #for entity_left, entity_right in combinations(entities, r=2):
            #    if (entity_left.label_ + '-' + entity_right.label_ in self.allowed_pairs) or (
            #            entity_right.label_ + '-' + entity_left.label_ in self.allowed_pairs):
            #        sentences.append(self._prepare_sentence(sentence, entity_left, entity_right, self.concept_map))
            #        entity_combinations.append((entity_left, entity_right))
            i_index += 1

        pred_sentences = self.clf.predict(sentences)

        rel_res = []
        rel_id = 1
        for sent, (ent1, ent2) in zip(pred_sentences, entity_combinations):
            relation = sent.labels[0].name

            if not negative_relation(relation):
                if swap_entities(relation):
                    rel_res.append(["Rel-"+str(rel_id), ent2[1], ent1[1], relation])
                    rel_id += 1
                else:
                    rel_res.append(["Rel-"+str(rel_id), ent1[1], ent2[1], relation])
                    rel_id += 1

        return {"ner_res": ner_res_2, "rel_res": rel_res}


if __name__ == '__main__':
    tokens = ['Seit', '2', 'Wochen', 'depressive', 'Symptomatik', '.', 'Hat', 'Schmerzen', 'und', 'Engegefühl', 'im', 'Brust', 'ohne', 'Dyspnoe', 'bei', 'unauffälligem', 'EKG-Befund', 'und', 'normaler', 'Labor', '.', 'Vorstellung', 'bei', 'Psychosomatik', 'nächste', 'Woche', 'am', '12.12.2012', '.', 'Kreatinin', 'auf', '1,0', 'abgefallen', '.', 'Prograf', 'planmäßig', 'reduziert', ',', 'Urbason', 'reduziert', '.', 'Sono-Tx', ':', 'iO', '.']
    tags = ['B-Time_information', 'I-Time_information', 'I-Time_information', 'B-Medical_condition', 'I-Medical_condition', 'O', 'O', 'B-Medical_condition', 'O', 'B-Medical_condition', 'O', 'B-Body_part', 'O', 'B-Medical_condition', 'O', 'B-State_of_health', 'B-DiagLab_Procedure', 'O', 'B-State_of_health', 'B-DiagLab_Procedure', 'O', 'B-Treatment', 'I-Treatment', 'I-Treatment', 'B-Time_information', 'I-Time_information', 'O', 'B-Time_information', 'O', 'B-Biological_chemistry', 'O', 'B-Measurement', 'I-Measurement', 'O', 'B-Medication', 'O', 'B-Treatment', 'O', 'B-Medication', 'B-Treatment', 'O', 'B-DiagLab_Procedure', 'O', 'B-State_of_health', 'O']
    sent_start_index = [6, 21, 29, 34, 41, 43]
    obj = RelationExtractionModel()
    c = obj.predict(tokens, sent_start_index, tags)
    print()
