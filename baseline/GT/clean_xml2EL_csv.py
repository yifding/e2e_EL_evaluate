# generate GT prediction for e2e_EL using processed .xml annotations.

import os
import argparse

from gen_anno_from_xml import gen_anno_from_xml


def doc_name_rank(s):
    if 'testa' in s:
        splits = s.split('testa')
        return int(splits[0])
    elif 'testb' in s:
        splits = s.split('testb')
        return int(splits[0])
    else:
        assert '_' in s
        splits = s.split('_')
        assert len(splits) == 2
        return int(splits[0])


def write_xml(dataset, xml_file, redict):
    print('ready to write:', 'dataset', dataset, 'path', xml_file)

    with open(xml_file, 'w') as writer:
        writer.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + '\n')
        writer.write('<' + dataset + '.entityAnnotation>' + '\n')
        if 'aida' in dataset:
            rank_func = doc_name_rank
        else:
            rank_func = str
        for document in sorted(redict.keys(), key=rank_func):
            tmps = redict[document]
            document = document.replace(' ', '_').replace('&', '&amp;')

            # <document docName="20001115_AFP_ARB.0093.eng">
            writer.write('\t' + '<document docName="' + document + '">' + '\n')
            for anno in tmps:
                # a preparation
                mention_txt = anno['mention_txt']
                entity_txt = anno['entity_txt']
                start = anno['start']
                end = anno['end']

                mention_txt = mention_txt.replace('_', ' ').replace('&', '&amp;')
                entity_txt = entity_txt.replace('_', ' ').replace('&', '&amp;')

                # b write things down
                writer.write('\t\t' + '<annotation>' + '\n')

                writer.write('\t\t\t' + '<mention>' + mention_txt + '</mention>' + '\n')
                writer.write('\t\t\t' + '<wikiName>' + entity_txt + '</wikiName>' + '\n')
                writer.write('\t\t\t' + '<offset>' + str(start) + '</offset>' + '\n')
                writer.write('\t\t\t' + '<length>' + str(end - start) + '</length>' + '\n')

                writer.write('\t\t' + '</annotation>' + '\n')

            writer.write('\t' + '</document>' + '\n')
        writer.write('</' + dataset + '.entityAnnotation>' + '\n')


def arg_parse():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(
        '--input_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/processed/wned/ori_xml2revise_xml',
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default='/scratch365/yding4/e2e_EL_evaluate/data/prediction/e2e_EL/GT',
    )

    parser.add_argument(
        '--datasets',
        type=eval,
        default="['ace2004', 'aquaint', 'wikipedia', 'clueweb', 'msnbc']",
    )

    args = parser.parse_args()
    return args


def main():
    args = arg_parse()

    os.makedirs(args.output_dir, exist_ok=True)
    for dataset in args.datasets:
        doc_name2txt, doc_name2anno = gen_anno_from_xml(args.input_dir, dataset)
        xml_file = os.path.join(args.output_dir, dataset + '/' + dataset + '.xml')
        txt_dir = os.path.join(args.output_dir, dataset + '/RawText')
        os.makedirs(txt_dir, exist_ok=True)

        # **YD** sort the annotations by start first, and end second.
        for doc_name in doc_name2anno:
            tmp = doc_name2anno[doc_name]
            tmp = sorted(tmp, key=lambda x: x['end'])
            tmp = sorted(tmp, key=lambda x: x['start'])
            doc_name2anno[doc_name] = list(tmp)

        for doc_name in doc_name2txt:
            txt_file = os.path.join(txt_dir, doc_name)
            with open(txt_file, 'w') as writer:
                writer.write(doc_name2txt[doc_name])

        write_xml(dataset, xml_file, doc_name2anno)


if __name__ == '__main__':
    main()