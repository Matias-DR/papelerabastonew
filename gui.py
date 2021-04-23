import constant as ct
import PySimpleGUI as ps
import domain as dm
from multiprocessing import Process


theme = ct.THEME
ps.theme(theme)


class RecordAdderComponent:
    '''
        Define los elementos para el agregado de registros
            - Spin
            - Button
    '''
    def __init__(self, key):
        self._layout = []
        self._element_record_adder = ps.Spin(values=ct.SPIN_RECORD_ADDER_VALUES, initial_value=0,
                                             size=ct.SIZES['xxxs'], key=key+',spin_add_records')
        self.render_layout(key)

    def layout(self):
        '''
        [  ADD_SPIN, ADD_BTT ]
        '''
        return self._layout

    def add(self):
        return self._element_record_adder.get()

    def render_layout(self, key):
        '''
        [ ADD_SPIN, ADD_BTT ]
        '''
        layout = [
            self._element_record_adder,
            ps.Button(button_text='', image_data=ct.PNG_ADD,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['add'],
                      key=key+',add_records', image_size=ct.BUTTON_SIZE)
        ]
        self._layout = layout


class TraderComponent:
    '''
        Define componentes de comercio:
            - Precio total
            - Porcentaje total
            - Generar comercio
            - Cancelar comercio
    '''
    def __init__(self, key):
        self._key = key
        self._layout = []
        self._element_total_price = ps.Text(text='$0000.00', key=key+',total_price',
                                            background_color='White', text_color='Black')
        self._element_total_percent = ps.Spin(ct.SPIN_PERCENT_VALUES, initial_value=0, size=ct.SIZES['xxs'],
                                              enable_events=True, readonly=True, k=key+',update_total_percent')
        self.render_layout(key)

    def layout(self):
        '''
        [
            TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%
        ]
        '''
        return self._layout

    def render_layout(self, key):
        '''
        [
            TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%
        ]
        '''
        layout = [
            ps.Button(button_text='', image_data=ct.PNG_CART_CANCEL,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['sale_cancel'],
                      key=self._key+',cancel_sale', image_size=ct.BUTTON_SIZE, pad=ct.CART_CANCEL_PAD),
            ps.Button(button_text='', image_data=ct.PNG_CART_ACCEPT,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['sale_accept'],
                      key=self._key+',accept_sale', image_size=ct.BUTTON_SIZE),
            self._element_total_price,
            self._element_total_percent
        ]
        self._layout = layout


class ExporterComponent:
    def __init__(self, key, list_components):
        self._key = key
        self._list_components = list_components
        self._layout = [[]]
        self._element_export_options = ps.Combo(values=['STOCK', 'VENTAS', 'COMPRAS'], default_value='STOCK',
                                                size=ct.SIZES['s'], key=self._key+',export_option', readonly=True)
        self._element_export_path = ps.Input(default_text=ct.EXPORT_PATH, size=ct.SIZES['xxl'],
                                             readonly=True, key=self._key+',export_path')
        self.render_layout()
        self._funcs = {
            'export': self.export
        }

    def layout(self):
        '''
        [
            [ EXP_COMB, EXP_SAVEAS, EXP_IN, EXP_BTT ]
        ]
        '''
        return self._layout

    def render_layout(self):
        '''
        [
            [ EXP_COMB, EXP_SAVEAS, EXP_IN, EXP_BTT ]
        ]
        '''
        exporter = [
            [
                self._element_export_options,
                ps.FileSaveAs(button_text='', initial_folder=ct.EXPORT_PATH,
                              target=(555666777, +2), tooltip=ct.BTT_TOOLTIPS['folder'],
                              image_data=ct.PNG_FOLDER, image_size=ct.BUTTON_SIZE,
                              file_types=(('', '.csv'), ), default_extension='.csv'),
                self._element_export_path,
                ps.Button(button_text='', image_data=ct.PNG_EXPORT,
                          border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['export'],
                          key=self._key+',export', image_size=ct.BUTTON_SIZE)
            ]
        ]
        self._layout = exporter

    def export(self):
        {
            'STOCK': self._list_components[0], 'VENTAS': self._list_components[1], 'COMPRAS': self._list_components[2]
        }[self._element_export_options.get()].export(self._element_export_path.get())

    def callback(self, func):
        self._funcs[func]()


class SectionComponent:
    def __init__(self, key):
        self._key = key
        self._layout = [[]]
        self._element_input_searcher = ps.Input(default_text='', key=self._key+',searcher',
                                                size=ct.SIZES['l'], pad=ct.SEARCHER_PAD)
        self._element_sort_options = ps.Combo(values=self._sort_options, default_value=self._sort_options[0],
                                              size=ct.SIZES['s'], key=self._key+',sort_options', readonly=True)
        self._element_clean_options = ps.Combo(values=self._clean_options, default_value=self._clean_options[0],
                                               size=ct.SIZES['+m'], key=self._key+',clean_options', readonly=True)
        self._funcs = {
            'search': self.search,
            'sort_min_max': self.sort_min_max,
            'sort_max_min': self.sort_max_min,
            'export': self.export
        }

    def layout(self):
        return self._layout

    def render_layout(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN ]
        ]
        '''
        self.render_searcher()
        self.render_sorter()
        self.render_first_index()

    def render_searcher(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT ]
        ]
        '''
        searcher = [
            self._element_input_searcher,
            ps.Button(button_text='', image_data=ct.PNG_SEARCH,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['search'],
                      key=self._key+',search', image_size=ct.BUTTON_SIZE)
        ]
        self._layout[0] += searcher

    def render_sorter(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ]
        ]
        '''
        sorter = [
            self._element_sort_options,
            ps.Button(button_text='', image_data=ct.PNG_SORT_MIN_TO_MAX,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['sort_min_max'],
                      key=self._key+',sort_min_max', image_size=ct.BUTTON_SIZE),
            ps.Button(button_text='', image_data=ct.PNG_SORT_MAX_TO_MIN,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['sort_max_min'],
                      key=self._key+',sort_max_min', image_size=ct.BUTTON_SIZE)
        ]
        self._layout[0] += sorter

    def render_first_index(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN ]
        ]
        '''
        index = [
            ps.Input(default_text='Nombre', size=ct.SIZES['m'],
                     pad=ct.FIRST_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='$ P/U', size=ct.SIZES['+s'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True)
        ]
        self._layout.append(index)

    def callback(self, func):
        self._funcs[func]()

    def render_record_to_top(self, index):
        record_to_top = self._records[index].report()
        for i in reversed(range(1, index+1)):
            self._records[i].update(self._records[i-1].report())
        self._records[0].update(record_to_top)

    def search(self, name):
        index = self._list_control.search(name)
        if index:
            self.render_record_to_top(index)

    def sort(self, sorted_report):
        for i, record in enumerate(self._records):
            record.update(sorted_report[i])

    def sort_min_max(self):
        self.sort(self._list_control.sorted_report_min_max(self._element_sort_options.get()))

    def sort_max_min(self):
        self.sort(self._list_control.sorted_report_max_min(self._element_sort_options.get()))

    def update_rendered_records(self):
        '''
        Actualiza el "layout" según los "registros"
        '''
        for i in range(len(self._layout)):
            self._records[i].update()

    def clean_selected(self):
        self._list_control.clean_selected()

    def export(self, path):
        self._list_control.export(path)

    def save(self):
        self._list_control.save()


class StockSectionComponent(SectionComponent):
    def __init__(self, key):
        self._list_control = dm.StockList()
        self._records = self._list_control.records()
        self._sort_options = [
            'Nombre', '$ P/U', 'Stock', '%'
        ]
        self._clean_options = [
            'Seleccionados', 'Vacíos'
        ]
        super().__init__(key)
        self._record_adder = RecordAdderComponent(self._key)
        funcs = {
            'add_records': self.add_records,
            'clean': self.clean,
            'secure_mode': self.secure_mode
        }
        self._funcs.update(funcs)
        self.render_layout()

    def render_layout(self):
        '''
        [ 
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT, ADD_SPIN, ADD_BTT ]
        ]
        '''
        super().render_layout()
        self.render_index()
        self.render_apply_percent()
        self.render_secure_mode()
        self.render_records()
        self.render_cleaner()
        self.render_record_adder()

    def render_index(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN ]
        ]
        '''
        index = ps.Input(default_text='Stock', size=ct.SIZES['xs'],
                         pad=ct.LAST_INDEX_INPUT_PAD, readonly=True)
        self._layout[-1].append(index)

    def render_apply_percent(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ]
        ]
        '''
        apply = ps.Button(button_text='', image_data=ct.PNG_APPLY,
                          border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['apply_percent'],
                          key=self._key+',apply_percent', image_size=ct.BUTTON_SIZE)
        self._layout[-1].append(apply)

    def render_secure_mode(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ]
        ]
        '''
        self._layout[-1].append(ps.Button(button_text='', key=self._key+',secure_mode',
                                          image_data=ct.PNG_SECURE_MODE(), tooltip=ct.BTT_TOOLTIPS['secure_mode'],
                                          image_size=ct.BUTTON_SIZE, border_width=ct.BTT_BORDER_WIDTH))

    def render_records(self):
        '''
        [ 
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ],
            [ RCS_LIST_COL ]
        ]
        '''
        records = [
            record.fields() for record in self._list_control.records()
        ]
        records_list = [
            ps.Column(layout=records, size=ct.STOCK_RCS_LIST_COL_SIZE,
                      scrollable=True, vertical_scroll_only=True)
        ]
        self._layout.append(records_list)

    def render_cleaner(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT ]
        ]
        '''
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='', image_data=ct.PNG_DELETE,
                      border_width=ct.BTT_BORDER_WIDTH,  tooltip=ct.BTT_TOOLTIPS['delete'],
                      key=self._key+',clean', image_size=ct.BUTTON_SIZE)
        ]
        self._layout.append(cleaner)

    def render_record_adder(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT, SECURE_MODE_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT, ADD_SPIN, ADD_BTT ]
        ]
        '''
        layout = self._record_adder.layout()
        self._layout[-1] += layout

    def secure_mode(self):
        self._layout[1][-1].update(image_data=ct.PNG_SECURE_MODE(),
                                    image_size=ct.BUTTON_SIZE)
        for record in self._records:
            record.secure_mode()

    def add_records(self):
        add = self._record_adder.add()
        if add:
            self._list_control.add_records(add)
            ct.__restart__ = True

    def clean(self):
        if self._element_clean_options.get() == 'Vacíos':
            self._list_control.clean_empty()
        else:
            self._list_control.clean_selected()

    def apply_percent(self):
        self._list_control.apply_percent()


class SalesSectionComponent(SectionComponent):
    def __init__(self, key):
        self._list_control = dm.SaleList()
        self._records = self._list_control.records()
        self._sort_options = [
            'Nombre', '$ P/U', 'Stock', 'Cant.', '$ Fin.', '%'
        ]
        self._clean_options = [
            'Seleccionados', 'Todos'
        ]
        super().__init__(key)
        self._trader = TraderComponent(self._key)
        self.render_layout()

    def render_layout(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],  
            [ RCS_LIST_COL ],  
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]  
        ]
        """
        super().render_layout()
        self.render_index()
        self.render_records()
        self.render_trader()
        self.render_cleaner()

    def render_index(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ]  
        ]
        '''
        index = [
            ps.Input(default_text='Stock', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='Cant.', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='$ Fin.', size=ct.SIZES['xs'],
                     pad=ct.LAST_INDEX_INPUT_PAD, readonly=True),
        ]
        self._layout[-1] += index

    def render_trader(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        '''
        layout = self._trader.layout()
        self._layout.append(layout)

    def render_cleaner(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]
        ]
        '''
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='', image_data=ct.PNG_DELETE,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['delete'],
                      key=self._key+',clean', image_size=ct.BUTTON_SIZE)
        ]
        self._layout[-1] += cleaner

    def render_records(self):
        '''
        [ 
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ]
        ]
        '''
        records = [
            record.fields() for record in self._list_control.records()
        ]
        records_list = [
            ps.Column(layout=records, size=ct.SALES_RCS_LIST_COL_SIZE,
                      scrollable=True, vertical_scroll_only=True)
        ]
        self._layout.append(records_list)


class BuysSectionComponent(SectionComponent):
    def __init__(self, key):
        self._list_control = dm.BuyList()
        self._records = self._list_control.records()
        self._sort_options = [
            'Nombre', '$ P/U', 'Stock', 'Cant.', 'Proveedor', '$ Fin.', '%'
        ]
        self._clean_options = [
            'Seleccionados', 'Todos'
        ]
        super().__init__(key)
        self._trader = TraderComponent(self._key)
        self._record_adder = RecordAdderComponent(self._key)
        funcs = {
            'add_records': self.add_records
        }
        self._funcs.update(funcs)
        self.render_layout()

    def render_layout(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],    
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],  
            [ RCS_LIST_COL ],  
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT, ADD_SPIN, ADD_BTT ]  
        ]
        """
        super().render_layout()
        self.render_index()
        self.render_records()
        self.render_trader()
        self.render_price_collector()
        self.render_cleaner()
        self.render_record_adder()

    def render_index(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ]  
        ]
        '''
        index = [
            ps.Input(default_text='Stock', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='Cant.', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='$ Fin.', size=ct.SIZES['xs'],
                     pad=ct.MID_INDEX_INPUT_PAD, readonly=True),
            ps.Input(default_text='Proveedor', size=ct.SIZES['s'],
                     pad=ct.LAST_INDEX_INPUT_PAD, readonly=True)
        ]
        self._layout[-1] += index

    def render_trader(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        '''
        self._layout.append(self._trader.layout())

    def render_price_collector(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        '''
        price_collector = ps.Button(button_text='', image_data=ct.PNG_REFRESH,
                                    border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['refresh'],
                                    key=self._key+',collect', image_size=ct.BUTTON_SIZE)
        self._layout[0].append(price_collector)

    def render_cleaner(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]
        ]
        '''
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='', image_data=ct.PNG_DELETE,
                      border_width=ct.BTT_BORDER_WIDTH, tooltip=ct.BTT_TOOLTIPS['delete'],
                      key=self._key+',clean', image_size=ct.BUTTON_SIZE)
        ]
        self._layout[-1] += cleaner

    def render_record_adder(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT, ADD_SPIN, ADD_BTT ]
        ]
        '''
        layout = self._record_adder.layout()
        self._layout[-1] += layout

    def render_records(self):
        '''
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ]
        ]
        '''
        records = [
            record.fields() for record in self._list_control.records()
        ]
        records_list = [
            ps.Column(layout=records, size=ct.BUYS_RCS_LIST_COL_SIZE,
                      scrollable=True, vertical_scroll_only=True)
        ]
        self._layout.append(records_list)

    def add_records(self):
        add = self._record_adder.add()
        if add:
            self._list_control.add_records(add)
            ct.__restart__ = True


class Main:
    def __init__(self, location):
        dm.FileManager.file_control()
        self._stock_sc = StockSectionComponent('self._stock_sc')
        self._sales_sc = SalesSectionComponent('self._sales_sc')
        self._buys_sc = BuysSectionComponent('self._buys_sc')
        self._list_components = [
            self._stock_sc, self._sales_sc, self._buys_sc
        ]
        self._exporter = ExporterComponent('self._exporter', self._list_components)
        self._layout = [[]]
        self.render_layout()
        self._win = ps.Window(title='Papelera Abasto', icon=ct.PNG_ICON,
                              layout=self._layout, location=location,
                              font=('Helvetica 14'), finalize=True,
                              margins=(0, 0))

    def render_stock_sc(self):
        '''
        [
            [ COL ]
        ]
        '''
        col = [
            [
                ps.Column(layout=self._stock_sc.layout(), size=ct.STOCK_COL_SIZE, pad=(0, 0))
            ]
        ]
        frame = [
            [
                ps.Frame(title='↓ STOCK ↓', title_color=ct.FRAME_TITLE_COLOR[theme],
                         layout=col, title_location='n')
            ]
        ]
        layout = ps.Column(layout=frame)
        self._layout[0].append(layout)

    def render_buys_sc(self, layout):
        '''
            [
                [ FRAME ],
                [ FRAME ]
            ]
        '''
        col = [
            [
                ps.Column(layout=self._buys_sc.layout(), size=ct.BUYS_COL_SIZE, pad=(0, 0))
            ]
        ]
        buys_sc = [
            ps.Frame(title='↓ COMPRAS ↓', title_color=ct.FRAME_TITLE_COLOR[theme],
                     layout=col, title_location='n')
        ]
        layout.append(buys_sc)

    def render_sales_sc(self, layout):
        '''
            [
                [ FRAME ]
            ]
        '''
        col = [
            [
                ps.Column(layout=self._sales_sc.layout(), size=ct.SALES_COL_SIZE, pad=(0, 0))
            ]
        ]
        sales_sc = ps.Frame(title='↓ VENTAS ↓', title_color=ct.FRAME_TITLE_COLOR[theme],
                            layout=col, title_location='n')
        layout[0].append(sales_sc)

    def render_sales_buys_sc(self):
        '''
            [
                [ COL ]
            ]
        '''
        layout = [[]]
        self.render_sales_sc(layout)
        self.render_buys_sc(layout)
        sales_buys = ps.Column(layout=layout)
        self._layout[0].append(sales_buys)

    def render_options(self):
        options = self._exporter.layout()
        options[0] += [
            ps.Button(button_text='', image_data=ct.PNG_TABLE,
                      image_size=ct.BUTTON_SIZE, border_width=ct.BTT_BORDER_WIDTH),
            ps.Button(button_text='', image_data=ct.PNG_THEME_CHANGE,
                      image_size=ct.BUTTON_SIZE, border_width=ct.BTT_BORDER_WIDTH),
            ps.Button(button_text='', image_data=ct.PNG_EXIT,
                      image_size=ct.BUTTON_SIZE, border_width=ct.BTT_BORDER_WIDTH)
        ]
        options_frame = [
            ps.Frame(title='', title_color=ct.FRAME_TITLE_COLOR[theme],
                     layout=options, title_location='n', pad=ct.OPTIONS_FRAME_PAD)
        ]
        self._layout.append(options_frame)

    def render_layout(self):
        '''
            [
                [ COL, COL ]
            ]
        '''
        self.render_stock_sc()
        self.render_sales_buys_sc()
        # self.render_options()

    def save(self):
        for list_component in self._list_components:
            list_component.save()

    def close(self, timeout=0):
        self._win.read(timeout=timeout)
        self._win.close()
        exit()

    def restart(self):
        Process(target=dm.FileManager.restart, args=(self._win.current_location(), )).start()
        self.close(2000)

    def run(self):
        print(self._layout)
        while True:
            event, _ = self._win.read()
            if event is None:
                self.save()
                self.close()
            print(event)
            var, func = event.split(',')
            getattr(eval(var), 'callback')(func)
            # if ct.__restart__:
            #     self.save()
            #     self.restart()


if __name__ == '__main__':
    Main((20, 20)).run()
