#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''
    The idea of this code is to make requests to the MusicBrainz api,
    in order to obtain the mbids of all string quartets (and each movement)
    from Mozart, Beethoven and Haydn, and organize that information in a
    python dictionary, for future uses.

    This file downloads the corpus from KernScores according to the json file
    that contains all the information about the composers and quartets

    Nestor Napoles, December 2016
    nestor.napoles@upf.edu
'''
import urllib2
import json
import common
import os
import string
import argparse
from subprocess import call

local_url = None
local_location_beethoven = 'beethoven/quartets/kern'
local_location_haydn = 'haydn/quartets/kern'
local_location_mozart = 'mozart/quartets/kern'

ks_url = 'http://kern.humdrum.org/'
ks_corpus_folder = 'cgi-bin/ksdata'
ks_location_beethoven = 'users/craig/classical/beethoven/quartet'
ks_location_haydn = 'musedata/haydn/quartet'
ks_location_mozart = 'musedata/mozart/quartet'

# Location of the quartets in the local repository
local_location_dict = {
    common.haydn_mbid: local_location_haydn,
    common.beethoven_mbid: local_location_beethoven,
    common.mozart_mbid: local_location_mozart
}

# Location of the quartets in the server
ks_location_dict = {
    common.haydn_mbid: ks_location_haydn,
    common.beethoven_mbid: ks_location_beethoven,
    common.mozart_mbid: ks_location_mozart
}

def genLocalUrl(composer_id, filestring):
    composer_location = local_location_dict[composer_id]
    folder = os.path.join(local_url, composer_location)
    return os.path.join(folder, filestring)

def genQueryUrl(composer_id, filestring, formt='kern'):
    composer_location = ks_location_dict[composer_id]
    return '{}{}?l={}&file={}&f={}'.format(ks_url, ks_corpus_folder, composer_location, filestring, formt)

def readDict(json_file):
    f = open(json_file, 'r')
    json_str = f.read().encode("ascii", "ignore")
    return json.loads(json_str)

# Replaces invalid characters for a directory name
def stripQuartetTitle(title):
    rstr = title
    mode_i = title.lower().find('major')
    if mode_i == -1:
        mode_i = title.lower().find('minor')
    if mode_i != -1:
        tonality = title[:mode_i].split()[-1]
        rstr = '{} {}'.format(tonality, title[mode_i:])
    return rstr.replace(':','-').replace('"','')

def stripMvmtTitle(title):
    maxchars = 64
    return title[:maxchars].replace(':','-').replace('"','').replace('\xc3'.decode('cp437'),'u')

def genHaydnKernFilename(quartet_info, mvmt_id):
    if not 'opus-number' in quartet_info['catalog-info']:
        print 'Missing catalog information for {}'.format(mvmt_id)
        return ''
    opus_number = quartet_info['catalog-info']['opus-number']
    mvmt_number = quartet_info['part-list'][mvmt_id]['part-number']
    if len(opus_number) == 2:
        return 'op{:02d}n{}-{:02d}.krn'.format(int(opus_number[0]), int(opus_number[1]), mvmt_number)
    else:
        return 'op{:02d}-{:02d}.krn'.format(int(opus_number[0]), mvmt_number)

def genBeethovenKernFilename(quartet_info, mvmt_id):
    quartet_number = quartet_info['quartet-number']
    mvmt_number = quartet_info['part-list'][mvmt_id]['part-number']
    return 'quartet{:02d}-{}.krn'.format(quartet_number, mvmt_number)

def genMozartKernFilename(quartet_info, mvmt_id):
    if not 'koechel' in quartet_info['catalog-info']:
        print 'Missing catalog information for {}'.format(mvmt_id)
        return ''
    mvmt_number = quartet_info['part-list'][mvmt_id]['part-number']
    koechel_number = quartet_info['catalog-info']['koechel']
    for k in koechel_number:
        if k.isdigit():
            return 'k{:03d}-{:02d}.krn'.format(int(k), mvmt_number)

def genKernFilename(composer_id, quartet_info, mvmt_id):
    rstr = ''
    if common.haydn_mbid == composer_id:
        rstr = genHaydnKernFilename(quartet_info, mvmt_id)
    elif common.beethoven_mbid == composer_id:
        rstr = genBeethovenKernFilename(quartet_info, mvmt_id)
    elif common.mozart_mbid == composer_id:
        rstr = genMozartKernFilename(quartet_info, mvmt_id)
    return rstr

def downloadCorpus(json_file, out_dir, mbids=False, localcorpus=None, tsroot=None):
    global local_url
    local_url = localcorpus
    quartet_dict = readDict(json_file)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for composer_id, composer_info in quartet_dict.iteritems():
        # Creating directory for this composer
        if mbids:
            composer_dir = composer_id
        else:
            composer_dir = composer_info['sort-name']
        composer_dir = os.path.join(out_dir, composer_dir)
        if not os.path.exists(composer_dir):
            os.makedirs(composer_dir)
        for quartet_id, quartet_info in composer_info['quartet-list'].iteritems():
            # Creating directory for this quartet
            if mbids:
                quartet_dir = quartet_id
            else:
                quartet_title = stripQuartetTitle(quartet_info['title'])
                quartet_dir = '{:02d} - {}'.format(quartet_info['quartet-number'], quartet_title)
            quartet_dir = os.path.join(composer_dir, quartet_dir)
            if not os.path.exists(quartet_dir):
                os.makedirs(quartet_dir)
            for mvmt_id, mvmt_info in quartet_info['part-list'].iteritems():
                # Creating directory for this quartet
                if mbids:
                    mvmt_dir = mvmt_id
                else:
                    mvmt_dir = stripMvmtTitle(mvmt_info['title'])
                mvmt_dir = os.path.join(quartet_dir, mvmt_dir)
                if not os.path.exists(mvmt_dir):
                    os.makedirs(mvmt_dir)
                krn_name = genKernFilename(composer_id, quartet_info, mvmt_id)
                if krn_name == '':
                    continue
                if not local_url:
                    query_url = genQueryUrl(composer_id, krn_name)
                    krn_file = urllib2.urlopen(query_url).read()
                else:
                    query_url = genLocalUrl(composer_id, krn_name)
                    if os.path.exists(query_url):
                        fd = open(query_url)
                        krn_file = fd.read()
                    else:
                        krn_file = ''                    
                if krn_file == '':
                    print 'Failed to retreive {} from {}'.format(krn_name, query_url)
                    if os.path.exists(mvmt_dir):
                        os.rmdir(mvmt_dir)
                    continue
                if os.path.exists(mvmt_dir):
                    output_file = os.path.join(mvmt_dir, krn_name)
                    if not os.path.exists(output_file):
                        try:
                            f = open(output_file, "w")
                            f.write(krn_file)
                            f.close()
                            print 'Success, {}'.format(query_url)
                            if tsroot:
                                with open('{}_tsroot.krn'.format(output_file), "w") as tsroot_out:
                                    call([tsroot, "-rp", output_file], stdout=tsroot_out)
                        except IOError:
                            print 'IOError, {}'.format(output_file)
                    else:
                        print 'Skip, {}'.format(query_url)            
            if not os.listdir(quartet_dir):
                print 'Removing empty folder {}'.format(quartet_dir)
                os.rmdir(quartet_dir)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download the corpus from KernScores.')
    parser.add_argument('input_json', metavar='JSON_FILE', help='The json file containing all the metadata')
    parser.add_argument('--output_dir', metavar='DIRECTORY', default='corpus', help='The output directory where the files are going to be stored')
    parser.add_argument('--tsroot', metavar='TSROOT_ADDRESS', help='Provide an address to the tsroot binary to compute harmonic analysis')
    parser.add_argument('--localcorpus', metavar='LOCAL_CORPUS', help='Attempt to download the files locally' )
    parser.add_argument('--mbids', action='store_const', const=True, default=False, help='Organize the folders per MBIDs')
    args = parser.parse_args()
    downloadCorpus(args.input_json, args.output_dir, args.mbids, args.localcorpus, args.tsroot)
