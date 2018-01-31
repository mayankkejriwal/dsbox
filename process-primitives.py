import glob, codecs, json, re
import os

dsbox_path = '/Users/mayankkejriwal/datasets/d3m/jan-2018/primitives_repo/'

def serialize_paths_jsons(input_folder = dsbox_path+'v2018.1.5', output = dsbox_path+'v2018.1.5.jl'):
    # files = glob.glob(input_folder)
    folders1 = [x[0] for x in os.walk(input_folder)]
    out = codecs.open(output, 'w')
    file_paths = list()
    # print folders1
    for folder in folders1:
        k = glob.glob(folder+'/*.json')
        if len(k) >= 1:
            file_paths += k

    # print file_paths
    for fp in file_paths:
        obj = json.load(codecs.open(fp, 'r'))
        answer = dict()
        answer[fp] = obj
        json.dump(answer, out)
        out.write('\n')
    out.close()

def prefix_clustering_naive(primitives_file=dsbox_path+'primitives.jl', output_file=dsbox_path+'two_level_clustering_naive.json'):
    """
    The clustering is naive because (1) the clustering does not result in a tree hierarchy since some primitives
    have multiple algorithm types, (2) it does not account for 'advanced' algorithms. Both of these issues
    are dealt with in the next function
    :param primitives_file:
    :param output_file:
    :return:
    """
    answer = dict()
    answer['PrimitivesOntology'] = dict()
    # primitive_families = dict()
    with codecs.open(primitives_file, 'r') as f:
        for line in f:
            obj = json.loads(line[0:-1])
            k = obj.keys()[0]
            primitive_family = obj[k]['primitive_family']
            algorithm_types = obj[k]['algorithm_types'] # this is a list
            if primitive_family not in answer['PrimitivesOntology']:
                answer['PrimitivesOntology'][primitive_family] = dict()
            for a in algorithm_types:
                if a not in answer['PrimitivesOntology'][primitive_family]:
                    answer['PrimitivesOntology'][primitive_family][a] = list()
                answer['PrimitivesOntology'][primitive_family][a].append(k[len(dsbox_path):])



    # new_dict = _serialize_clustering_results(answer)
    out = codecs.open(output_file, 'w')
    json.dump(answer, out, indent=4)
    out.close()

def prefix_clustering(primitives_file=dsbox_path+'primitives.jl', output_file=dsbox_path+'two_level_clustering.json'):
    """
    The clustering handles some of the issues noted in prefix_clustering_naive; however, the solution is rather
    ad-hoc.
    :param primitives_file:
    :param output_file:
    :return:
    """
    answer = dict()
    answer['PrimitivesOntology'] = dict()
    answer['PrimitivesOntology']['ADVANCED'] = dict()
    multi_algorithm_types = 0
    # primitive_families = dict()
    with codecs.open(primitives_file, 'r') as f:
        for line in f:
            obj = json.loads(line[0:-1])
            k = obj.keys()[0]
            primitive_family = obj[k]['primitive_family']
            algorithm_types = obj[k]['algorithm_types'] # this is a list

            # special case 1: advanced algorithms we do not really want to be using for the jan. 2018 hackathon
            if 'distil.Goat' in k or 'distil.simon' in k or 'distil.duke' in k:
                if primitive_family not in answer['PrimitivesOntology']['ADVANCED']:
                    answer['PrimitivesOntology']['ADVANCED'][primitive_family] = dict()
                for a in algorithm_types:
                    if a not in answer['PrimitivesOntology']['ADVANCED'][primitive_family]:
                        answer['PrimitivesOntology']['ADVANCED'][primitive_family][a] = list()
                    answer['PrimitivesOntology']['ADVANCED'][primitive_family][a].append(k[len(dsbox_path):])
                continue

            #special case 2: when multiple algorithm types are found. Right now, we modify algorithm types and let
            #the next if do it's thing subsequently.
            if len(algorithm_types) > 1:
                multi_algorithm_types += 1
                if 'd3m.primitives.d3metafeatureextraction.D3MetafeatureExtraction' in k: # in the latest pull occurs in both 2018.1.5 and 2018.1.26
                    algorithm_types = [u'DATA_PROFILING']
                elif 'd3m.primitives.datasmash' in k and 'v2018.1.26' in k:
                    algorithm_types = [u'HIDDEN_MARKOV_MODEL']
                elif 'd3m.primitives.cmu.autonlab.find_projections.Search' in k and 'v2018.1.26' in k:
                    algorithm_types = [u'DECISION_TREE']
                elif 'd3m.primitives.corex_text.CorexText' in k and 'v2018.1.5' in k:
                    algorithm_types = [u'LATENT_DIRICHLET_ALLOCATION']
                elif 'd3m.primitives.dsbox.KnnImputation' in k: # in the latest pull occurs in both 2018.1.5 and 2018.1.26
                    algorithm_types = [u'IMPUTATION']
                elif 'd3m.primitives.test.RandomPrimitive' in k and 'v2018.1.26' in k: # in the latest pull occurs in both 2018.1.5 and 2018.1.26
                    algorithm_types = [u'NORMAL_DISTRIBUTION']
                elif 'd3m.primitives.spider.featurization.AudioFeaturization' in k and 'v2018.1.26' in k: # in the latest pull occurs in both 2018.1.5 and 2018.1.26
                    algorithm_types = [u'INFORMATION_ENTROPY']
                elif 'd3m.primitives.spider.distance.RFD' in k and 'v2018.1.26' in k: # in the latest pull occurs in both 2018.1.5 and 2018.1.26
                    algorithm_types = [u'RANDOM_FOREST']
                else:
                    print line
                    raise Exception

            if primitive_family not in answer['PrimitivesOntology']:
                answer['PrimitivesOntology'][primitive_family] = dict()
            for a in algorithm_types:
                if a not in answer['PrimitivesOntology'][primitive_family]:
                    answer['PrimitivesOntology'][primitive_family][a] = list()
                answer['PrimitivesOntology'][primitive_family][a].append(k[len(dsbox_path):])



    # new_dict = _serialize_clustering_results(answer)
    out = codecs.open(output_file, 'w')
    json.dump(answer, out, indent=4)
    out.close()
    print 'primitives with multiple algorithm types...',str(multi_algorithm_types)


def print_paths_with_multi_algorithm_types(primitives_file=dsbox_path+'primitives.jl'):
    with codecs.open(primitives_file, 'r') as f:
        for line in f:
            obj = json.loads(line[0:-1])
            k = obj.keys()[0]
            primitive_family = obj[k]['primitive_family']
            # print primitive_family
            algorithm_types = obj[k]['algorithm_types']
            if len(algorithm_types) > 1:
                print k
                print algorithm_types

def serialize_sklearn_primitives_to_skeleton_json(sklearn_text=dsbox_path+'sklearn-primitives.txt',output_file=dsbox_path+'sklearn-primitives-skeleton.jl'):
    out = codecs.open(output_file, 'w')
    with codecs.open(sklearn_text, 'r', 'utf-8') as f:
        for line in f:
            line = line[0:-1]
            answer = dict()
            answer[line] = dict()
            answer[line]['primitive_family'] = ""
            answer[line]['algorithm_types'] = []
            json.dump(answer, out)
            out.write('\n')
            # print line
    out.close()

# serialize_sklearn_primitives_to_skeleton_json()
# serialize_paths_jsons()
# print_paths_with_multi_algorithm_types()
# prefix_clustering()
# serialize_paths_jsons()