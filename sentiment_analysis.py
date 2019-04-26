"""
Sentiment Analysis
"""
from collections import defaultdict
from term_frequencies import generate_term_list
from term_frequencies import calculate_term_frequencies
from term_frequencies import term_co_occurrences


filename = "data/stream_avengers.json"
term_filter = "single_stop_words"
term_list = generate_term_list(filename, term_filter)
count_stop_single = calculate_term_frequencies(term_list, 20)
com = term_co_occurrences(term_list, 20)
print(com)
# n_docs is the total n. of tweets
p_t = {}
p_t_com = defaultdict(lambda: defaultdict(int))

for term, n in count_stop_single.items():
    p_t[term] = n / n_docs
    for t2 in com[term]:
        p_t_com[term][t2] = com[term][t2] / n_docs
