from vcf_config import VCF_CONFIG as config
import subprocess
import os

def load_modules(modules):
    for module in modules:
        command = "module load " + module
        subprocess.Popen(command, shell=True)

def data_generator(dir_path):
    for data in os.listdir(dir_path):
        if data.startswith('.'):
            continue
        data_path = dir_path + "/" + data
        yield data_path

def variant_calling_v1(data, data_len, save_dir, ref_gen):
    """Variant calling with minimap2, samtools, and bcftools"""
    for i in range(data_len):
        d = next(data)

        fastq = save_dir + d.replace(".gz", "")
        fastq = d.replace("./../../data/external/malaria_SciRep2018/R7.3_fastq/", "")

        sam = save_dir + fastq.replace('.fq', '.sam')
        map_to_genome = ['minimap2', '-ax', 'map-ont', ref_genome, fastq, '>', sam]
        subprocess.Popen(map_to_genome)

        bam = save_dir + fastq.replace('.fq', '.bam')
        sam_to_bam = ['samtools', 'view', '-b', '-S', '-o', sam, bam]
        subprocess.Popen(sam_to_bam)

        soretd_bam = save_dir + fastq.replace('.fq', '.sorted.bam')
        sort_bam = ['samtools', 'sort', '-o', bam, (sorted_bam + '.bam')]
        subprocess.Popen(soretd_bam)

        bam_index = save_dir + bam + '.bai'
        index_sorted_bam = ['samtools', 'index', sorted_bam, bam_index]
        subprocess.Popen(index_sorted_bam)


        bcf = save_dir + fastq.replace('.fq', '.bcf')
        pileup = ['samtools', 'mpileup', '-g', '-f', ref_genome, sorted_bam, '>', bcf]
        subprocess.Popen(pileup)

        vcf = fastq.replace('.fq', '.vcf')
        variants = ['bcftools', 'call', '-c', '-v', bcf, '>', vcf]
        subprocess.Popen(variants)









if __name__ == '__main__':
    ######################################################################################
    # Load Modules                                                                       #
    ######################################################################################
    modules = config["load_modules"]
    load_modules(modules)

    ######################################################################################
    # Variant_call_v1                                                                       #
    ######################################################################################


    data_path = "./../../data" + config["data_directory"]
    data_len = len([i for i in os.listdir(data_path) if not i.startswith('.')])
    data_gen = data_generator(data_path)

    ref_genome = config["ref_genome"]

    save_dir = config["save_directory"]

    variant_calling_v1(data_gen, data_len, save_dir, ref_genome)
