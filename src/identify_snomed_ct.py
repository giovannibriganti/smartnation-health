from rag_snomed import identify_snomed_ct


if __name__ == "__main__":
    snomed_ct = identify_snomed_ct(
        "attaque cardiaque",
        config_path="./pipeline_meta/snomed_ct_meta.yaml",
    )
    # 104784, Heart dise
    print(snomed_ct)
