import constant as ct
import PySimpleGUI as ps
import domain as dm


ps.theme('PapelerAbasto')


class RecordComponent:
    def __init__(self):
        pass

    def __str__(self):
        # RETORNA SUS DATOS CONCATENADOS EN STR
        pass


class StockRecordComponent(RecordComponent):
    def __init__(self):
        pass


class SaleRecordComponent(RecordComponent):
    def __init__(self):
        pass


class BuyRecordComponent(RecordComponent):
    def __init__(self):
        pass


class ListComponent:
    """
        Clase padre para las listas de registros
        Define los componentes en comun entre las listas
            - Column
            - Registros
            - Key
    """
    def __init__(self, key, records):
        self._key = key
        self._records = records

    def render_layout(self):
        """
            COL
        """
        layout = [
            [record] for record in self._records
        ]
        return ps.Column(layout=layout, scrollable=True, vertical_scroll_only=True)

    def render_record_to_top(self, index):
        """
        Recibe el índice de un registro y lo sube
        """
        record_to_top = self._records[index].list()
        for i in reversed(range(1, index+1)):
            self._records[i].update_rendered_record(self._records[i-1].list())
        self._records[0].update_rendered_record(record_to_top)

    def update_rendered_records(self, records):
        """
        Recibe una lista de registros con la que actualiza la renderizada
        """
        for i in range(len(records)):
            self._records[i].update_rendered_record(records[i].list())

    def sort_min_max(self):
        sorted_records = sorted(self._records, key=lambda record: record.name())
        self.update_rendered_records(sorted_records.list())

    def sort_max_min(self):
        sorted_records = sorted(self._records, key=lambda record: record.name(), reverse=True)
        self.update_rendered_records(sorted_records.list())


class StockListComponent(ListComponent):
    def __init__(self, key):
        self._stock_control = dm.StockList()
        super().__init__(key, self._stock_control.records())

    def search(self):
        index = self._stock_control.search()
        if index:
            self.render_record_to_top(index)


class SaleListComponent(ListComponent):
    def __init__(self, key):
        self._sale_control = dm.SaleList()
        super().__init__(key, self._sale_control.records())

    def search(self):
        index = self._sale_control.search()
        if index:
            self.render_record_to_top(index)


class BuyListComponent(ListComponent):
    def __init__(self, key):
        self._buy_control = dm.BuyList()
        super().__init__(key, self._buy_control.records())

    def search(self):
        index = self._buy_control.search()
        if index:
            self.render_record_to_top(index)


class SectionComponent:
    """
        Clase padre para el render de las secciones
        Define los elementos en común entre secciones:
            - Buscador
            - Ordenador
            - Descartador
            - Índice principal
            - Exportador
    """
    # COMO LISTA DE REGISTROS CREAR E INSERTAR UNA CLASE QUE CONTROLE LA PARTE GRÁFICA DE LA MISMA
    # CREAR E INSERTAR UNA NUEVA CLASE QUE REFIERA AL CONTROL DE TIPO CÁLCULO DE ESA LISTA
    # EL RENDER DE LA LISTA SE ENCUENTRA EN ESA CLASE, Y LE PIDE LOS REGISTROS A LA CLASE DE CONTROL
    # LA CLAVE PARA CADA CAMPO DE CADA REGISTRO DE CADA LISTA DE REGISTROS, DEBE SER NUMÉRICA SEGÚN LEN(LISTA)
    # LA FUENTE SE CAMBIA DESDE WINDOW CON font=('Arial 44') "font=('tipo_de_letra tamaño')"
    def __init__(self, key):
        self._key = key
        self._layout = [[]]
        self._element_input_searcher = ps.Input(default_text='', key=self._key+',searcher', size=ct.SIZES['l'])
        self._sort_options = ['Nombre', 'Stock', '$ P/U']
        self._element_sort_options = ps.Combo(values=self._sort_options, default_value=self._sort_options[0],
                                              size=ct.SIZES['m'], key=self._key+',sort_options', readonly=True)
        self._clean_options = ['Seleccionados']
        self._element_clean_options = ps.Combo(values=self._clean_options, default_value=self._clean_options[0],
                                               size=ct.SIZES['m'], key=self._key+',clean_options', readonly=True)

    def render_searcher(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT ]
        ]
        """
        searcher = [
            self._element_input_searcher,
            ps.Button(button_text='', image_data=ct.PNG_SEARCH,
                      key=self._key+',search', image_size=ct.BUTTON_SIZE)
        ]
        self._layout[0] += searcher

    def render_sorter(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ]
        ]
        """
        sorter = [
            self._element_sort_options,
            ps.Button(button_text='', image_data=ct.PNG_SORT_MIN_TO_MAX,
                      key=self._key+',sort_min_to_max', image_size=ct.BUTTON_SIZE),
            ps.Button(button_text='', image_data=ct.PNG_SORT_MAX_TO_MIN,
                      key=self._key+',sort_max_to_min', image_size=ct.BUTTON_SIZE)
        ]
        self._layout[0] += sorter

    def render_index(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN ]
        ]
        """
        index = [
            ps.Input(default_text='Nombre', size=ct.SIZES['l'],
                     pad=ct.FIRST_INPUT_PAD, readonly=True),
            ps.Input(default_text='Stock', size=ct.SIZES['xs'],
                     pad=ct.MID_INPUT_PAD, readonly=True)
        ]
        self._layout.append(index)

    def render_layout(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ]
        ]
        """
        self.render_searcher()
        self.render_sorter()


class RecordAdderComponent:
    """
        Define los elementos para el agregado de registros
            - Spin
            - Button
    """
    def __init__(self, key):
        self._layout = []
        self._element_record_adder = ps.Spin(values=ct.SPIN_RECORD_ADDER_VALUES, initial_value=0,
                                             size=ct.SIZES['xs'], key=key+',spin_add_records')
        self.render_layout(key)

    def layout(self):
        """
        [  ADD_SPIN, ADD_BTT ]
        """
        return self._layout

    def render_layout(self, key):
        """
        [ ADD_SPIN, ADD_BTT ]
        """
        layout = [
            self._element_record_adder,
            ps.Button(button_text='', image_data=ct.PNG_ADD,
                      key=key+',add_records', image_size=ct.BUTTON_SIZE)
        ]
        self._layout = layout


class StockSectionComponent(SectionComponent):
    """
        Define elementos propios:
            - Lista de registros
            - Aplicador de porcentajes
    """
    def __init__(self, key):
        super().__init__(key)
        self._clean_options.append('Vacíos')
        self.record_adder = RecordAdderComponent(key)
        self._stock_control = dm.StockList()
        self.render_layout()

    def layout(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT, ADD_SPIN, ADD_BTT ]
        ]
        """
        return self._layout

    def render_index(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN ]
        ]
        """
        index = ps.Input(default_text='$ P/U', size=ct.SIZES['xs'],
                         pad=ct.LAST_INPUT_PAD, readonly=True)
        self._layout[-1].append(index)

    def render_apply_percent(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ]
        ]
        """
        apply = ps.Button(button_text='', image_data=ct.PNG_APPLY,
                          key=self._key+',apply_percent', image_size=ct.BUTTON_SIZE)
        self._layout[-1].append(apply)

    def render_stock_list(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ],
            [ RCS_LIST_COL ]
        ]
        """
        records = self._stock_control.records()
        layout = [
            ps.Column(layout=records, size=ct.STOCK_RCS_LIST_COL_SIZE,
                      scrollable=True, vertical_scroll_only=True)
        ]
        self._layout.append(layout)

    def render_cleaner(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT ]
        ]
        """
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='', image_data=ct.PNG_DELETE,
                      key=self._key+',clean', image_size=ct.BUTTON_SIZE)
        ]
        self._layout.append(cleaner)

    def render_record_adder(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ],
            [ RCS_LIST_COL ],
            [ CLEANER_COMBO, CLEANR_BTT, ADD_SPIN, ADD_BTT ]
        ]
        """
        layout = self.record_adder.layout()
        self._layout[-1] += layout

    def render_layout(self):
        """
        [ 
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, APPLY_BTT ],
            [ CLEANER_COMBO, CLEANR_BTT, ADD_SPIN, ADD_BTT ]
        ]
        """
        super().render_layout()
        super().render_index()
        self.render_index()
        self.render_apply_percent()
        self.render_stock_list()
        self.render_cleaner()
        self.render_record_adder()


class TraderComponent:
    """
        Define componentes de comercio:
            - Precio total
            - Porcentaje total
            - Generar comercio
            - Cancelar comercio
    """
    def __init__(self, key):
        self._key = key
        self._layout = []
        self._element_total_price = ps.Text(text='$0000.00', key=key+',total_price',
                                            background_color='White', text_color='Black')
        self._element_total_percent = ps.Spin(ct.SPIN_PERCENT_VALUES, initial_value=0, size=ct.SIZES['xs'],
                                              enable_events=True, readonly=True, k=key+',update_total_percent')
        self.render_layout(key)

    def layout(self):
        """
        [
            TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%
        ]
        """
        return self._layout

    def render_layout(self, key):
        """
        [
            TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%
        ]
        """
        layout = [
            ps.Button(button_text='', image_data=ct.PNG_CART_CANCEL,
                      key=self._key+',cancel_sale', image_size=ct.BUTTON_SIZE),
            ps.Button(button_text='', image_data=ct.PNG_CART_ACCEPT,
                      key=self._key+',accept_sale', image_size=ct.BUTTON_SIZE),
            self._element_total_price,
            self._element_total_percent
        ]
        self._layout = layout


class SalesSectionComponent(SectionComponent):
    """
        Define elementos propios:
            - Índice propio (lo agrega al principal)
            - Comerciante: TraderComponent
    """
    def __init__(self, key):
        super().__init__(key)
        self._sort_options += [
            'Cant.', '$ Fin.'
        ]
        self._clean_options.append('Todos')
        self._trader = TraderComponent(key)
        self._sales_control = dm.SaleList()
        self.render_layout()

    def layout(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]
        ]
        """
        return self._layout

    def render_index(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ]  
        ]
        """
        index = [
            ps.Input(default_text='$ P/U', size=ct.SIZES['xs'],
                     pad=ct.MID_INPUT_PAD, readonly=True),
            ps.Input(default_text='Cant.', size=ct.SIZES['xs'],
                     pad=ct.MID_INPUT_PAD, readonly=True),
            ps.Input(default_text='$ Fin.', size=ct.SIZES['xs'],
                     pad=ct.LAST_INPUT_PAD, readonly=True),
        ]
        self._layout[-1] += index

    def render_sales_list(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ]
        ]
        """
        records = self._sales_control.records()
        layout = [
            ps.Column(layout=records, size=ct.SALES_RCS_LIST_COL_SIZE,
                      scrollable=True, vertical_scroll_only=True)
        ]
        self._layout.append(layout)

    def render_trader(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        """
        layout = self._trader.layout()
        self._layout.append(layout)

    def render_cleaner(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]
        ]
        """
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='', image_data=ct.PNG_DELETE,
                      key=self._key+',clean', image_size=ct.BUTTON_SIZE)
        ]
        self._layout[-1] += cleaner

    def render_layout(self):
        super().render_layout()
        super().render_index()
        self.render_index()
        self.render_sales_list()
        self.render_trader()
        self.render_cleaner()


class BuysSectionComponent(SectionComponent):
    """
        Define elementos propios:
            - Índice propio (lo agrega al principal)
            - Comerciante: TraderComponent
            - Actualizador de precios
    """
    def __init__(self, key):
        super().__init__(key)
        self._sort_options += [
            'Cant.', 'Proveedor', '$ Fin.'
        ]
        self._clean_options.append('Todos')
        self._trader = TraderComponent(key)
        self._record_adder = RecordAdderComponent(key)
        self._buys_control = dm.BuyList()
        self.render_layout()

    def layout(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT, ADD_SPIN, ADD_BTT ]
        ]
        """
        return self._layout

    def render_index(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ]  
        ]
        """
        index = [
            ps.Input(default_text='$ P/U', size=ct.SIZES['xs'],
                     pad=ct.MID_INPUT_PAD, readonly=True),
            ps.Input(default_text='Cant.', size=ct.SIZES['xs'],
                     pad=ct.MID_INPUT_PAD, readonly=True),
            ps.Input(default_text='Proveedor', size=ct.SIZES['s'],
                     pad=ct.MID_INPUT_PAD, readonly=True),
            ps.Input(default_text='$ Fin.', size=ct.SIZES['xs'],
                     pad=ct.LAST_INPUT_PAD, readonly=True)
        ]
        self._layout[-1] += index

    def render_buys_list(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ]
        ]
        """
        records = self._buys_control.records()
        layout = [
            ps.Column(layout=records, size=ct.BUYS_RCS_LIST_COL_SIZE,
                      scrollable=True, vertical_scroll_only=True)
        ]
        self._layout.append(layout)

    def render_trader(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        """
        layout = self._trader.layout()
        self._layout.append(layout)

    def render_price_collector(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_% ]
        ]
        """
        price_collector = ps.Button(button_text='', image_data=ct.PNG_REFRESH,
                                    key=self._key+',collect', image_size=ct.BUTTON_SIZE)
        self._layout[0].append(price_collector)

    def render_cleaner(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT ]
        ]
        """
        cleaner = [
            self._element_clean_options,
            ps.Button(button_text='', image_data=ct.PNG_DELETE,
                      key=self._key+',clean', image_size=ct.BUTTON_SIZE)
        ]
        self._layout[-1] += cleaner

    def render_record_adder(self):
        """
        [
            [ SEARCH_IN, SEARCH_BTT, SORT_COMBO, SORT_BTT, SORT_BTT, COLLECT_BTT ],  
            [ INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN, INDEX_IN ],
            [ RCS_LIST_COL ],
            [ TRADE_BTT, TRADE_BTT, TEXT_$, SPIN_%, CLEAN_COMBO, CLEAN_BTT, ADD_SPIN, ADD_BTT ]
        ]
        """
        layout = self._record_adder.layout()
        self._layout[-1] += layout

    def render_layout(self):
        super().render_layout()
        super().render_index()
        self.render_index()
        self.render_buys_list()
        self.render_trader()
        self.render_price_collector()
        self.render_cleaner()
        self.render_record_adder()


class ExporterComponent:
    """
        Define los elementos de exportación de listas
    """
    def __init__(self, key):
        self._key = key
        self._layout = [[]]
        self._element_export_path = ps.Input(default_text='', size=ct.SIZES['xxl'],
                                             readonly=True, key=self._key+',export_path')
        self.render_layout()

    def layout(self):
        """
        [
            [ EXP_COMB, EXP_SAVEAS, EXP_IN, EXP_BTT ]
        ]
        """
        return self._layout

    def render_layout(self):
        """
        [
            [ EXP_COMB, EXP_SAVEAS, EXP_IN, EXP_BTT ]
        ]
        """
        exporter = [
            [
                ps.Combo(values=['STOCK', 'VENTAS', 'COMPRAS'], default_value='STOCK',
                         size=ct.SIZES['s'], key=self._key+',export_option', readonly=True),
                ps.FileSaveAs(button_text='', initial_folder=ct.EXPORT_PATH, target=(555666777, +2),
                              image_data=ct.PNG_FOLDER, image_size=ct.BUTTON_SIZE,
                              file_types=(('', '.csv'), ), default_extension='.csv'),
                self._element_export_path,
                ps.Button(button_text='', image_data=ct.PNG_EXPORT,
                          key=self._key+',export', image_size=ct.BUTTON_SIZE)
            ]
        ]
        self._layout = exporter


class Main:
    def __init__(self):
        self._stock_sc = StockSectionComponent('_stock_sc')
        self._sales_sc = SalesSectionComponent('_sales_sc')
        self._buys_sc = BuysSectionComponent('_buys_sc')
        self._exporter = ExporterComponent('_exporter')
        self._layout = [[]]
        self.render_layout()
        self._win = ps.Window(title='Papelera Abasto', layout=self._layout,
                              font=('Arial 14'), finalize=True, location=(0, 0),
                              margins=(0, 0), button_color='#232323')

    def render_stock_sc(self):
        """
        [
            [ COL ]
        ]
        """
        col = [
            [
                ps.Column(layout=self._stock_sc.layout(), size=ct.STOCK_COL_SIZE, pad=(0, 0))
            ]
        ]
        frame = ps.Frame(title='↓ STOCK ↓', layout=col, title_color='White', title_location='n')
        stock_sc = [
            [
                frame
            ]
        ]
        exporter = self._exporter.layout()
        exporter_frame = [
            ps.Frame(title='↓ EXPORTAR A EXCEL ↓', layout=self._exporter.layout(),
                     title_color='White', title_location='n')
        ]
        stock_sc.append(exporter_frame)
        layout = ps.Column(layout=stock_sc)
        self._layout[0].append(layout)

    def render_buys_sc(self, layout):
        """
            [
                [ FRAME ],
                [ FRAME ]
            ]
        """
        col = [
            [
                ps.Column(layout=self._buys_sc.layout(), size=ct.BUYS_COL_SIZE, pad=(0, 0))
            ]
        ]
        buys_sc = [
            ps.Frame(title='↓ COMPRAS ↓', layout=col, title_color='White', title_location='n')
        ]
        layout.append(buys_sc)

    def render_sales_sc(self, layout):
        """
            [
                [ FRAME ]
            ]
        """
        col = [
            [
                ps.Column(layout=self._sales_sc.layout(), size=ct.SALES_COL_SIZE, pad=(0, 0))
            ]
        ]
        sales_sc = ps.Frame(title='↓ VENTAS ↓', layout=col, title_color='White', title_location='n')
        layout[0].append(sales_sc)

    def render_sales_buys_sc(self):
        """
            [
                [ COL ]
            ]
        """
        layout = [[]]
        self.render_sales_sc(layout)
        self.render_buys_sc(layout)
        sales_buys = ps.Column(layout=layout)
        self._layout[0].append(sales_buys)

    def render_layout(self):
        """
            [
                [ COL, COL ]
            ]
        """
        self.render_stock_sc()
        self.render_sales_buys_sc()

    def run(self):
        print(self._layout)
        while True:
            event, _ = self._win.read()
            print(event)
            if event is None:
                self._win.close()
                break


if __name__ == '__main__':
    Main().run()
