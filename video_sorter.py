import os
import shutil

def sort_data_by_category():
    file_sources = ['with_sound_csv', 'without_sound_csv']
    for file_source in file_sources:
        get_files = os.listdir(file_source)
        videos = {
            "speaking": {
                "_Ellen",
                "_conversation",
                "_-Uy5LTocHmoA",
                "_-SZYXQ-6bfiQ",
                "_-RbgxpagCY_c",
                "_-n524y8uPUaU",
                "_-J0Q4L68o3xE",
                "_-idLVnagjl_s",
                "_-g4fQ5iOVzsI",
                "_-ey9J7w98wlI",
                "_-ey9J7w98wlI",
                "_-72f3ayGhMEA",
                "_-5h95uTtPeck",
                "_-4SilhsTuDU0",
                "_-1LM84FSzW0g",
                "_-0cfJOmUaNNI"
            },
            "music": {
                "_band",
                "_-TCUsegqBZ_M",
                "_-SJIbpqgYWGw",
                "_-gTB1nfK-0Ac",
                "_-eGGFGota5_A",
                "_-dBM3eM9HOoA",
                "_-Bvu9m__ZX60"
            },
            "miscellanea": {
                "_-RSYbTSTz91g",
                "_-RrGhiInqXhc",
                "_-I-43DzvhxX8_",
                "_-gy4TI-6j5po",
                "_-eqmjLZGZ36k",
                "_-72f3ayGhMEA"
            }
        }
        for g in get_files:
            for categoria, arquivos in videos.items():
                for arquivo in arquivos:
                    if arquivo in g:
                        print(f"Copiando arquivos da pasta: {g} para {categoria}")

                        file_source_path = os.path.join(file_source, g)
                        file_destination = os.path.join('categorias-' + ('c' if file_source == 'with_sound_csv' else 's'), categoria, g)

                        if os.path.isdir(file_source_path):
                            os.makedirs(file_destination, exist_ok=True)

                            for csv_file in os.listdir(file_source_path):
                                if csv_file.endswith(".csv"):
                                    full_csv_path = os.path.join(file_source_path, csv_file)
                                    print(f"Copiando arquivo CSV: {csv_file}")
                                    shutil.copy2(full_csv_path, os.path.join(file_destination, csv_file))