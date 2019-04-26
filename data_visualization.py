"""
Data visualization
"""
from term_frequencies import generate_term_list
from term_frequencies import calculate_term_frequencies
import vincent

filename = "/data/stream_biden.json"
term_filter = "terms_only"
terms = generate_term_list(filename, term_filter)
word_freq = calculate_term_frequencies(terms, 20)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')
