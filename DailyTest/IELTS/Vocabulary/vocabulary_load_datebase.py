import sqlalchemy
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from DailyTest.IELTS.database_connect import MySQLConnect, models


# $$$自然地理
# +++
# atmosphere|n.|大气层；氛围|The approaching examination created a tense atmosphere on the campus
# hydrosphere|n.|水圈；大气中的水汽|All the water in the earth's surface is included in the hydrosphere
# lithosphere|n.|岩石圈|The lithosphere and the hydrosphere together form the earth's surface
# ---
# oxygen|n.|

def get_ori_data():
    filename = 'vocabulary.txt'
    with open(file=filename, mode='r') as f:
        lines = f.readlines()
        return lines


def safe_split_and_slice(string, delimiter, target_length):
    parts = string.split(delimiter)
    return [parts[i] if i < len(parts) else '' for i in range(target_length)]


def get_parts_of_speech_meaning(string):
    parts_of_speech_map = {
        "n.": ("noun", "名词"),
        "v.": ("verb", "动词"),
        "adj.": ("adjective", "形容词"),
        "adv.": ("adverb", "副词"),
        "pron.": ("pronoun", "代词"),
        "prep.": ("preposition", "介词"),
        "conj.": ("conjunction", "连词"),
        "interj.": ("interjection", "感叹词"),
        "art.": ("article", "冠词"),
        "det.": ("determiner", "限定词"),
        "aux.": ("auxiliary verb", "助动词"),
        "modal": ("modal verb", "情态动词"),
        "ger.": ("gerund", "动名词"),
        "part.": ("participle", "分词"),
        "inf.": ("infinitive", "不定式"),
        "num.": ("numeral", "数词"),
        "cl.": ("clause marker", "从属连词或引导词"),
        "rel. pron.": ("relative pronoun", "关系代词"),
        "poss. pron.": ("possessive pronoun", "物主代词"),
        "dem. pron.": ("demonstrative pronoun", "指示代词"),
        "refl. pron.": ("reflexive pronoun", "反身代词"),
        "int. pron.": ("intensive pronoun", "强调代词"),
        "quant.": ("quantifier", "量词"),
        "prop. n.": ("proper noun", "专有名词"),
        "comm. n.": ("common noun", "普通名词"),
        "phr. v.": ("phrasal verb", "短语动词"),
        "part.": ("particle", "小品词"),
        "expl.": ("expletive", "填充词"),
        "ger.-part.": ("gerund-participle", "动名词和分词结合"),
        "inf. mark.": ("infinitive marker", "不定式标志"),
        "predet.": ("predeterminer", "前限定词"),
        "postp.": ("postposition", "后置词"),
        "contr.": ("contraction", "缩略形式"),
        "ellip.": ("ellipsis marker", "省略标志"),
        "cop.": ("copula", "系动词"),
    }

    def get_pos_value(pos):
        if pos in parts_of_speech_map.keys():
            pos_whole = parts_of_speech_map[pos][0]
            pos_chn = parts_of_speech_map[pos][1]
            return pos_whole, pos_chn

    # n./v.
    if '/' in string:
        pos_list = string.split('/')
        pos_whole_list = []
        pos_chn_list = []
        for pos in pos_list:
            res_temp = get_pos_value(pos)
            pos_whole_list.append(res_temp[0])
            pos_chn_list.append(res_temp[1])
        pos_whole_str = '/'.join(pos_whole_list)
        pos_chn_str = '/'.join(pos_chn_list)
        return pos_whole_str, pos_chn_str
    else:
        res = get_pos_value(string)
    return res


def data_extract(lines):
    vocabulary_table_dict = {}
    vocabulary_table_list = []
    sort = ''
    for line in lines:
        if line.startswith('+++') or line.startswith('---') or line.startswith('==='):
            pass
        elif line.startswith('$$$'):
            sort = line.replace('$$$', '').strip()
            vocabulary_table_list = []
            vocabulary_table_dict[sort] = []
        else:
            vocabulary_fac_list = []
            line_parts = safe_split_and_slice(line, '|', 4)
            vocabulary = line_parts[0].strip()
            parts_of_speech = line_parts[1].strip()
            pos_pair = get_parts_of_speech_meaning(parts_of_speech)
            if pos_pair:
                parts_of_speech_eng = pos_pair[0].strip()
                parts_of_speech_chn = pos_pair[1].strip()
            else:
                parts_of_speech_eng = ''
                parts_of_speech_chn = ''
            meaning = line_parts[2].strip()
            example_sentence = line_parts[3].strip()
            vocabulary_fac_list.append(vocabulary)
            vocabulary_fac_list.append(parts_of_speech)
            vocabulary_fac_list.append(parts_of_speech_eng)
            vocabulary_fac_list.append(parts_of_speech_chn)
            vocabulary_fac_list.append(meaning)
            vocabulary_fac_list.append(example_sentence)
            if sort:
                vocabulary_table_list.append(vocabulary_fac_list)
                vocabulary_table_dict[sort] = vocabulary_table_list
    return vocabulary_table_dict


def database_writer(vocabulary_table_dict):
    session = MySQLConnect.get_session()
    for sort, voc_list in vocabulary_table_dict.items():
        for voc in voc_list:
            insert_stmt = insert(models.t_ielts_vocabulary).values(
                vocabulary=voc[0],
                parts_of_speech=voc[1],
                parts_of_speech_eng=voc[2],
                parts_of_speech_chn=voc[3],
                meaning=voc[4],
                example_sentence=voc[5],
                sort=sort
            )
            try:
                session.execute(insert_stmt)
                session.commit()
            except SQLAlchemyError as e:
                print(f"An error occurred: {e}")
    MySQLConnect.session_close(session)


data = data_extract(get_ori_data())
database_writer(data)
