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
string_quartets = {#haydn_mbid:{},
                   mozart_mbid:{}}
#                   beethoven_mbid:{}}

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
    for idx,quartet_id in enumerate(composed_quartets):
        print '\tFetching quartet information...({}/{})'.format(idx+1,quartet_count)
        quartet_info = musicbrainzngs.get_work_by_id(quartet_id, includes=['work-rels'])['work']
        curr_quartet = {'title':quartet_info['title']}
        curr_quartet['movement-list'] = {}
        for related_work in quartet_info['work-relation-list']:
            related_work_id = related_work['work']['id']
            if related_work['type'] == 'parts':
                # Detecting a parent opus
                if 'direction' in related_work and related_work['direction'] == 'backward':
                    parent_id = related_work['work']['id']
                    parent_title = related_work['work']['title']
                    if parent_id not in full_quartet_dict:
                        full_quartet_dict[parent_id] = dict()
                        full_quartet_dict[parent_id]['title'] = parent_title
                        full_quartet_dict[parent_id]['work-list'] = {}
                    full_quartet_dict[parent_id]['work-list'][quartet_id] = curr_quartet
                # If not a parent opus, then it is a movement from the quartet
                else:
                    curr_quartet['movement-list'][related_work_id] = {'title':related_work['work']['title']}
    return full_quartet_dict

def main(args):
    for composer_id in string_quartets:
        # Lucene query: Looking for all string quartets of the composers in the dictionary
        composer_info = musicbrainzngs.get_artist_by_id(composer_id)['artist']
        # Get the appropiate entry in the string_quartets dictionary
        composer = string_quartets[composer_id]
        # Fill the basic information of the composer
        composer['name'] = composer_info['name']
        composer['sort-name'] = composer_info['sort-name']
        composer['quartet-list'] = {}
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
    with open(args.output_file, 'w') as outfile:
        outfile.write(json.dumps(string_quartets))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract string quartet information.')
    parser.add_argument('output_file', help='The output json file')
    args = parser.parse_args()
    main(args)
