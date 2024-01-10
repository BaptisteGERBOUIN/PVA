import requests
from tqdm.auto import tqdm
from json import loads
from math import ceil

def scale_unit(value: int | str, unit: str, precision: int=2, divisor: int=1000) -> str:
    value = int(value)
    for threshold, modifier in zip(range(1, 5), ['', 'k', 'M', 'G']):
        if value < divisor**threshold:
            return str(round(value / divisor**(threshold - 1), precision)) + modifier + unit
    return str(round(value / divisor**5, precision)) + 'T' + unit

def get_data_from_api(url: str, params: dict[str, str], page_size: int=5_000, nbr_page: int=3, leavePbar: bool=True, disablePbar: bool=False) -> list[dict[str, ]]:
    if nbr_page is None or nbr_page <= 0:
        head_params = {**params, 'size': 1, 'fields': params['fields'].split(',')[0]}

        response = requests.get(url, params=head_params)
        response.raise_for_status()
        nbr_rows_to_download = response.json().get('count', 0)
        nbr_page = ceil(nbr_rows_to_download / page_size)
    else:
        nbr_rows_to_download = page_size * nbr_page

    final_json_data = list()
    total_downloaded = 0
    api_pbar = tqdm(total=nbr_rows_to_download, desc=f'API: {url}', unit='row', unit_scale=True, leave=leavePbar, disable=disablePbar)
    for current_page in range(1, nbr_page + 1):
        params.update({'page': current_page, 'size': page_size})
        response = requests.get(url, params=params, stream=True)
        response.raise_for_status()

        with tqdm(desc=f'Downloading page {current_page}', unit='B', unit_scale=True, miniters=1, leave=False, disable=disablePbar) as sub_pbar:
            json_data = ''
            for data in response.iter_content(1000, decode_unicode=True):
                sub_pbar.update(len(data))
                api_pbar.update(data.count('{'))
                json_data += data
            api_pbar.update(-1)

            total_downloaded += sub_pbar.format_dict['n']
            api_pbar.set_description(f'API: {url} [Total downloaded: {scale_unit(total_downloaded, unit="B")}]')

        final_json_data.extend(loads(json_data).get('data', []))
    return final_json_data