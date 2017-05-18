'''
    The idea of this code is to make requests to the MusicBrainz api,
    in order to obtain the mbids of all string quartets (and each movement)
    from Mozart, Beethoven and Haydn, and organize that information in a
    python dictionary, for future uses.

    This file generates the json output from querying to MusicBrainz

    Nestor Napoles, November 2016
    nestor.napoles@upf.edu
'''
import json
import musicbrainzngs
import roman
import common

# Main dictionary
string_quartets = {common.haydn_mbid:{},
                   #common.mozart_mbid:{},
                   #common.beethoven_mbid:{}}

musicbrainzngs.set_useragent(
    "harmonic analysis of string quartets",
    "0.1",
    "https://github.com/napulen/HarmonicAnalysis"
)

def filterQuartets(quartet_list, composer_id):
    composed_quartets = {}
    other_quartets = {}
    for quartet in quartet_list:
        # Ignore all the quartets that are not in the manually parsed list by Rafael Caro
        quartet_id = quartet['id']
        if quartet_id not in common.manual_quartet_lists[composer_id]:
            continue
        if quartet['type'] == 'Quartet':
            for artist in quartet['artist-relation-list']:
                if artist['type'] == 'composer':
                    if artist['artist']['id'] == composer_id:
                        composed_quartets[quartet_id] = quartet
                    else:
                        other_quartets[quartet_id] = quartet
    return composed_quartets, other_quartets

def parseQuartetTitle(quartet_title):
    catalog_information = {}
    title_tokens = quartet_title.lower().split()
    # Checking for Op. XX No. XX entries
    if 'op.' in title_tokens:
        op_i = title_tokens.index('op.')
        opus = title_tokens[op_i + 1].replace(',','')
        catalog_information['opus-number'] = [int(opus)]
        # I am sure there is a better way to check this...
        if (op_i + 1) < (len(title_tokens) - 1):
            if 'no.' == title_tokens[op_i + 2]:
                number = title_tokens[op_i + 3].replace(',', '')
                catalog_information['opus-number'].append(int(number))
    # Checking for K. entries
    if 'k.' in title_tokens:
        k_i = title_tokens.index('k.')
        koechel = title_tokens[k_i + 1]
        koechel = koechel.split('/')
        if len(koechel) == 2:
            catalog_information['koechel'] = [koechel[0], koechel[1]]
        else:
            catalog_information['koechel'] = [koechel[0]]
    # Checking for Hob. entries
    if 'hob.' in title_tokens:
        hob_i = title_tokens.index('hob.')
        hoboken = title_tokens[hob_i + 1]
        hoboken = hoboken.split(':')
        if len(hoboken) != 2:
            print 'Error in hoboken catalog string in\n{}'.format(quartet_title)
        else:
            catalog_information['hoboken'] = [hoboken[0], hoboken[1]]
    return catalog_information

def parsePartTitle(child_title, parent_title):
    tmp_child_title = child_title
    if parent_title in child_title:
        # Remove the name of the quartet from a movement's title
        tmp_child_title = tmp_child_title.replace(parent_title, '')
        # Remove blank spaces at the beginning
        tmp_child_title = tmp_child_title.split(' ', 1)
        if tmp_child_title[0] != ':':
            print 'Strange name in {} from {}'.format(child_title, parent_title)
        tmp_child_title = tmp_child_title[1]
    part_roman_number = tmp_child_title.split('.', 1)[0]
    try:
        part_arabic_number = roman.fromRoman(part_roman_number)
    except roman.InvalidRomanNumeralError:
        part_arabic_number = 99
        print 'Strange name in {} from {}'.format(child_title, parent_title)
    return tmp_child_title, part_arabic_number

def fillQuartetInformation(composer_id, composed_quartets):
    quartet_count = len(composed_quartets)
    full_quartet_dict = dict()
    # Fetching information about each node
    for idx,work_id in enumerate(composed_quartets):
        print '\tFetching quartet information...({}/{})'.format(idx+1,quartet_count)
        work_info = musicbrainzngs.get_work_by_id(work_id, includes=['work-rels'])['work']
        curr_node = {'title':work_info['title']}
        # Fill quartet number from the manually-checked list
        curr_node['quartet-number'] = common.manual_quartet_lists[composer_id].index(work_id) + 1
        # Parse Opus|Koechel|Hoboken information
        curr_node['catalog-info'] = parseQuartetTitle(curr_node['title'])
        # Filtering garbage mbid entries, like this: 30d4080a-d195-3f03-88e3-585aae505398
        if 'work-relation-list' in work_info:
            for related_work in work_info['work-relation-list']:
                related_work_id = related_work['work']['id']
                related_work_title = related_work['work']['title']
                if related_work['type'] == 'parts':
                    # Ignoring a parent node for this work
                    if 'direction' in related_work and related_work['direction'] == 'backward':
                        continue
                    else:
                        if work_id not in full_quartet_dict:
                            # This parent will instantiate itself in the dictionary
                            full_quartet_dict[work_id] = curr_node
                            curr_node['part-list'] = {}
                        child_id = related_work_id
                        child_title, part_number = parsePartTitle(related_work_title, curr_node['title'])
                        curr_node['part-list'][child_id] = {'title': child_title, 'part-parent':work_id, 'part-number': part_number}
    return full_quartet_dict

def generateJson(output_file):
    with open(output_file, 'w') as outfile:
        for composer_id in string_quartets:
            # Lucene query: Looking for all string quartets of the composers in the dictionary
            composer_info = musicbrainzngs.get_artist_by_id(composer_id)['artist']
            # Get the appropiate entry in the string_quartets dictionary
            composer = string_quartets[composer_id]
            # Fill the basic information of the composer
            composer['name'] = composer_info['name']
            composer['sort-name'] = composer_info['sort-name']
            # Starting with quartet information. Make the query to the MusicBrainz API
            query = 'type:Quartet AND arid:{}'.format(composer_id)
            result = musicbrainzngs.search_works(query, limit=100)
            if result['work-count'] > 100:
                print ''' MORE WORKS LEFT, THIS NEEDS MORE QUERY ITERATIONS!! '''
            quartet_list = result['work-list']
            # Filter the list of "real" works from others, e.g., disputed-attributions, dedications, arrangements, etc.
            composed_quartets, other_quartets = filterQuartets(quartet_list, composer_id)
            # Complete all the information of the quartets, i.e., Opus and number, movements, etc.
            print '{}:'.format(composer['name'])
            full_quartet_dict = fillQuartetInformation(composer_id, composed_quartets)
            # Assign the quartet information to the composer entry in the dictionary
            composer['quartet-list'] = full_quartet_dict
        outfile.write(json.dumps(string_quartets))
