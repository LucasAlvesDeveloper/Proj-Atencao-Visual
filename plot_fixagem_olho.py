import os
import glob
from collections import namedtuple

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import video_sorter

ROOT_FOLDER = '.'
OUTPUT_FOLDER = 'saida'

# Tipagem de tupla, não altere
Point = namedtuple('Point', ['x', 'y'])

def run_eye_fixation_plot():
    no_sound_general_points_list: list[Point[float,float]] = []
    with_sound_general_points_list: list[Point[float,float]] = []

    for category in os.listdir('categorias-s'):
        no_sound_category_points_list: list[Point[float,float]] = []
        with_sound_category_points_list: list[Point[float,float]] = []
        for video in os.listdir(f'categorias-s/{category}'):
            no_sound_points_list: list[Point[float, float]] = []
            with_sound_points_list: list[Point[float, float]] = []

            read_data_from_video(no_sound_points_list, os.path.join(f'{ROOT_FOLDER}/categorias-s', category, video))
            read_data_from_video(with_sound_points_list, os.path.join(f'{ROOT_FOLDER}/categorias-c', category, video))

            plot_data(
                'Pontos de Fixação dos Olhos',
                f'{ROOT_FOLDER}/{OUTPUT_FOLDER}/{category}',
                f'{video}',
                no_sound_points_list,
                with_sound_points_list
            )

            no_sound_category_points_list.extend(no_sound_points_list)
            with_sound_category_points_list.extend(with_sound_points_list)

        plot_data(
            f'Pontos de Fixação dos Olhos na categoria {category}',
            f'{ROOT_FOLDER}/{OUTPUT_FOLDER}',
            f'{category}',
            no_sound_category_points_list,
            with_sound_category_points_list
        )

        no_sound_general_points_list.extend(no_sound_category_points_list)
        with_sound_general_points_list.extend(with_sound_category_points_list)

    plot_data(
        'Gráfico de Fixação Geral dos Olhos',
        f'{OUTPUT_FOLDER}',
        'geral',
        no_sound_general_points_list,
        with_sound_general_points_list
    )

    pass

def read_data_from_video(points_list: list[Point[float, float]], path: str):
    for file in glob.glob('*.csv', root_dir=path):
        full_path = os.path.join(path, file)
        data_frame: pd.DataFrame = pd.read_csv(full_path)
        eye_fixation_data: pd.DataFrame = data_frame[['EF_latitude_h', 'EF_longitude_w']]
        for y, x in eye_fixation_data.to_numpy():
            data_point = Point(x, y)
            points_list.append(data_point)


def plot_data(
        title: str,
        output_folder: str,
        filename: str,
        no_sound_eye_positions: list[Point[float, float]],
        with_sound_eye_positions: list[Point[float, float]]
):
    fig: plt.Figure = plt.figure(figsize=(12.8, 7.2))
    fig.suptitle(title)

    no_sound_axis: plt.Axes = fig.add_subplot(2, 1, 1, frameon=False)
    no_sound_axis.set_xticks([])
    no_sound_axis.set_yticks([])
    no_sound_axis.set_title('Sem Som', pad=10)

    no_sound_axis_x: plt.Axes = fig.add_subplot(2, 2, 1)
    no_sound_axis_y: plt.Axes = fig.add_subplot(2, 2, 2)
    plot_eye_fixation_hist(
        no_sound_axis_x,
        no_sound_axis_y,
        no_sound_eye_positions
    )

    with_sound_axis: plt.Axes = fig.add_subplot(2, 1, 2, frameon=False)
    with_sound_axis.set_xticks([])
    with_sound_axis.set_yticks([])
    with_sound_axis.set_title('Com Som', pad=10)

    with_sound_axis_x: plt.Axes = fig.add_subplot(2, 2, 3)
    with_sound_axis_y: plt.Axes = fig.add_subplot(2, 2, 4)
    plot_eye_fixation_hist(
        with_sound_axis_x,
        with_sound_axis_y,
        with_sound_eye_positions
    )

    plt.tight_layout()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    fig.savefig(f'{output_folder}/{filename}.png')
    plt.close(fig)
    print(f'Salvo {output_folder}/{filename}.png')
    pass


def plot_eye_fixation_hist(
        x_axis: plt.Axes,
        y_axis: plt.Axes,
        eye_positions_list: list[Point[float, float]]
):
    pos_list_x = [(point.x - 0.5) * 360.0 for point in eye_positions_list]
    pos_list_y = [(point.y - 0.5) * 180.0 for point in eye_positions_list]

    pos_list_x = np.asarray(pos_list_x)
    pos_list_y = np.asarray(pos_list_y)

    mean_x: float = np.mean(pos_list_x).astype(float)
    mean_y: float = np.mean(pos_list_y).astype(float)

    median_x: float = np.median(pos_list_x).astype(float)
    median_y: float = np.median(pos_list_y).astype(float)

    standard_deviation_x = np.std(pos_list_x).astype(float)
    standard_deviation_y = np.std(pos_list_y).astype(float)

    x_axis.set_xlabel('Longitude (em graus)')
    x_axis.set_xlim(-180, 180)
    x_axis.set_xticks([x for x in np.arange(-180, 181, 360 / 12)])
    x_axis.axvline(mean_x, color='red', label=f'Média = {mean_x:.3f}')
    x_axis.axvline(median_x, color='yellow', label=f'Mediana = {median_x:.3f}')
    x_axis.axvline(standard_deviation_x, color='black', label=f'Desvio Padrão = {standard_deviation_x:.3f}')
    x_axis.hist(pos_list_x, bins=180, label='Pontos de fixação')
    x_axis.legend(loc='upper left')

    y_axis.set_xlabel('Latitude (em graus)')
    y_axis.set_xlim(-90, 90)
    y_axis.set_xticks([x for x in np.arange(-90, 91, 180 / 12)])
    y_axis.axvline(mean_y, color='red', label=f'Média = {mean_y:.3f}')
    y_axis.axvline(median_y, color='yellow', label=f'Mediana = {median_y:.3f}')
    y_axis.axvline(standard_deviation_y, color='black', label=f'Desvio Padrão = {standard_deviation_y:.3f}')
    y_axis.hist(pos_list_y, bins=180, label='Pontos de fixação')
    y_axis.legend(loc='upper left')
    pass


if __name__ == '__main__':
    # É importante não parar o programa enquanto estiver a rodar o organizador de categoria.
    # Se o programa tiver erro, experimente deletar as duas pastas em questão.
    if not os.path.exists('categorias-s') or not os.path.exists('categorias-c'):
        video_sorter.sort_data_by_category()
    run_eye_fixation_plot()
    pass
