import nltk
from nltk.corpus import words
from nltk.tokenize import word_tokenize
common_words_set = set(words.words())

def is_likely_a_sentence(input_string):
    # 分词
    tokens = word_tokenize(input_string)
    # 过滤掉标点符号（这可能需要更复杂的处理，但这里作为简单示例）
    filtered_tokens = [token for token in tokens if token.isalnum()]
    # 检查每个单词是否在常见单词集中
    all_common_words = [word in common_words_set for word in filtered_tokens]
    # 简单的句子合理性检查：至少包含3个单词（这是一个非常宽松的条件）
    has_enough_words = len(filtered_tokens) >= 3
    has_enough_common_words = sum(all_common_words) >= 3
    # 返回结果（这里仅作示例，实际情况可能需要更复杂的逻辑）
    return has_enough_common_words and has_enough_words

random_string = "@llhjmd#N@$p#ojhf#b#slvmg#le#ab`lm"
print(is_likely_a_sentence(random_string))  # 应该输出 True
