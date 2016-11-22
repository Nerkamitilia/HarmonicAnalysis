'''
    The idea of this code is to make requests to the MusicBrainz api,
    in order to obtain the mbids of all string quartets (and each movement)
    from Mozart, Beethoven and Haydn, and organize that information in a
    python dictionary, for future uses.

    Nestor Napoles, November 2016
    nestor.napoles@upf.edu
'''
import json
import argparse
import musicbrainzngs

# MusicBrainz ID of Joseph Haydn
haydn_mbid = 'c130b0fb-5dce-449d-9f40-1437f889f7fe'
# MusicBrainz ID of Amadeus Mozart
mozart_mbid = 'b972f589-fb0e-474e-b64a-803b0364fa75'
# MusicBrainz ID of Ludwig van Beethoven
beethoven_mbid = '1f9df192-a621-4f54-8850-2c5373b7eac9'
# Main dictionary
string_quartets = {haydn_mbid:{},
                   mozart_mbid:{},
                   beethoven_mbid:{}}

musicbrainzngs.set_useragent(
    "harmonic analysis of string quartets",
    "0.1",
    "https://github.com/nerkamitilia/HarmonicAnalysis",
)

def filterQuartets(quartet_list, composer_id):
    composed_quartets = {}
    other_quartets = {}
    for quartet in quartet_list:
        quartet_id = quartet['id']
        if quartet['type'] == 'Quartet':
            for artist in quartet['artist-relation-list']:
                if artist['type'] == 'composer':
                    if artist['artist']['id'] == composer_id:
                        composed_quartets[quartet_id] = quartet
                    else:
                        other_quartets[quartet_id] = quartet
    return composed_quartets, other_quartets

def fillQuartetInformation(composed_quartets):
    quartet_count = len(composed_quartets)
    full_quartet_dict = dict()
    # Fetching information about each node
    for idx,work_id in enumerate(composed_quartets):
        print '\tFetching quartet information...({}/{})'.format(idx+1,quartet_count)
        work_info = musicbrainzngs.get_work_by_id(work_id, includes=['work-rels'])['work']
        # Parts could have made an entry of this work already
        if work_id in full_quartet_dict:
            curr_node = full_quartet_dict[work_id]
        # New work that has not been parsed before
        else:
            curr_node = {'title':work_info['title']}
        # Filtering garbage mbid entries, like this: 30d4080a-d195-3f03-88e3-585aae505398
        if 'work-relation-list' in work_info:
            for related_work in work_info['work-relation-list']:
                related_work_id = related_work['work']['id']
                related_work_title = related_work['work']['title']
                if related_work['type'] == 'parts':
                    # Detecting a parent work for this node
                    if 'direction' in related_work and related_work['direction'] == 'backward':
                        parent_id = related_work_id
                        parent_title = related_work['work']['title']
                        curr_node['part-parent'] = parent_id
                        if parent_id not in full_quartet_dict:
                            # This child will instantiate the parent
                            full_quartet_dict[parent_id] = dict()
                            full_quartet_dict[parent_id]['title'] = parent_title
                            full_quartet_dict[parent_id]['part-list'] = {}
                        full_quartet_dict[parent_id]['part-list'][work_id] = curr_node
                    else:
                        if work_id not in full_quartet_dict:
                            # This parent will instantiate itself in the dictionary
                            full_quartet_dict[work_id] = curr_node
                            curr_node['part-list'] = {}
                        child_id = related_work_id
                        child_title = related_work_title
                        curr_node['part-list'][child_id] = {'title': child_title, 'part-parent':work_id}
    # Filtering non-root works, e.g., (Op.53 No.1, Op.53 No.2, Op.53 No.3  ---> All contained within Op.53)
    full_quartet_dict = { work_id: full_quartet_dict[work_id] for work_id in full_quartet_dict if 'part-parent' not in full_quartet_dict[work_id]}
    return full_quartet_dict

def main(args):
    with open(args.output_file, 'w') as outfile:
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
            full_quartet_dict = fillQuartetInformation(composed_quartets)
            # Assign the quartet information to the composer entry in the dictionary
            composer['quartet-list'] = full_quartet_dict
        outfile.write(json.dumps(string_quartets))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract string quartet information.')
    parser.add_argument('output_file', help='The output json file')
    args = parser.parse_args()
    main(args)
