from time import strftime as now
from pathlib import Path as path


# ------------------------------------------ #
#           RECORDLIST PARAMETERS            #
# ------------------------------------------ #
WINDOWS_SIZE = (1280, 640)

# ------------------------------------------ #
#               DATE AND TIME                #
# ------------------------------------------ #
def DATE() -> str:
    return now('%d/%m/%Y')


def TIME() -> str:
    return now('%H:%M')


# ------------------------------------------ #
#                    PATH                    #
# ------------------------------------------ #
JSON_STOCK_PATH = './db/Stock.json'
JSON_SALES_PATH = './db/Sales.json'
JSON_BUYS_PATH = './db/Buys.json'
JSON_PATHS = (JSON_STOCK_PATH, JSON_SALES_PATH, JSON_BUYS_PATH)
CSV_SALES_PATH = './db/Sales.csv'
CSV_BUYS_PATH = './db/Buys.csv'
DESKTOP = str(path.home()).replace('\\', '/') + '/Desktop/'

# ------------------------------------------ #
#               CSV HEADERS                  #
# ------------------------------------------ #
CSV_HEADER = [[DATE(), TIME()]]
CSV_STOCK_HEADER = CSV_HEADER + [['NOMBRE', 'PRECIO POR UNIDAD', 'STOCK']]
CSV_SALES_HEADER = [
    [
        'DÍA', 'HORA', 'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK',
        'CANTIDAD VENDIDA', 'PRECIO FINL'
    ]
]
CSV_BUYS_HEADER = [
    [
        'DÍA', 'HORA', 'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK',
        'CANTIDAD COMPRADA', 'PRECIO FINL', 'PROVEEDOR'
    ]
]

# ------------------------------------------ #
#             RECORD PARAMETERS              #
# ------------------------------------------ #
R_TMP_SIZE = (5, 1)
R_TMP_PAD = (0, 1)
NAME_SIZE = R_TMP_SIZE
NAME_PAD = R_TMP_PAD
UNIT_PRICE_SIZE = R_TMP_SIZE
UNIT_PRICE_PAD = R_TMP_PAD
STOCK_SIZE = R_TMP_SIZE
STOCK_PAD = R_TMP_PAD
SPIN_SIZE = R_TMP_SIZE
SPIN_PAD = R_TMP_PAD
SPIN_VALUES = [i for i in range(-100, 101, 5)]
CHECK_PAD = R_TMP_PAD
AMOUNT_SIZE = R_TMP_SIZE
AMOUNT_PAD = R_TMP_PAD
FINAL_PRICE_SIZE = R_TMP_SIZE
FINAL_PRICE_PAD = R_TMP_PAD
SUPPLIER_SIZE = R_TMP_SIZE
SUPPLIER_PAD = R_TMP_PAD

# ------------------------------------------ #
#           RECORDLIST PARAMETERS            #
# ------------------------------------------ #
RL_TMP_SIZE = (1241, 300)
RL_TMP_PAD = (0, 1)
RECORDLIST_COLUMN_SIZE = RL_TMP_SIZE
RECORDLIST_COLUMN_PAD = RL_TMP_PAD
SALELIST_COLUMN_SIZE = RL_TMP_SIZE
SALELIST_COLUMN_PAD = RL_TMP_PAD
BUYLIST_COLUMN_SIZE = RL_TMP_SIZE
BUYLIST_COLUMN_PAD = RL_TMP_PAD

# ------------------------------------------ #
#               SECTION SIZES                #
# ------------------------------------------ #
RL_S_TMP_SIZE = (717, 398)
RL_S_TMP_PAD = ((0, 0), (0, 0))
STOCKLIST_S_SIZE = (1258, 398)
STOCKLIST_S_PAD = RL_S_TMP_PAD
SALELIST_S_SIZE = RL_S_TMP_SIZE
SALELIST_S_PAD = RL_S_TMP_PAD
BUYSECTION_S_SIZE = RL_S_TMP_SIZE
BUYSECTION_S_PAD = RL_S_TMP_PAD

# ------------------------------------------ #
#             SECTION PARAMETERS             #
# ------------------------------------------ #
S_TMP_SIZE = (5, 5)
S_TMP_PAD = ((0, 0), (0, 0))
FINDER_INPUT_KEY = ',finder_input'
FINDER_INPUT_SIZE = S_TMP_SIZE
FINDER_INPUT_PAD = S_TMP_PAD
FINDER_BUTTON_KEY = ',finder_button'
FINDER_BUTTON_PAD = S_TMP_PAD
FINDER_BUTTON_TEXT = '🔍'
FINDER_BUTTON_TOOLTIP = ''
SORTER_COMBO_KEY = ''
SORTER_COMBO_SIZE = S_TMP_SIZE
SORTER_COMBO_PAD = S_TMP_PAD
SORTER_COMBO_TOOLTIP = ''
SORTER_COMBO_STOCK_VALUES = ['NOMBRE', 'PRECIO POR UNIDAD', 'STOCK']
SORTER_COMBO_SALES_VALUES = [
    'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK', 'CANTIDAD VENDIDA', 'PRECIO FINAL'
]
SORTER_COMBO_BUYS_VALUES = [
    'NOMBRE', 'PRECIO POR UNIDAD', 'STOCK', 'CANTIDAD COMPRADA', 'PRECIO FINL',
    'PROVEEDOR'
]
SORTER_BUTTON_UP_KEY = ',finder_inputsorter_button_up'
SORTER_BUTTON_DOWN_KEY = ',sorter_button_down'
SORTER_BUTTON_PAD = S_TMP_PAD
SORTER_BUTTON_UP_TEXT = '⬊'
SORTER_BUTTON_DOWN_TEXT = '⬋'
SORTER_BUTTON_UP_TOOLTIP = ''
SORTER_BUTTON_DOWN_TOOLTIP = ''
CLEANER_COMBO_KEY = ',cleaner_combo'
CLEANER_COMBO_SIZE = S_TMP_SIZE
CLEANER_COMBO_PAD = S_TMP_PAD
CLEANER_BUTTON_KEY = ',cleaner_button'
CLEANER_BUTTON_PAD = S_TMP_PAD
CLEANER_BUTTON_TEXT = '―'
CLEANER_BUTTON_TOOLTIP = ''
APPLY_BUTTON_KEY = ',apply'
APPLY_BUTTON_PAD = S_TMP_PAD
APPLY_BUTTON_TEXT = '✔'
APPLY_BUTTON_TOOLTIP = ''
INDEX_RADIO_SIZE = S_TMP_SIZE
INDEX_RADIO_PAD = S_TMP_PAD
INDEX_COLUMN_PAD = S_TMP_PAD
INDEX_INPUT_NAME_SIZE = S_TMP_SIZE
INDEX_INPUT_NAME_PAD = S_TMP_PAD
INDEX_INPUT_NAME_TEXT = 'NOMBRE'
INDEX_INPUT_UNIT_PRICE_SIZE = S_TMP_SIZE
INDEX_INPUT_UNIT_PRICE_PAD = S_TMP_PAD
INDEX_INPUT_UNIT_PRICE_TEXT = '$/U'
INDEX_INPUT_STOCK_SIZE = S_TMP_SIZE
INDEX_INPUT_STOCK_PAD = S_TMP_PAD
INDEX_INPUT_STOCK_TEXT = 'STOCK'
INDEX_INPUT_PERCENT_SIZE = S_TMP_SIZE
INDEX_INPUT_PERCENT_PAD = S_TMP_PAD
INDEX_INPUT_PERCENT_TEXT = '%'
INDEX_INPUT_FINAL_PRICE_SIZE = S_TMP_SIZE
INDEX_INPUT_FINAL_PRICE_PAD = S_TMP_PAD
INDEX_INPUT_FINAL_PRICE_TEXT = '$/F'
INDEX_INPUT_AMOUNT_SIZE = S_TMP_SIZE
INDEX_INPUT_AMOUNT_PAD = S_TMP_PAD
INDEX_INPUT_AMOUNT_TEXT = ''
INDEX_INPUT_SUPPLIER_SIZE = S_TMP_SIZE
INDEX_INPUT_SUPPLIER_PAD = S_TMP_PAD
INDEX_INPUT_SUPPLIER_TEXT = ''
ADDER_SPIN_KEY = 'spin_adder'
ADDER_SPIN_SIZE = S_TMP_SIZE
ADDER_SPIN_PAD = S_TMP_PAD
ADDER_SPIN_VALUES = [i for i in range(1, 30, 2)]
ADDER_BUTTON_KEY = 'button_adder'
ADDER_BUTTON_PAD = S_TMP_PAD
ADDER_BUTTON_TEXT = '＋'
ADDER_BUTTON_TOOLTIP = '',
STOCK_SECTION_CLEANER_OPTIONS = ['SELECCIONADOS']
SAVE_AS_BUTTON_KEY = ''
SAVE_AS_BUTTON_PAD = S_TMP_PAD
SAVE_AS_BUTTON_TEXT = '💾'
SAVE_AS_BUTTON_TOOLTIP = ''
SAVE_AS_BUTTON_INITIAL_FOLDER = DESKTOP + f'Reporte {DATE()} {TIME()}.csv'
COMMERCE_BUTTON_KEY = ',commerce'
COMMERCE_BUTTON_PAD = S_TMP_PAD
COMMERCE_BUTTON_TEXT = ''
COMMERCE_BUTTON_TOOLTIP = '💲'
TOTAL_PRICE_KEY = ''
TOTAL_PRICE_SIZE = S_TMP_SIZE
TOTAL_PRICE_PAD = S_TMP_PAD
PRE_VISULIZATOR_BUTTON_KEY = ',pre_visualizator'
PRE_VISULIZATOR_BUTTON_PAD = S_TMP_PAD
PRE_VISULIZATOR_BUTTON_TEXT = ''
PRE_VISULIZATOR_BUTTON_TOOLTIP = ''

BUTTON_IMAGE = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA9ElEQVQ4T3VTWRYDMQiS+x/aPgWX2HY+ZkkiAjKwuJB3g5s5+Om6c6E24qmzhnxVKRf7AiGiOI/BzBtIHREtYEAcdi9gMqn6g+nZnaAikl9N63n/U5zi2FPNEkAo2mhMqFsfLilRQ2lt2euBiKZLbnDISyIVfZ46moIfwpO091KS7dmcTqwpFPGRU9PrebVzBI4BSMIQmwxwbTxebmc02JsTO80rW6N1RUQesE45cM0kKOWET9qaSQleyM0g9Na1O++Zn7xSwkzyB2FpfXP6JkypLev4gxCaUr5NLN9rf0f5B8c97zdA5NU5eLSuP/icksGT7Q/rqoAi4wjvpQAAAABJRU5ErkJggg=='
# BUTTON_IMAGE = None
BUTTON_IMAGE_SIZE = (52, 22)
