class PanelSublista {
            
    constructor(panelName, url) {

        this.url = $SCRIPT_ROOT + url;

        //Selectores jQuery de elementos
        this.$panel = $(`#panel_${panelName}`);
        this.$modalConfirm = $('#id_modal_confirmacion');

        // estado por defecto inicial de un boton/expandir contraer
        this.expandContractState = 'expand'
        this.btnExpCont = `#${panelName}_expandContract_button`
        
        // Bandera que se utiliza para que campo de busqueda no pierda el foco al quedar vacio
        this.inFocus = 0;

        // Parametros de Solicitudes al api
        this.queryParameters = {
            page: 1,
            ids_delete: "",
            ids_unlink: "",
            ids_link: "",
            text_search: "", 
            flag_text_search: "", 
        };
    };

    // ----------------------------------------------------------------------------------------------------
    // Llamada desde el cuadro de texto de búsqueda.
    // ----------------------------------------------------------------------------------------------------
    showTablistByText(minchr) {
        // el parametro mionchar lo empleabamos cuando bscabamos a partir de n caracteres
        this.inFocus = 1
        this.queryParameters.text_search = this.$panel.find('#select_input_text').val()
        this.queryParameters.page = 1;
        this._showTablist();
    
    };

    // ----------------------------------------------------------------------------------------------------
    // Llamada desde los botones de paginación.
    // ----------------------------------------------------------------------------------------------------
    showTablistByPage(page) {
        !!page && (this.queryParameters.page = page);
        this._showTablist();
    };

    // ----------------------------------------------------------------------------------------------------
    // Llamada desde los botones de borrado de fila de la tabla.
    // ----------------------------------------------------------------------------------------------------
    showTablistByDelete(ids_delete) {
        if (!ids_delete)
            ids_delete = this.giveRowsSelected();
        else // TODO Cuando quites lo relacionado con panelFichero te puedes volar esra conversión
            ids_delete = ids_delete.toString();
        this.queryParameters.ids_delete = ids_delete;
        this._showTablist();
        this._closeConfirmPanel();
    };

    // ----------------------------------------------------------------------------------------------------
    // Llamada desde los botones de desvincular de fila de la tabla.
    // ----------------------------------------------------------------------------------------------------
    show_tablist_by_unlink(ids_unlink) {
        !ids_unlink && (ids_unlink = this.giveRowsSelected());
        this.queryParameters.ids_unlink = ids_unlink;
        this._showTablist();
        this._closeConfirmPanel();
    };

    // ----------------------------------------------------------------------------------------------------
    // Llamada desde los botones de vincular de fila de la tabla.
    // ----------------------------------------------------------------------------------------------------
    link_tablist(ids_link) {
       this.queryParameters.ids_link = ids_link.toString();
       this._showTablist();
    }

    // ----------------------------------------------------------------------------------------------------
    // Funcion que hace la llamada al api y gestiona la presentacion del tab
    // ----------------------------------------------------------------------------------------------------
    _showTablist() {
        const self = this;
        this.queryParameters.flag_text_search = this.queryParameters.text_search ? 1 : "";
        this.$panel.find('tbody').addClass("hidden");
        this.$panel.find('.imgPreLoader').removeClass("hidden");
        
        $.get(  this.url, 
                this.queryParameters, 
                function( htmlData ) {
                    self.$panel.empty().html(htmlData);
                    if (self.inFocus || self.queryParameters.text_search){
                        self.$panel.find('#select_input_text').attr('tabindex', -1).focus();
                    };
                })
                .done(function() {
                    self._childrenFuntion();
                    self.manageExpContState();
                  })
                .fail(function(xhr) {
                    self.$panel.find('.imgPreLoader').addClass("hidden");
                    self._postErrorMsg(xhr);
                    // alert( `Ha habido un error por parte del servidor - Status: ${xhr.status} ${xhr.statusText}` );
                })
                .always(function() {
                    // Limpia el objeto Literal(Diccionario)
                    $.each(self.queryParameters, function(key) {
                        if (key != 'page' && key != 'text_search')
                            self.queryParameters[key] = "";
                    }); 
                });
    };

    // ----------------------------------------------------------------------------------------------------
    // // Espacio Para Funciones de clases que hereden de esta
    // ----------------------------------------------------------------------------------------------------
    _childrenFuntion() {
        // Espacio Para Funciones de clases que hereden de esta
    }

    // ----------------------------------------------------------------------------------------------------
    // Comprueba si existe un boton de expandir/contraer en el tab y mantiende su estado al tenr una busqueda
    // ----------------------------------------------------------------------------------------------------
    manageExpContState() {
        const $btnExpCont = $(this.btnExpCont);
        if ($btnExpCont.length) {
            if (this.expandContractState !== $btnExpCont.data('state')) {
                this.expandContractState = 'expand';
                this.expandContract($btnExpCont);
            }
        }
    };
 
    // ----------------------------------------------------------------------------------------------------
    // Hace que una tabla se contraiga/expanda para mostrar o no campos de m a m
    // ----------------------------------------------------------------------------------------------------
    expandContract($btnExpCont) {
        if (this.expandContractState == 'expand') {
            this.$panel.find('table .hidden').removeClass('hidden').addClass('_hidden');
            $btnExpCont.empty().append('<i class="fas fa-compress-alt"></i> Contraer').data('state', 'contranct');
            this.expandContractState = 'contranct'
            
        } else {
            this.$panel.find('table ._hidden').removeClass('_hidden').addClass('hidden');
            $btnExpCont.empty().append('<i class="fas fa-expand-alt"></i> Expandir').data('state', 'expand');
            this.expandContractState = 'expand'
        }
    };

    // ----------------------------------------------------------------------------------------------------
    // Devuelve las filas seleccionadas
    // ----------------------------------------------------------------------------------------------------
    giveRowsSelected() {
        let ids_selected = "";
        this.$panel.find('tr').each((i, el) =>{
            const $el = $(el)
            if ($el.hasClass('selected')) {
                const idx =$el.data('id');
                !!ids_selected && (ids_selected += ',');
                ids_selected += idx;
            };
        });
        return ids_selected;       
    }

    // ----------------------------------------------------------------------------------------------------
    // Activa el Panel Seleccionado
    // ----------------------------------------------------------------------------------------------------
    active() {
        this.$panel.addClass('active');
    };

    // ----------------------------------------------------------------------------------------------------
    // Oculta el pandel de Confirmacion
    // ----------------------------------------------------------------------------------------------------
    _closeConfirmPanel() {
        this.$modalConfirm.modal('hide');
    }

    _postErrorMsg(xhr) {
        this.$panel
            .html(
                `<div id="_panel_messages" class="mt-3">
                    <div class="alert alert-warning alert-dismissible fade show" role="alert">
                        <strong>¡ATENCIÓN!</strong> Se produjo un error en el lado servidor - Estatus: ${xhr.status} ${xhr.statusText}
                        <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                </div>`
            );
    }

}