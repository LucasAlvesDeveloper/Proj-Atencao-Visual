from os import path

import plot_fixagem_olho
import video_sorter

if __name__ == '__main__':
    if not path.exists('categorias-s') or not path.exists('categorias-c'):
        video_sorter.sort_data_by_category()
    plot_fixagem_olho.run_eye_fixation_plot()
