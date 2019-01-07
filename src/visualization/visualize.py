import allel
import os
import numpy as np


class VariantsData:
    data = {}
    def __init__(self, chromosome, position, raw_depth, variant_depth, ref, alt):
        self.chromosome = chromosome
        self.position = position
        self.raw_depth = raw_depth
        self.variant_depth = variant_depth
        self.ref = ref
        self.alt = alt
        # print('ref', self.ref)
        # print(self.alt)

        self._load_data()

    def _load_data(self):
        # data = (self.chromosome, self.position, self.raw_depth, self.variant_depth, self.ref, self.alt)
        # VariantsData.data.append(data)
        if self.chromosome in VariantsData.data.keys():
            if self.position in VariantsData.data[self.chromosome].keys():
                if self.alt in VariantsData.data[self.chromosome][self.position]['variants']:
                    VariantsData.data[self.chromosome][self.position]['variants'][self.alt][0] += self.raw_depth
                    VariantsData.data[self.chromosome][self.position]['variants'][self.alt][1] += self.variant_depth
                    VariantsData.data[self.chromosome][self.position]['variants'][self.alt][2] += 1
                elif not VariantsData.data[self.chromosome][self.position]['reference'][self.ref]:
                    VariantsData.data[self.chromosome][self.position]['reference'] = self.ref
                    VariantsData.data[self.chromosome][self.position]['variants'][self.alt][0] = self.raw_depth
                    VariantsData.data[self.chromosome][self.position]['variants'][self.alt][1] = self.variant_depth
                    VariantsData.data[self.chromosome][self.position]['variants'][self.alt][2] = 1
            else:
                VariantsData.data[self.chromosome][self.position] = {'reference': self.ref, 'variants': {self.alt: [self.raw_depth, self.variant_depth, 1]}}
        else:
            VariantsData.data[self.chromosome] = {}

        return

    @classmethod
    def get_data(self):
        print(VariantsData.data.keys())
        for key in VariantsData.data.keys():
            for i in VariantsData.data[key].keys():
                print(i)
                print(VariantsData.data[key][i])




def load_variants_data(vcf_data, variants_index, threshold=5):
    for index in variants_index:
        variant_depth = sum(vcf_data['variants/DP4'][index][-2:])
        if variant_depth >= threshold:
            print(vcf_data['samples'])
            variants_data = VariantsData(vcf_data['variants/CHROM'][index],
                                         vcf_data['variants/POS'][index],
                                         vcf_data['variants/DP'][index],
                                         variant_depth,
                                         vcf_data['variants/REF'][index],
                                         vcf_data['variants/ALT'][index][0])

if __name__ == '__main__':

    ## Grab vcf files
    data_path = '../../data/processed/variant_call_v1'
    vcf_files = []
    counter = 0
    for file in os.listdir('../../data/processed/variant_call_v1'):
        if file[-4:] == '.vcf':
            vcf_files.append(allel.read_vcf(data_path + '/' + file, fields=['samples', 'variants/REF', 'variants/ALT', 'variants/CHROM', 'variants/POS', 'variants/QUAL', 'variants/DP', 'variants/DP4', 'variants/INDEL']))

    # print(counter)
    ## Get variant position
    for vcf in vcf_files:
        if vcf:
            variants = []
            for index, x in np.ndenumerate(vcf['variants/INDEL']):
                if x == False:
                    variants.append(index[0])
            load_variants_data(vcf, variants)

    VariantsData.get_data()
