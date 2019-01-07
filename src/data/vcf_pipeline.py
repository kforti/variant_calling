from vcf_config import VCF_CONFIG as config
import subprocess
import os
from pathlib import Path

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

def variant_calling_v1(data, data_len, save_dir, ref_genome):
    """Variant calling with minimap2, samtools, and bcftools"""
    save_path = Path(save_dir)
    if not save_path.exists():
        save_path.mkdir()

    for i in range(data_len):
        data_path = next(data)
        process = subprocess.Popen("echo hello", shell=True)
        process.wait()

        ## Map fastq to Indexed Reference Genome
        fastq = data_path.replace(".gz", "")
        fastq = fastq.replace("../../data/external/malaria_SciRep2018/R7.3_fastq/", "")
        print("fastq ", fastq)
        sam = save_dir + fastq.replace('.fq', '.sam')
        print("sam ", sam)
        map_to_genome = 'minimap2 -ax map-ont ' + ref_genome + ' ' + data_path + ' > ' + sam
        process = subprocess.Popen(map_to_genome, shell=True)
        process.wait()

        ## Convert Sam to Bam
        bam = save_dir + fastq.replace('.fq', '.bam')
        print("bam ", bam)
        sam_to_bam = 'samtools view -b -S -o ' + bam + ' ' + sam
        process = subprocess.Popen(sam_to_bam, shell=True)
        process.wait()

        ## Sort Bam
        sorted_bam = save_dir + fastq.replace('.fq', '.sorted.bam')
        print("sorted-bam ", sorted_bam)
        sort_bam = 'samtools sort ' + bam + ' -o ' + sorted_bam
        process = subprocess.Popen(sort_bam, shell=True)
        process.wait()

        ## Index Bam
        bam_index = bam + '.bai'
        print("bam index", bam_index)
        index_sorted_bam = 'samtools index ' + sorted_bam + ' ' + bam_index
        process = subprocess.Popen(index_sorted_bam, shell=True)
        process.wait()

        ## Pileup
        bcf = save_dir + fastq.replace('.fq', '.bcf')
        print("bcf ", bcf)
        pileup = 'bcftools mpileup -Ob -f ' + ref_genome + ' ' + sorted_bam + ' > ' + bcf
        process = subprocess.Popen(pileup, shell=True)
        process.wait()

        ## Variant Calling
        vcf = save_dir + fastq.replace('.fq', '.vcf')
        print("vcf ", vcf)
        variants = 'bcftools call -c -v ' + bcf + ' > ' + vcf
        process = subprocess.Popen(variants, shell=True)
        process.wait()


if __name__ == '__main__':
    ######################################################################################
    # Load Modules                                                                       #
    ######################################################################################
    modules = config["load_modules"]
    load_modules(modules)

    ######################################################################################
    # Variant_call_v1                                                                       #
    ######################################################################################

    data_path = "../../data" + config["data_directory"]
    data_len = len([i for i in os.listdir(data_path) if not i.startswith('.')])
    data_gen = data_generator(data_path)

    ref_genome = "../../data" + config["ref_genome"]

    save_dir = "../../data" + config["save_directory"]

    variant_calling_v1(data_gen, data_len, save_dir, ref_genome)
