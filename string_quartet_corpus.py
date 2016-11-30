import argparse
from generate_json import generateJson


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract string quartet information.')
    parser.add_argument('output_file', help='The output json file')
    args = parser.parse_args()
    generateJson(args.output_file)
