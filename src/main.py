#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse, logging
import numpy as np
import struc2vec
from gensim.models import Word2Vec


import graph

logging.basicConfig(filename='struc2vec.log',filemode='w',level=logging.DEBUG,format='%(asctime)s %(message)s')

def parse_args():
	'''
	Parses the node2vec arguments.
	'''
	parser = argparse.ArgumentParser(description="Run struc2vec.")

	parser.add_argument('--input', nargs='?', default='graph/karate.edgelist',
	                    help='Input graph path')

	parser.add_argument('--output', nargs='?', default='emb/karate.emb',
	                    help='Embeddings path')

	parser.add_argument('--dimensions', type=int, default=128,
	                    help='Number of dimensions. Default is 128.')

	parser.add_argument('--walk-length', type=int, default=80,
	                    help='Length of walk per source. Default is 80.')

	parser.add_argument('--walk-length-balls', type=int, default=80,
	                    help='Length of walk per source. Default is 80.')

	parser.add_argument('--num-walks', type=int, default=10,
	                    help='Number of walks per source. Default is 10.')

	parser.add_argument('--window-size', type=int, default=10,
                    	help='Context size for optimization. Default is 10.')

	parser.add_argument('--k', type=int, default=50,
                    	help='')

	parser.add_argument('--until-layer', type=int, default=2,
                    	help='Calcula até a camada.')

	parser.add_argument('--iter', default=5, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--workers', type=int, default=4,
	                    help='Number of parallel workers. Default is 8.')

	parser.add_argument('--weighted', dest='weighted', action='store_true',
	                    help='Boolean specifying (un)weighted. Default is unweighted.')
	parser.add_argument('--unweighted', dest='unweighted', action='store_false')
	parser.set_defaults(weighted=False)

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	return parser.parse_args()

def read_graph():
	'''
	Reads the input network in networkx.
	'''
	logging.info(" - Carregando matriz de adjacência para Grafo (na memória)...")
	#G = graph.load_adjacencylist(args.input,undirected=True)
	G = graph.load_edgelist(args.input,undirected=True)
	logging.info(" - Convertendo grafo para Dict (na memória)...")
	dictG = G.gToDict()

	return dictG

def learn_embeddings(walks):
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''
	logging.info("Iniciando criação das representações...")
	walks = [map(str, walk) for walk in walks]
	model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, hs=1, sg=1, workers=args.workers, iter=args.iter)
	#model = Word2Vec(walks, size=args.dimensions, window=args.window_size, min_count=0, sg=1, workers=args.workers)
	model.save_word2vec_format(args.output)
	logging.info("Representações criadas e salvas com sucesso.")
	
	return

def main(args):
	'''
	Pipeline for representational learning for all nodes in a graph.
	'''
	G = read_graph()
	G = struc2vec.Graph(G, args.directed, args.workers,calcUntilLayer=args.until_layer)
	#G.calc_diameter()
	G.get_diameter()
	G.calcUntilLayer = G.diameter
	#G.preprocess_neighbors_with_bfs()
	#G.preprocess_calc_distances()
	
	#G.preprocess_calc_distances_with_threshold()

	#G.create_distances_network()
	#G.preprocess_parameters_random_walk()

	#G.calcSpectralGap()

	G.simulate_walks(args.num_walks, args.walk_length)

	walks = G.get_ramdom_walks()

	learn_embeddings(walks)

if __name__ == "__main__":
	args = parse_args()
	main(args)
