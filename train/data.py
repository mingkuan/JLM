import pickle
import numpy as np
import os
import sys
from collections import defaultdict
from tqdm import tqdm

sys.path.append('..')
from config import get_configs, experiment_path, data_path


sys.path.append('..')
from config import experiment_path, experiment_id

class Vocab(object):
    def __init__(self, size):
        lexicon = pickle.load(open(os.path.join(data_path, 'lexicon.pkl'), 'rb'))[:size]
        # put unk to top.
        # otherwise, if freq if provided, sort with freq
        lexicon = [('<unk>', 0)] + lexicon
        self.w2i = {x[0]:i for i, x in enumerate(lexicon)}
        self.i2w = {v:k for k,v in self.w2i.items()}
        print('vocab with size {} loaded'.format(size))

    def __len__(self):
        return len(self.w2i)

class Corpus(object):
    def __init__(self, vocab, debug=False):
        self.vocab = vocab
        self.encoded_train = self.encode_corpus('train.txt', debug)
        self.encoded_dev = self.encode_corpus('dev.txt', debug)
        self.encoded_test = self.encode_corpus('test.txt', debug)

    def encode_corpus(self, filename, debug=False):
        encoded = []
        print('encode corpus: {}'.format(filename))
        with open(os.path.join(data_path, filename), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if debug:
                lines = lines[:1024*100]
            for line in tqdm(lines):
                words = line.strip().split(' ')
                encoded += [self.vocab.w2i[x] if x in self.vocab.w2i else self.vocab.w2i['<unk>'] for x in words] \
                          + [self.vocab.w2i['<eos>']]
        return encoded
'''
Pack the compressed embeddings into a pickle again  
'''
def build_compressed_embedding_pkl(name):
    embeddings = []
    weights_dir = os.path.join(experiment_path, str(experiment_id), "weights")
    with open(os.path.join(weights_dir, name), 'r') as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.strip().split()
            v = [float(x) for x in tokens[1:]]
            embeddings.append(v)

    LM= np.array(embeddings)
    pickle.dump(LM, open(os.path.join(weights_dir, "CLM.pkl"), "wb"))

    print('LM size {} dumped'.format(LM.shape))

if __name__ == "__main__":
    # test the model
    # build_compressed_embedding_pkl('embedding.txt.comp')
    vocab = Vocab(50000)
    corpus = Corpus(vocab, debug=True)
    print([vocab.i2w[x] for x in corpus.encoded_train][:100])
