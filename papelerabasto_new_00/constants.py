from time import strftime as now


# ------------------------------------------ #
#               DATE AND TIME                #
# ------------------------------------------ #
DATE = lambda: now('%d/%m/%Y')
TIME = lambda: now('%H:%M')

# ------------------------------------------ #
#                    PATH                    #
# ------------------------------------------ #
JSON_STOCK_PATH = './db/Stock.json'
JSON_SALES_PATH = './db/Sales.json'
JSON_BUYS_PATH = './db/Buys.json'
CSV_SALES_PATH = './db/Sales.csv'
CSV_BUYS_PATH = './db/Buys.csv'

# ------------------------------------------ #
#         RECORD ELEMENT PARAMETERS          #
# ------------------------------------------ #
R_TMP_SIZE = (5, 1)
R_TMP_PAD = (0, 1)
NAME_ELEMENT_SIZE = R_TMP_SIZE
NAME_ELEMENT_PAD = R_TMP_PAD
UNIT_PRICE_ELEMENT_SIZE = R_TMP_SIZE
UNIT_PRICE_ELEMENT_PAD = R_TMP_PAD
STOCK_ELEMENT_SIZE = R_TMP_SIZE
STOCK_ELEMENT_PAD = R_TMP_PAD
SPIN_ELEMENT_SIZE = R_TMP_SIZE
SPIN_ELEMENT_PAD = R_TMP_PAD
SPIN_ELEMENT_VALUES = [i for i in range(-100, 101, 5)]
CHECK_ELEMENT_PAD = R_TMP_PAD
AMOUNT_ELEMENT_SIZE = R_TMP_SIZE
AMOUNT_ELEMENT_PAD = R_TMP_PAD
FINAL_PRICE_ELEMENT_SIZE = R_TMP_SIZE
FINAL_PRICE_ELEMENT_PAD = R_TMP_PAD
SUPPLIER_ELEMENT_SIZE = R_TMP_SIZE
SUPPLIER_ELEMENT_PAD = R_TMP_PAD
BUTTON_BORDER_WIDTH = 3

# ------------------------------------------ #
#       RECORDLIST ELEMENT PARAMETERS        #
# ------------------------------------------ #
RL_TMP_SIZE = (400, 400)
RL_TMP_PAD = (0, 1)
RECORDLIST_COLUMN_SIZE = RL_TMP_SIZE
RECORDLIST_COLUMN_PAD = RL_TMP_PAD
SALELIST_COLUMN_SIZE = RL_TMP_SIZE
SALELIST_COLUMN_PAD = RL_TMP_PAD
BUYSLIST_COLUMN_SIZE = RL_TMP_SIZE
BUYSLIST_COLUMN_PAD = RL_TMP_PAD
